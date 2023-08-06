import os
import json
from pandas.core.frame import DataFrame


class DataSegment(object):
    def __init__(self, data, segment_id, session, label=None, uuid=None, capture=None):
        self._metadata = [
            "label",
            "capture",
            "segment_id",
            "segment_start",
            "segment_length",
            "columns",
            "session",
            "uuid",
        ]
        self._label = label
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
    def label(self):
        return self._label

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
    def segment_start(self):
        return int(self._original_index[0])

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

        return DataFrame(M)

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
