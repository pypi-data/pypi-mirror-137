import os
import json
from pandas.core.frame import DataFrame
from sensiml.dclproj.utils import plot_segments_labels


class DataSegment(object):
    def __init__(
        self, data, segment_id, session, label_value=None, uuid=None, capture=None
    ):
        self._metadata = [
            "label_value",
            "capture",
            "segment_id",
            "capture_sample_sequence_start",
            "capture_sample_sequence_end",
            "columns",
            "session",
            "uuid",
        ]
        self._label_value = str(label_value)
        self._session = session
        self._segment_id = segment_id
        self._uuid = uuid
        self._original_index = data.index
        self._capture = capture
        self._data = data.reset_index(drop=True)

    def plot(self, **kwargs):
        self._data.plot(title=self.__str__(), **kwargs)

    @property
    def capture(self):
        return self._capture

    @property
    def segment_id(self):
        return self._segment_id

    @property
    def label_value(self):
        return self._label_value

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def data(self):
        return self._data

    @property
    def segment_length(self):
        return int(self._data.shape[0])

    @property
    def columns(self):
        return int(self._data.shape[1])

    @property
    def capture_sample_sequence_start(self):
        return int(self._original_index[0])

    @property
    def capture_sample_sequence_end(self):
        return int(self.capture_sample_sequence_start + self.segment_length)

    @property
    def session(self):
        return self._session

    @property
    def metadata(self):
        return {metadata: getattr(self, metadata) for metadata in self._metadata}

    def to_dict(self):
        return self.metadata

    def __str__(self):
        return " ".join(["{}: {}, ".format(k, v) for k, v in self.metadata.items()])


class DataSegments(dict):
    def plot(self, **kwargs):
        import matplotlib as plt

        plt.rcParams.update({"figure.max_open_warning": 0})
        for _, segment in self.items():
            segment.plot(**kwargs)

    def to_dataframe(self):
        """Returns a dataframe representation of the segment information."""
        M = []
        for _, segment in self.items():
            M.append(segment.metadata)

        tmp_df = DataFrame(M)
        tmp_df["length"] = (
            tmp_df["capture_sample_sequence_end"]
            - tmp_df["capture_sample_sequence_start"]
        )
        return tmp_df.sort_values(
            by=["session", "capture", "capture_sample_sequence_start"]
        ).reset_index(drop=True)

    def to_dict(self, orient="records"):
        return self.to_dataframe().to_dict(orient=orient)

    def export(self, folder="segment_export"):
        """Exports all the segments to the specified folder as individual <UUID>.csv files.
        The metadata is stored in a metadata.json file which has all the info about each segment.
        """
        if not os.path.exists(folder):
            os.mkdir(folder)

        metadata = []
        for _, segment in self.items():
            segment.data.to_csv(os.path.join(folder, segment.uuid + ".csv"), index=None)
            metadata.append(segment.metadata)

        json.dump(metadata, open(os.path.join(folder, "metadata.json"), "w"))

    def list_label_values(self):
        """List all the labels in the DataSegments object"""
        label_values = set()
        for _, segment in self.items():
            label_values.add(segment.label_value)

        return list(label_values)

    def merge_segments(self, dcl, min_length=10000, delta=10):

        merged_segments = merge_segments(self, min_length=10000, delta=10)

        return segment_list_to_datasegments(dcl, DataFrame(merged_segments))


def to_datasegments(data, metdata_columns, label_column):
    """Converts a dataframe into a data segments object"""

    group_columns = metdata_columns + [label_column]
    g = data.groupby(group_columns)
    ds = DataSegments()

    data_columns = [x for x in data.columns if x not in group_columns]

    for key in g.groups.keys():

        metadata = {}
        for index, value in enumerate(group_columns):
            metadata[value] = key[index]

        tmp_df = g.get_group(key)[data_columns]

        ds[tmp_df["uuid"]] = DataSegment(tmp_df, metadata, metadata[label_column])

    return ds


def segment_list_to_datasegments(dcl, labels, session=""):
    """Converts a dataframe into a data segments object"""

    if isinstance(labels, DataFrame):

        # DCL generates segments with this format ""
        if labels.columns.to_list() == [
            "File",
            "Label",
            "Start",
            "End",
            "Length",
        ]:
            label_dict = (
                labels.rename(
                    columns={
                        "File": "capture",
                        "Label": "label_value",
                        "Start": "capture_sample_sequence_start",
                        "End": "capture_sample_sequence_end",
                    },
                )
                .sort_values(by="capture")
                .to_dict(orient="records")
            )
        else:
            label_dict = labels.sort_values(by="capture").to_dict(orient="records")
    else:
        raise Exception("Expected DataFrame")

    data_segments = DataSegments()
    capture_name = None

    for index, label in enumerate(label_dict):

        if capture_name != label["capture"]:
            data = dcl.get_capture(label["capture"])
            capture_name = label["capture"]

        tmp_df = data.iloc[
            label["capture_sample_sequence_start"] : label[
                "capture_sample_sequence_end"
            ]
        ]

        data_segments[index] = DataSegment(
            tmp_df,
            index,
            session=label.get("session", session),
            label_value=label["label_value"],
            capture=label["capture"],
        )

    return data_segments


def merge_segments(segments, min_length=10000, delta=10):
    """Merges data segments that are within a distance delta of each other and have the same class name."""

    def template(segment, min_length=1, start=None, end=None):
        if start is None:
            start = segment["capture_sample_sequence_start"]
        if end is None:
            end = segment["capture_sample_sequence_end"]

        difference = end - start
        if difference < min_length:
            end += int(min_length - difference) // 2
            start -= int(min_length - difference) // 2
        if start < 0:
            print("Error: Start of a segment was less than 0")
            start = 0

        return {
            "capture_sample_sequence_start": start,
            "capture_sample_sequence_end": end,
            "label_value": segment["label_value"],
            "length": end - start,
            "capture": segment["capture"],
            "session": segment["session"],
        }

    seg_groups = segments.to_dataframe().groupby(["session", "capture"])

    for key in seg_groups.groups.keys():

        segment_list = (
            seg_groups.get_group(key)
            .sort_values(by="capture_sample_sequence_start")
            .to_dict(orient="records")
        )

        merge_list = []
        new_segments = []

        for index, segment in enumerate(segment_list):
            if not merge_list:
                if len(segment_list) - 1 == index:
                    new_segments.append(template(segment, min_length=min_length))
                    # print('ending')
                    continue
                elif segment_list[index + 1]["label_value"] != segment["label_value"]:
                    new_segments.append(template(segment, min_length=min_length))
                    # print('no merge list diff value', index)
                    continue
                elif (
                    abs(
                        segment_list[index + 1]["capture_sample_sequence_start"]
                        - segment["capture_sample_sequence_end"]
                    )
                    > delta
                ):
                    new_segments.append(template(segment, min_length=min_length))
                    # print('no merge list to large', index)
                    continue

            if (
                len(segment_list) - 1 != index
                and segment_list[index + 1]["label_value"] == segment["label_value"]
            ):
                if (
                    abs(
                        segment_list[index + 1]["capture_sample_sequence_start"]
                        - segment["capture_sample_sequence_end"]
                    )
                    < delta
                ):
                    if not merge_list:
                        # print('add merge list', index)
                        merge_list.append(index)
                    merge_list.append(index + 1)
            else:
                # do merge
                if merge_list:
                    new_segments.append(
                        template(
                            segment_list[merge_list[0]],
                            min_length=min_length,
                            start=segment_list[merge_list[0]][
                                "capture_sample_sequence_start"
                            ],
                            end=segment_list[merge_list[-1]][
                                "capture_sample_sequence_end"
                            ],
                        )
                    )
                else:
                    new_segments.append(template(segment, min_length=min_length))

                merge_list = []

        if merge_list:
            new_segments.append(
                template(
                    segment_list[merge_list[0]],
                    min_length=min_length,
                    start=segment_list[merge_list[0]]["capture_sample_sequence_start"],
                    end=segment_list[merge_list[-1]]["capture_sample_sequence_end"],
                )
            )

    return new_segments
