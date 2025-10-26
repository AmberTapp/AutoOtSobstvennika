
from typing import Dict, List

def match_for_buyer(buyer: Dict, cars: List[Dict], top: int = 5) -> List[Dict]:
    def score(car: Dict) -> float:
        s = 0.0
        if buyer.get("budget_min") and car["price"] < buyer["budget_min"]: s -= 1
        if buyer.get("budget_max") and car["price"] > buyer["budget_max"]: s -= 1
        if buyer.get("brands") and car["brand"] not in buyer["brands"]: s -= 0.5
        if buyer.get("regions") and car["region"] not in buyer["regions"]: s -= 0.5
        s += car.get("score", 50)/100
        return s
    ranked = sorted(cars, key=score, reverse=True)
    return ranked[:top]
