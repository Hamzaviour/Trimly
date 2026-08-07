"""
Trimly AI — Churn Prevention Agent
Calculates customer churn risk scores and triggers automated winback campaigns (WhatsApp / AI Call).
"""
import math
from datetime import datetime, timezone
from typing import List, Dict, Any


def calculate_churn_risk(
    last_visit_days: int,
    avg_visit_frequency_days: int = 21,
    total_visits: int = 1,
) -> float:
    """
    Calculate customer churn risk score (0.0 to 1.0).
    
    Formula:
    overdue_ratio = last_visit_days / avg_visit_frequency_days
    """
    if total_visits == 0:
        return 0.0  # New lead
        
    overdue_ratio = last_visit_days / max(1, avg_visit_frequency_days)
    
    if overdue_ratio < 1.0:
        return 0.1  # Low risk, customer on schedule
    elif overdue_ratio < 1.4:
        return 0.4  # Moderate risk, slightly late
    elif overdue_ratio < 2.0:
        return 0.75  # High risk, overdue for haircut
    else:
        return 0.95  # Churned / At Risk of leaving permanently


def generate_winback_offer(customer_name: str, churn_risk: float, favorite_service: str) -> Dict[str, Any]:
    """
    Generate personalized discount offer based on churn risk level.
    """
    if churn_risk >= 0.75:
        discount_percent = 20
        code = "WELCOME20"
        message_ur = f"السلام علیکم {customer_name} صاحب! ہم آپ کو مس کر رہے ہیں۔ آج ہی اپائنٹمنٹ لیں اور {discount_percent}٪ رعایت پائیں۔ پرومو کوڈ: {code}"
    else:
        discount_percent = 10
        code = "FRESH10"
        message_ur = f"السلام علیکم {customer_name} صاحب! آپ کا {favorite_service} ڈیو ہو چکا ہے۔ اپائنٹمنٹ بک کریں اور ۱۰٪ رعایت حاصل کریں۔"

    return {
        "customer_name": customer_name,
        "churn_risk": churn_risk,
        "discount_percent": discount_percent,
        "coupon_code": code,
        "message_ur": message_ur,
        "recommended_channel": "AI_CALL" if churn_risk >= 0.75 else "WHATSAPP",
    }
