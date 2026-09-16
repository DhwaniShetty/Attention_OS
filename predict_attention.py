import pandas as pd

import joblib


model = joblib.load(
    "attention_model.joblib"
)


test_cases = pd.DataFrame([

    {
        "activity": "deep_work",
        "focus_duration": 95,
        "typing_activity": 92,
        "mouse_activity": 75,
        "notification_count": 1
    },

    {
        "activity": "moderate",
        "focus_duration": 20,
        "typing_activity": 40,
        "mouse_activity": 35,
        "notification_count": 12
    },

    {
        "activity": "idle",
        "focus_duration": 0,
        "typing_activity": 5,
        "mouse_activity": 5,
        "notification_count": 15
    }

])


predictions = model.predict(
    test_cases
)


probabilities = model.predict_proba(
    test_cases
)


for i, prediction in enumerate(
    predictions
):

    confidence = (
        max(probabilities[i]) * 100
    )


    print(
        "\n-------------------------"
    )


    print(
        "Predicted state:",
        prediction
    )


    print(
        "Confidence:",
        f"{confidence:.1f}%"
    )
