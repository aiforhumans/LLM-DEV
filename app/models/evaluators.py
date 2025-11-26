from typing import Any, Dict

def exact_match(prediction: str, reference: str) -> float:
    return 1.0 if prediction.strip() == reference.strip() else 0.0

def contains_match(prediction: str, reference: str) -> float:
    return 1.0 if reference.strip().lower() in prediction.strip().lower() else 0.0

def length_ratio(prediction: str, reference: str) -> float:
    len_pred = len(prediction)
    len_ref = len(reference)
    if len_ref == 0:
        return 0.0
    return min(len_pred / len_ref, len_ref / len_pred)

BUILTIN_EVALUATORS = {
    "exact_match": exact_match,
    "contains_match": contains_match,
    "length_ratio": length_ratio
}
