import json
import os
import joblib
import pandas as pd


class AttentionAgent:

    def __init__(self):

        self.preferences_file = "user_preferences.json"

        self.default_preferences = {
            "emergency": 100,
            "work": 80,
            "calendar": 80,
            "college": 60,
            "personal": 50,
            "social": 20,
            "advertisement": 5
        }

        self.user_preferences = self.load_preferences()

        self.ml_model = joblib.load(
            "attention_model.joblib"
        )


    # ==========================================
    # LOAD PREFERENCES
    # ==========================================

    def load_preferences(self):

        if os.path.exists(self.preferences_file):

            with open(
                self.preferences_file,
                "r"
            ) as file:

                return json.load(file)

        return self.default_preferences.copy()


    # ==========================================
    # SAVE PREFERENCES
    # ==========================================

    def save_preferences(self):

        with open(
            self.preferences_file,
            "w"
        ) as file:

            json.dump(
                self.user_preferences,
                file,
                indent=4
            )


    # ==========================================
    # ESTIMATE ATTENTION STATE
    # ==========================================

    def calculate_attention_state(
        self,
        activity,
        focus_duration
    ):

        if (
            activity == "deep_work"
            and focus_duration >= 60
        ):

            return "DEEP_FOCUS"


        elif activity == "deep_work":

            return "FOCUS"


        elif activity == "meeting":

            return "UNAVAILABLE"


        elif activity == "idle":

            return "AVAILABLE"


        else:

            return "MODERATE"


    # ==========================================
    # CALCULATE NOTIFICATION IMPORTANCE
    # ==========================================

    def calculate_importance(
        self,
        notification_type
    ):

        return self.user_preferences.get(
            notification_type,
            30
        )


    # ==========================================
    # INTERRUPTION COST
    # ==========================================

    def calculate_interruption_cost(
        self,
        attention_state
    ):

        costs = {

            "DEEP_FOCUS": 90,

            "FOCUS": 70,

            "MODERATE": 40,

            "UNAVAILABLE": 85,

            "AVAILABLE": 10

        }

        return costs.get(
            attention_state,
            50
        )


    # ==========================================
    # DECISION ENGINE
    # ==========================================

    def make_decision(
        self,
        attention_state,
        importance,
        interruption_cost
    ):

        # Critical events always pass

        if importance >= 90:

            return "ALLOW"


        # Deep focus

        if attention_state == "DEEP_FOCUS":

            if importance >= 70:

                return "ALLOW"

            elif importance >= 40:

                return "DELAY"

            else:

                return "BLOCK"


        # Focus

        if attention_state == "FOCUS":

            if importance >= 60:

                return "ALLOW"

            elif importance >= 30:

                return "DELAY"

            else:

                return "BLOCK"


        # Meeting

        if attention_state == "UNAVAILABLE":

            if importance >= 80:

                return "ALLOW"

            return "DELAY"


        # Available

        if attention_state == "AVAILABLE":

            return "ALLOW"


        # Moderate

        if importance >= interruption_cost:

            return "ALLOW"

        elif importance >= 30:

            return "DELAY"

        else:

            return "BLOCK"


    # ==========================================
    # CONFIDENCE
    # ==========================================

    def calculate_confidence(
        self,
        importance,
        interruption_cost
    ):

        difference = abs(
            importance - interruption_cost
        )

        confidence = 50 + difference / 2

        return min(
            99,
            round(confidence)
        )


    # ==========================================
    # REASONING
    # ==========================================

    def generate_reason(
        self,
        attention_state,
        importance,
        interruption_cost,
        decision
    ):

        if decision == "BLOCK":

            return (
                f"You are in {attention_state.replace('_', ' ').lower()} "
                f"and the notification importance ({importance}) is lower "
                f"than the interruption cost ({interruption_cost}). "
                "The agent blocked it to protect your focus."
            )


        elif decision == "DELAY":

            return (
                f"You are in {attention_state.replace('_', ' ').lower()} "
                f"and the notification has moderate importance ({importance}). "
                "The agent delayed it to reduce unnecessary interruption."
            )


        elif decision == "ALLOW":

            return (
                f"The notification importance ({importance}) is high enough "
                f"to justify interrupting your current state "
                f"({attention_state.replace('_', ' ').lower()}). "
                "The agent allowed it."
            )


        return "Decision generated by the AttentionOS decision engine."


    # ==========================================
    # ML INFERENCE
    # ==========================================

    def predict_attention_state(
        self,
        activity,
        focus_duration,
        typing_activity,
        mouse_activity,
        notification_count
    ):

        features = pd.DataFrame([{

            "activity":
                activity,

            "focus_duration":
                focus_duration,

            "typing_activity":
                typing_activity,

            "mouse_activity":
                mouse_activity,

            "notification_count":
                notification_count

        }])


        prediction = self.ml_model.predict(
            features
        )[0]


        probabilities = (
            self.ml_model.predict_proba(
                features
            )[0]
        )


        confidence = (
            max(probabilities) * 100
        )


        return (
            prediction,
            round(confidence)
        )


    # ==========================================
    # MAIN AGENT
    # ==========================================

    def process_event(
        self,
        activity,
        focus_duration,
        notification_type,
        typing_activity=70,
        mouse_activity=60,
        notification_count=3
    ):

        attention_state, ml_confidence = (
            self.predict_attention_state(
                activity,
                focus_duration,
                typing_activity,
                mouse_activity,
                notification_count
            )
        )


        importance = (
            self.calculate_importance(
                notification_type
            )
        )


        interruption_cost = (
            self.calculate_interruption_cost(
                attention_state
            )
        )


        decision = (
            self.make_decision(
                attention_state,
                importance,
                interruption_cost
            )
        )


        decision_confidence = (
            self.calculate_confidence(
                importance,
                interruption_cost
            )
        )


        reason = (
            self.generate_reason(
                attention_state,
                importance,
                interruption_cost,
                decision
            )
        )


        return {

            "activity": activity,

            "focus_duration": focus_duration,

            "attention_state":
                attention_state,

            "notification":
                notification_type,

            "importance":
                importance,

            "interruption_cost":
                interruption_cost,

            "base_preference":
                self.user_preferences.get(notification_type, 30),

            "decision":
                decision,

            "ml_confidence": ml_confidence,

            "decision_confidence":
                decision_confidence,

            "reason":
                reason
        }


    # ==========================================
    # LEARNING
    # ==========================================

    def learn(
        self,
        notification_type,
        user_feedback
    ):

        current_value = (
            self.user_preferences.get(
                notification_type,
                30
            )
        )


        if user_feedback == "allow":

            current_value += 10


        elif user_feedback == "block":

            current_value -= 10


        current_value = max(
            0,
            min(
                100,
                current_value
            )
        )


        self.user_preferences[
            notification_type
        ] = current_value


        self.save_preferences()


        return current_value
