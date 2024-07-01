from copy import deepcopy
import numpy as np

from dataset import get_train_test_matrices
from evaluation import evaluate, recall, ndcg
from models import EASE, AbsEASE


def hyperparameter_selection(dataset, l2s, metric, k, target_value=None):
    train_X, test_X_pos, _, test_y = get_train_test_matrices(dataset, "val", target_ratio=0.8)

    best = {
        "EASE": (None, 0.),
        "AbsEASE": (None, 0.),
    }

    for l2 in l2s:
        print(f"L2 {l2}")
        ease = EASE(l2)  # train EASE
        ease.fit(train_X)
        absease = AbsEASE(l2)
        absease.B = deepcopy(ease.B)  # just copy EASE and modify the weights
        absease.B.data *= np.sign(absease.B.data)

        for model_name, model in [("EASE", ease), ("AbsEASE", absease)]:
            print(model_name)
            scores = model.recommend(test_X_pos)
            topk_ids = np.argsort(-scores, axis=1)[:, :k]  # want highest scored items

            metrics = evaluate(topk_ids, test_y, metric, target_value=target_value)
            print(f"ndcg @ {k}: {np.mean(metrics)} +- {np.std(metrics) / np.sqrt(len(metrics))}")

            if np.mean(metrics) > best[model_name][1]:
                best[model_name] = (l2, np.mean(metrics))

        print()

    print(f"Best L2: EASE {best['EASE'][0]}, AbsEASE {best['AbsEASE'][0]}")
    return best


def train_and_test_on_split(models, dataset, split, ks, results_dict=None):
    print(f"Split {split}")
    train_X, test_X_pos, test_X, test_y = get_train_test_matrices(dataset, split, target_ratio=0.8)

    max_k = max(ks)

    for model_name, model_class, l2 in models:
        print(model_name)
        model = model_class(l2)
        model.fit(train_X)
        
        for input_type, input_matrix in [("pos_inputs", test_X_pos), ("pos_neg_inputs", test_X)]:
            print(input_type)
            scores = model.recommend(input_matrix)
            top_max_k_ids = np.argsort(-scores, axis=1)[:, :max_k]  # want highest scored items
            for k in ks:
                top_k_ids = top_max_k_ids[:, :k]
                recall_liked_k = evaluate(top_k_ids, test_y, recall, target_value=1.)
                recall_disliked_k = evaluate(top_k_ids, test_y, recall, target_value=-1.)
                ndcg_k = evaluate(top_k_ids, test_y, ndcg)

                print(f"recall_liked @ {k}: {np.mean(recall_liked_k)} +- {np.std(recall_liked_k) / np.sqrt(len(recall_liked_k))}")
                print(f"recall_disliked @ {k}: {np.mean(recall_disliked_k)} +- {np.std(recall_disliked_k) / np.sqrt(len(recall_disliked_k))}")
                print(f"ndcg @ {k}: {np.mean(ndcg_k)} +- {np.std(ndcg_k) / np.sqrt(len(ndcg_k))}")

                if results_dict is not None:
                    results_dict[model_name][input_type][k]["recall_liked_values"] = recall_liked_k
                    results_dict[model_name][input_type][k]["recall_disliked_values"] = recall_disliked_k
                    results_dict[model_name][input_type][k]["ndcg_values"] = ndcg_k

                    results_dict[model_name][input_type][k]["recall_liked"] = (np.mean(recall_liked_k), np.std(recall_liked_k) / np.sqrt(len(recall_liked_k)))
                    results_dict[model_name][input_type][k]["recall_disliked"] = (np.mean(recall_disliked_k), np.std(recall_disliked_k) / np.sqrt(len(recall_disliked_k)))
                    results_dict[model_name][input_type][k]["ndcg"] = (np.mean(ndcg_k), np.std(ndcg_k) / np.sqrt(len(ndcg_k)))

                print()
            print()
        print()
        
    print("-------------------------------------------")
    

def run_test(models, dataset, ks):
    results_dict = {
        model_name: {
            "pos_inputs": {
                k: {
                    "recall_liked": (None, None),
                    "recall_disliked": (None, None),
                    "ndcg": (None, None),
                } for k in ks
            },
            "pos_neg_inputs": {
                k: {
                    "recall_liked": (None, None),
                    "recall_disliked": (None, None),
                    "ndcg": (None, None),
                } for k in ks
            },
        } for model_name, _, _ in models
    }
    
    train_and_test_on_split(models, dataset, "test", ks, results_dict)

    return results_dict
