from pandas import DataFrame
import numpy as np


import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

from scipy.sparse import coo_matrix


def confusion_matrix(y_true, y_pred, labels, normalize=None):

    labels = np.asarray(labels)
    n_labels = labels.size
    if n_labels == 0:
        raise ValueError("'labels' should contains at least one label.")
    elif y_true.size == 0:
        return np.zeros((n_labels, n_labels), dtype=int)
    elif len(np.intersect1d(y_true, labels)) == 0:
        raise ValueError("At least one label specified must be in y_true")

    sample_weight = np.ones(y_true.shape[0], dtype=np.int64)

    # check_consistent_length(y_true, y_pred, sample_weight)

    if normalize not in ["true", "pred", "all", None]:
        raise ValueError("normalize must be one of {'true', 'pred', 'all', None}")

    n_labels = labels.size
    # If labels are not consecutive integers starting from zero, then
    # y_true and y_pred must be converted into index form
    need_index_conversion = not (
        labels.dtype.kind in {"i", "u", "b"}
        and np.all(labels == np.arange(n_labels))
        and y_true.min() >= 0
        and y_pred.min() >= 0
    )
    if need_index_conversion:
        label_to_ind = {y: x for x, y in enumerate(labels)}
        y_pred = np.array([label_to_ind.get(x, n_labels + 1) for x in y_pred])
        y_true = np.array([label_to_ind.get(x, n_labels + 1) for x in y_true])

    # intersect y_pred, y_true with labels, eliminate items not in labels
    ind = np.logical_and(y_pred < n_labels, y_true < n_labels)
    if not np.all(ind):
        y_pred = y_pred[ind]
        y_true = y_true[ind]
        # also eliminate weights of eliminated items
        sample_weight = sample_weight[ind]

    # Choose the accumulator dtype to always have high precision
    dtype = np.int64

    cm = coo_matrix(
        (sample_weight, (y_true, y_pred)),
        shape=(n_labels, n_labels),
        dtype=dtype,
    ).toarray()

    with np.errstate(all="ignore"):
        if normalize == "true":
            cm = cm / cm.sum(axis=1, keepdims=True)
        elif normalize == "pred":
            cm = cm / cm.sum(axis=0, keepdims=True)
        elif normalize == "all":
            cm = cm / cm.sum()
        cm = np.nan_to_num(cm)

    return cm


def compute_confusion_matrix(
    predicted, ground_truth, ytick_labels=None, ground_truth_unlabled_is_unknown=False
) -> dict:

    if ytick_labels is None:
        ytick_labels = []

    df_gt = DataFrame(
        [
            "Unlabeled"
            for _ in range(
                max(
                    ground_truth[-1]["capture_sample_sequence_end"],
                    predicted[-1]["capture_sample_sequence_end"],
                )
                + 1
            )
        ],
        columns=["label_value"],
    )

    for segment in ground_truth:

        df_gt.iloc[
            segment["capture_sample_sequence_start"] : segment[
                "capture_sample_sequence_end"
            ]
        ] = segment["label_value"]

    for segment in predicted:
        # print(segment["capture_sample_sequence_start"])
        # print(segment["capture_sample_sequence_end"])
        segment["y_predicted"] = df_gt.iloc[
            segment["capture_sample_sequence_start"] : segment[
                "capture_sample_sequence_end"
            ]
        ]["label_value"].mode()[0]

    combined = DataFrame(predicted)
    if ground_truth_unlabled_is_unknown == False:
        combined = combined[combined["y_predicted"] != "Unlabeled"]

    # TODO: Discuss a better way to handle this situation,  for now I think the best method is to return confusion matrix
    # if not set(combined["Label_Value"].values) <= set(ytick_labels):
    #    return get_empty_confusion_matrix(ytick_labels)

    ytick_labels = list(
        set(combined["label_value"].values.astype(str)).union(ytick_labels)
    )

    ytick_labels = sorted(
        list(set(ytick_labels).union(set(combined["y_predicted"].values.astype(str))))
    )

    cm_array = confusion_matrix(
        y_true=combined["label_value"].astype(str),
        y_pred=combined["y_predicted"].astype(str),
        labels=ytick_labels,
    )

    df_cm = DataFrame(cm_array, index=ytick_labels, columns=ytick_labels).T

    df_cm["Total"] = df_cm.T.sum(axis=0)

    return df_cm


def plot_segments_labels(segments, labels=None, figsize=(30, 8), title=None):

    plt.figure(figsize=figsize)
    currentAxis = plt.gca()

    cmap = plt.cm.rainbow

    if labels is None:
        labels = sorted(segments.label_value.unique().tolist())

    delta = 1 / len(labels)
    label_float = np.arange(0, 1, delta)
    label_float[-1] = 1.0

    label_colors = {labels[index]: cmap(x) for index, x in enumerate(label_float)}
    label_legend = [Line2D([0], [0], color=cmap(x), lw=4) for x in label_float] + [
        Line2D([0], [0], color="white", lw=4)
    ]

    x_lim_end = 0
    for _, seg in segments.iterrows():
        y_origin = 0
        x_origin = seg["capture_sample_sequence_start"]
        x_final = (
            seg["capture_sample_sequence_end"] - seg["capture_sample_sequence_start"]
        )
        y_final = len(labels)

        currentAxis.add_artist(
            plt.Rectangle(
                (x_origin, y_origin),
                x_final,
                y_final,
                alpha=0.7,
                color=label_colors[seg["label_value"]],
            )
        )
        x_lim_end = seg["capture_sample_sequence_end"]

    currentAxis.legend(label_legend, labels + [""], loc=1)
    plt.xlim((0, x_lim_end))
    plt.title(title)
