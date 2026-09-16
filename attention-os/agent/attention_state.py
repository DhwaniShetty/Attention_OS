class AttentionState:
    STATES = {
        "AVAILABLE": {"threshold": 20, "name": "🟢 Available"},
        "MODERATE_FOCUS": {"threshold": 50, "name": "🟡 Moderate Focus"},
        "DEEP_FOCUS": {"threshold": 70, "name": "🔴 Deep Focus"},
        "OVERLOAD": {"threshold": 90, "name": "🟣 Cognitive Overload"},
    }

    @staticmethod
    def calculate_state(activity, focus_duration_mins, manual_override=None):
        if manual_override:
            return AttentionState.STATES.get(manual_override, AttentionState.STATES["AVAILABLE"])
            
        if focus_duration_mins >= 180:
            return AttentionState.STATES["OVERLOAD"]
        elif focus_duration_mins >= 45:
            return AttentionState.STATES["DEEP_FOCUS"]
        elif focus_duration_mins >= 15:
            return AttentionState.STATES["MODERATE_FOCUS"]
        else:
            return AttentionState.STATES["AVAILABLE"]
