from .attention_state import AttentionState
from .learning import LearningEngine

class DecisionEngine:
    BASE_SCORES = {
        "emergency": 90,
        "phone_call": 90,
        "calendar": 80,
        "slack": 60,
        "whatsapp": 40,
        "instagram": 10,
        "twitter": 10,
        "system": 50
    }

    SENDER_MODIFIERS = {
        "vip": 30,
        "family": 30,
        "work": 20,
        "project_group": 20,
        "known": 0,
        "unknown": -20,
        "automated": -20
    }

    KEYWORD_MODIFIERS = {
        "emergency": 40,
        "urgent": 40,
        "asap": 40,
        "meeting": 20,
        "call": 20,
        "promo": -30,
        "discount": -30,
        "sale": -30
    }

    def __init__(self):
        self.learning_engine = LearningEngine()

    def calculate_importance(self, notification):
        source = notification.get("source", "").lower()
        sender_type = notification.get("sender_type", "known").lower()
        content = notification.get("content", "").lower()
        sender_name = notification.get("sender_name", "")

        # 1. Base Score
        base_score = self.BASE_SCORES.get(source, 30)

        # 2. Sender Modifier
        sender_mod = self.SENDER_MODIFIERS.get(sender_type, 0)

        # 3. Keyword Modifier
        keyword_mod = 0
        for keyword, mod in self.KEYWORD_MODIFIERS.items():
            if keyword in content:
                keyword_mod += mod

        # 4. Learned Preference Modifier
        learned_mod = self.learning_engine.get_preference_score(source, sender_name)

        final_score = base_score + sender_mod + keyword_mod + learned_mod
        
        # Cap score between 0 and 100
        return max(0, min(100, final_score))

    def process_event(self, notification, user_state):
        importance_score = self.calculate_importance(notification)
        threshold = user_state["threshold"]

        if importance_score >= threshold:
            decision = "ALLOW"
        elif importance_score >= (threshold - 20):
            decision = "DELAY"
        else:
            decision = "BLOCK"

        return {
            "notification": notification,
            "importance_score": importance_score,
            "threshold": threshold,
            "decision": decision
        }
