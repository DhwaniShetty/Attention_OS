import json
import os


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


    # -----------------------------------
    # LOAD USER PREFERENCES
    # -----------------------------------

    def load_preferences(self):

        if os.path.exists(self.preferences_file):

            with open(
                self.preferences_file,
                "r"
            ) as file:

                return json.load(file)

        return self.default_preferences.copy()


    # -----------------------------------
    # SAVE USER PREFERENCES
    # -----------------------------------

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


    # -----------------------------------
    # ATTENTION STATE
    # -----------------------------------

    def calculate_attention_state(
        self,
        activity,
        focus_duration
    ):

        if activity == "deep_work" and focus_duration >= 60:
            return "DEEP_FOCUS"

        elif activity == "deep_work":
            return "FOCUS"

        elif activity == "meeting":
            return "UNAVAILABLE"

        elif activity == "idle":
            return "AVAILABLE"

        else:
            return "MODERATE"


    # -----------------------------------
    # NOTIFICATION IMPORTANCE
    # -----------------------------------

    def calculate_importance(
        self,
        notification_type
    ):

        return self.user_preferences.get(
            notification_type,
            30
        )


    # -----------------------------------
    # DECISION ENGINE
    # -----------------------------------

    def make_decision(
        self,
        attention_state,
        importance
    ):

        if importance >= 90:

            return "ALLOW"

        elif attention_state == "DEEP_FOCUS":

            if importance >= 70:
                return "ALLOW"

            elif importance >= 40:
                return "DELAY"

            else:
                return "BLOCK"

        elif attention_state == "FOCUS":

            if importance >= 60:
                return "ALLOW"

            elif importance >= 30:
                return "DELAY"

            else:
                return "BLOCK"

        elif attention_state == "UNAVAILABLE":

            if importance >= 80:
                return "ALLOW"

            return "DELAY"

        else:

            return "ALLOW"


    # -----------------------------------
    # PROCESS EVENT
    # -----------------------------------

    def process_event(
        self,
        activity,
        focus_duration,
        notification_type
    ):

        attention_state = (
            self.calculate_attention_state(
                activity,
                focus_duration
            )
        )

        importance = (
            self.calculate_importance(
                notification_type
            )
        )

        decision = (
            self.make_decision(
                attention_state,
                importance
            )
        )

        return {

            "activity": activity,

            "focus_duration": focus_duration,

            "attention_state": attention_state,

            "notification": notification_type,

            "importance": importance,

            "decision": decision
        }


    # -----------------------------------
    # LEARNING
    # -----------------------------------

    def learn(
        self,
        notification_type,
        user_feedback
    ):

        current_value = self.user_preferences.get(
            notification_type,
            30
        )


        if user_feedback == "allow":

            current_value += 10


        elif user_feedback == "block":

            current_value -= 10


        current_value = max(
            0,
            min(100, current_value)
        )


        self.user_preferences[
            notification_type
        ] = current_value


        self.save_preferences()


        return current_value
