from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from agent import AttentionAgent


app = Flask(__name__)

agent = AttentionAgent()


@app.route("/")
def dashboard():

    return render_template(
        "dashboard.html"
    )


@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():
    data = request.json

    result = agent.process_event(
        activity=data.get("activity", "deep_work"),
        focus_duration=int(data.get("focus_duration", 60)),
        notification_type=data.get("notification", "social"),
        typing_activity=data.get("typing_activity", 70),
        mouse_activity=data.get("mouse_activity", 60),
        notification_count=data.get("notification_count", 3)
    )

    return jsonify(result)


@app.route(
    "/feedback",
    methods=["POST"]
)
def feedback():

    data = request.json

    notification = data.get(
        "notification"
    )

    feedback = data.get(
        "feedback"
    )


    new_value = agent.learn(
        notification,
        feedback
    )


    return jsonify({

        "notification":
            notification,

        "new_importance":
            new_value

    })


@app.route(
    "/preferences",
    methods=["GET"]
)
def preferences():

    return jsonify(
        agent.user_preferences
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )
