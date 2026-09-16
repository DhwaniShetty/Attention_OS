from flask import Flask, render_template, request, jsonify
from agent.attention_state import AttentionState
from agent.decision_engine import DecisionEngine
from agent.perception import parse_incoming_event
import time

app = Flask(__name__)
decision_engine = DecisionEngine()

# Global state to simulate the agent's current understanding of the user
current_activity = "Software Development"
focus_start_time = time.time()
manual_override = None

def get_current_focus_duration_mins():
    return (time.time() - focus_start_time) / 60

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/state', methods=['GET'])
def get_state():
    duration = get_current_focus_duration_mins()
    state = AttentionState.calculate_state(current_activity, duration, manual_override)
    
    return jsonify({
        "activity": current_activity,
        "duration_mins": round(duration, 2),
        "state": state,
        "is_manual": manual_override is not None
    })

@app.route('/api/set_state', methods=['POST'])
def set_state():
    global current_activity, focus_start_time, manual_override
    data = request.json
    
    if "activity" in data:
        current_activity = data["activity"]
    if "reset_timer" in data and data["reset_timer"]:
        focus_start_time = time.time()
    if "override" in data:
        manual_override = data["override"] # e.g., "DEEP_FOCUS" or None
        
    return jsonify({"status": "success"})

@app.route('/api/event', methods=['POST'])
def handle_event():
    raw_event = request.json
    parsed_event = parse_incoming_event(raw_event)
    
    duration = get_current_focus_duration_mins()
    user_state = AttentionState.calculate_state(current_activity, duration, manual_override)
    
    result = decision_engine.process_event(parsed_event, user_state)
    return jsonify(result)

@app.route('/api/feedback', methods=['POST'])
def handle_feedback():
    data = request.json
    source = data.get("source")
    sender = data.get("sender_name")
    user_action = data.get("user_action")
    agent_decision = data.get("agent_decision")
    
    decision_engine.learning_engine.update_preference(source, sender, user_action, agent_decision)
    return jsonify({"status": "success"})

@app.route('/api/learning', methods=['GET'])
def get_learning():
    return jsonify(decision_engine.learning_engine.preferences)
    
@app.route('/api/reset_learning', methods=['POST'])
def reset_learning():
    decision_engine.learning_engine.reset()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
