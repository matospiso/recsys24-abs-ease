from copy import deepcopy
import numpy as np

np.random.seed(12345)


def recall(topk_ids, true_ids, true_rel):
    hits = np.sum(np.isin(topk_ids, true_ids))
    total = len(true_ids)
    return hits/total


def dcg(topk_ids, true_ids, true_rel):
    k = len(topk_ids)
    mask = np.isin(topk_ids, true_ids)

    top_k_hits = topk_ids[mask]
    relevances = np.zeros_like(topk_ids, dtype=float)
    positions = np.array([np.where(true_ids == top_k_hits[i])[0][0] for i in range(len(top_k_hits))], dtype=int)
    relevances[mask] = true_rel[positions]

    discounts = np.log2(np.arange(2,k+2))
    metric = np.sum(
       relevances / discounts
    )
    return metric


def idcg(true_rel):
    positive_count = np.sum(true_rel == 1.)
    return np.sum(1/np.log2(np.arange(2,positive_count+2)))


def ndcg(topk_ids, true_ids, true_rel):
    d = dcg(topk_ids, true_ids, true_rel)
    i = idcg(true_rel)
    return d/i


def evaluate(topk_ids, true, metric, target_value=None):
    targets = deepcopy(true)
    if target_value is not None:
        targets.data *= targets.data == target_value  # evaluate on positive targets if target_value == 1. or on negative targets if target_value == -1.
        targets.eliminate_zeros()
    true_ids = [targets.indices[targets.indptr[i]:targets.indptr[i+1]] for i in range(targets.shape[0])]  # get column (item) indices of targets as a list of np.arrays
    true_rel = [targets.data[targets.indptr[i]:targets.indptr[i+1]] for i in range(targets.shape[0])]  # get relevance of targets as a list of np.arrays

    metrics = []
    for tk, ti, tr in zip(topk_ids, true_ids, true_rel):
        metrics.append(metric(tk, ti, tr))
    
    return metrics
