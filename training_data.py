import pandas as pd


data = [

    # activity, focus_duration, typing, mouse, notifications, label

    ["deep_work", 90, 95, 80, 1, "DEEP_FOCUS"],
    ["deep_work", 80, 90, 75, 1, "DEEP_FOCUS"],
    ["deep_work", 70, 85, 70, 2, "DEEP_FOCUS"],
    ["deep_work", 60, 80, 65, 2, "DEEP_FOCUS"],
    ["deep_work", 55, 75, 60, 3, "FOCUS"],

    ["deep_work", 45, 70, 60, 4, "FOCUS"],
    ["deep_work", 40, 65, 55, 5, "FOCUS"],
    ["deep_work", 30, 60, 50, 5, "FOCUS"],

    ["moderate", 30, 50, 45, 8, "MODERATE"],
    ["moderate", 25, 45, 40, 10, "MODERATE"],
    ["moderate", 20, 40, 35, 12, "MODERATE"],
    ["moderate", 15, 35, 30, 15, "MODERATE"],

    ["idle", 0, 5, 5, 15, "AVAILABLE"],
    ["idle", 2, 10, 10, 12, "AVAILABLE"],
    ["idle", 5, 15, 15, 10, "AVAILABLE"],
    ["idle", 10, 20, 20, 8, "AVAILABLE"],

    ["meeting", 30, 20, 15, 3, "UNAVAILABLE"],
    ["meeting", 45, 15, 10, 2, "UNAVAILABLE"],
    ["meeting", 60, 10, 5, 1, "UNAVAILABLE"],

]


columns = [

    "activity",
    "focus_duration",
    "typing_activity",
    "mouse_activity",
    "notification_count",
    "attention_state"

]


df = pd.DataFrame(
    data,
    columns=columns
)


df.to_csv(
    "attention_training_data.csv",
    index=False
)


print("Training dataset created.")

print(
    df.head()
)

print(
    "\nDataset size:",
    len(df)
)
