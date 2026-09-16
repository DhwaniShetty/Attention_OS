import os
import json

PREFERENCES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'user_preferences.json')

class LearningEngine:
    def __init__(self):
        self.preferences = self.load_preferences()

    def load_preferences(self):
        if not os.path.exists(PREFERENCES_FILE):
            os.makedirs(os.path.dirname(PREFERENCES_FILE), exist_ok=True)
            with open(PREFERENCES_FILE, 'w') as f:
                json.dump({}, f)
            return {}
        with open(PREFERENCES_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save_preferences(self):
        os.makedirs(os.path.dirname(PREFERENCES_FILE), exist_ok=True)
        with open(PREFERENCES_FILE, 'w') as f:
            json.dump(self.preferences, f, indent=4)

    def get_preference_score(self, source, sender):
        """Get learned modifier for a specific source and sender combo."""
        key = f"{source}::{sender}"
        return self.preferences.get(key, 0)

    def update_preference(self, source, sender, user_action, agent_decision):
        """
        Update the learned preference based on user feedback.
        If agent blocked, but user allowed -> add +5
        If agent allowed, but user dismissed without reading (if we had that data) -> subtract -5
        """
        key = f"{source}::{sender}"
        current_score = self.preferences.get(key, 0)
        
        if agent_decision == "BLOCK" and user_action == "ALLOW":
            current_score += 5
        elif agent_decision == "ALLOW" and user_action == "DISMISS":
            current_score -= 5
            
        self.preferences[key] = current_score
        self.save_preferences()
        
    def reset(self):
        self.preferences = {}
        self.save_preferences()
