import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import OneHotEncoder

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

import joblib


# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv(
    "attention_training_data.csv"
)


# ======================================
# FEATURES & TARGET
# ======================================

X = df[
    [
        "activity",
        "focus_duration",
        "typing_activity",
        "mouse_activity",
        "notification_count"
    ]
]


y = df[
    "attention_state"
]


# ======================================
# TRAIN / TEST SPLIT
# ======================================

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )
)


# ======================================
# PREPROCESSING
# ======================================

categorical_features = [
    "activity"
]


numeric_features = [
    "focus_duration",
    "typing_activity",
    "mouse_activity",
    "notification_count"
]


preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),

        (
            "numeric",
            "passthrough",
            numeric_features
        )

    ]

)


# ======================================
# MODEL
# ======================================

model = RandomForestClassifier(

    n_estimators=150,

    random_state=42,

    max_depth=8

)


# ======================================
# PIPELINE
# ======================================

pipeline = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "classifier",
            model
        )

    ]

)


# ======================================
# TRAIN
# ======================================

pipeline.fit(
    X_train,
    y_train
)


# ======================================
# EVALUATE
# ======================================

predictions = pipeline.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print(
    f"\nModel accuracy: {accuracy:.2f}"
)


# ======================================
# SAVE
# ======================================

joblib.dump(
    pipeline,
    "attention_model.joblib"
)


print(
    "\nModel saved as attention_model.joblib"
)
