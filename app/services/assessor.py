
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CarAssessment:
    score: float
    flags: Dict[str, Any]

WEIGHTS = {
    "price_vs_market": 0.2,
    "mileage_vs_year": 0.1,
    "vin_present": 0.05,
    "photos_quality": 0.05,
    "owner_words": 0.05,
    "region_consistency": 0.05,
    "accident_risk": 0.15,
    "duplicate_listing": 0.05,
    "service_history_hint": 0.05,
    "ownership_count": 0.05,
    "engine_flags": 0.05,
    "gearbox_flags": 0.05,
    "taxi_usage_risk": 0.03,
    "tuning_risk": 0.02,
    "photo_dents": 0.03,
    "airbag_light": 0.02,
    "paint_mismatch": 0.02,
    "stolen_phrases": 0.02,
    "doc_red_flags": 0.03,
    "seller_reputation": 0.03,
}

def assess_car(car: dict) -> CarAssessment:
    f = {}
    f["vin_present"] = 1.0 if car.get("vin") else 0.0
    f["mileage_vs_year"] = _mileage_score(car.get("mileage"), car.get("year"))
    f["price_vs_market"] = _price_score(car.get("price"), car.get("brand"), car.get("model"), car.get("year"))
    f["photos_quality"] = 0.6 if car.get("photos") else 0.1
    f["owner_words"] = _nlp_flags(car.get("description",""))
    f["region_consistency"] = 0.7
    f["accident_risk"] = 0.8
    f["duplicate_listing"] = 0.6
    f["service_history_hint"] = 0.5
    f["ownership_count"] = 0.5
    f["engine_flags"] = 0.6
    f["gearbox_flags"] = 0.6
    f["taxi_usage_risk"] = 0.5
    f["tuning_risk"] = 0.5
    f["photo_dents"] = 0.5
    f["airbag_light"] = 0.5
    f["paint_mismatch"] = 0.5
    f["stolen_phrases"] = 0.5
    f["doc_red_flags"] = 0.5
    f["seller_reputation"] = 0.5

    score = sum(f[k] * w for k, w in WEIGHTS.items())
    return CarAssessment(score=round(score * 100, 2), flags=f)

def _mileage_score(mileage: int | None, year: int | None) -> float:
    if not mileage or not year:
        return 0.3
    age = max(1, 2025 - int(year))
    avg = 15000 * age
    ratio = max(0.0, min(1.5, avg / max(1, mileage)))
    return min(1.0, ratio / 1.5)

def _price_score(price: float | None, brand: str | None, model: str | None, year: int | None) -> float:
    if not price:
        return 0.3
    return 0.6 if 3000 < price < 100000000 else 0.4

def _nlp_flags(text: str) -> float:
    red = ["срочно", "небольшой удар", "надо сделать", "без торга"]
    penalty = any(w in text.lower() for w in red)
    return 0.4 if penalty else 0.7
