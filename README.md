# 🧠 AttentionOS

### AI-Based Cognitive Environment Management Agent

AttentionOS is a context-aware intelligent agent designed to manage digital interruptions according to the user's estimated attention state.

Instead of treating every notification equally, AttentionOS observes digital interaction signals, estimates the user's current attention state using Machine Learning, evaluates the importance and interruption cost of an incoming notification, and autonomously decides whether to:

**ALLOW → DELAY → BLOCK**

The system also learns from user feedback to adapt notification preferences over time.

---

## 🚀 Project Overview

Modern digital environments continuously compete for human attention through notifications, messages, emails, social media, reminders, and other interruptions.

The problem is not simply the number of notifications — it is **whether a notification should interrupt the user at that particular moment**.

For example:

| User State | Notification | Agent Action |
|---|---|---|
| Deep Focus | Social notification | 🔴 BLOCK |
| Deep Focus | College notification | 🟡 DELAY |
| Deep Focus | Work notification | 🟢 ALLOW |
| Deep Focus | Emergency | 🟢 ALLOW |
| Available | Social notification | 🟢 ALLOW |

AttentionOS attempts to make these decisions automatically.

---

# 🎯 Objectives

The main objectives of AttentionOS are:

- Estimate the user's operational attention state.
- Detect whether the user is currently focused, moderately active, idle, or unavailable.
- Evaluate the importance of incoming notifications.
- Estimate the interruption cost of breaking the user's current state.
- Automatically decide whether to allow, delay, or block notifications.
- Explain the factors behind each decision.
- Learn from user feedback.
- Provide a real-time visualization of the agent's decisions and performance.

---

# 🤖 What Makes AttentionOS an Intelligent Agent?

AttentionOS follows the fundamental intelligent-agent cycle:

```text
PERCEIVE
   ↓
UNDERSTAND
   ↓
DECIDE
   ↓
ACT
   ↓
LEARN
   ↓
ADAPT
````

The agent:

1. **Perceives** observable digital interaction signals.
2. **Estimates** the user's current attention state.
3. **Evaluates** an incoming notification.
4. **Chooses** an action.
5. **Acts** by allowing, delaying, or blocking the interruption.
6. **Receives feedback** from the user.
7. **Learns** user-specific notification preferences.

---

# 🧠 Intelligent Agent Type

AttentionOS is a **Hybrid Intelligent Agent** combining three major characteristics:

### 1. Model-Based Agent

The system maintains an internal representation of the user's current operational context.

Example:

```text
Activity       → Deep Work
Focus Duration → 95 minutes
Typing         → High
Mouse Activity → High
Notifications  → Low
```

This information is used to estimate the user's current state.

---

### 2. Utility-Based Agent

The agent evaluates whether interrupting the user is worthwhile.

A conceptual utility function is:

```text
Utility =
Focus Benefit
+ Important Communication
- Unnecessary Interruptions
- Cognitive Overload
```

The agent compares:

```text
Notification Importance
        VS
Interruption Cost
```

before selecting an action.

---

### 3. Learning Agent

AttentionOS learns from user feedback.

For example:

```text
Initial Social Notification Importance
20

User repeatedly blocks social notifications

        ↓

Learned Preference

Social Notification Importance
20 → 10
```

This allows the agent to gradually adapt to individual preferences.

---

# 📐 PEAS Model

## Performance Measure

The agent can be evaluated using:

* Reduction of unnecessary interruptions
* Focus duration
* Important notification preservation
* Task completion
* Decision confidence
* User feedback
* Notification handling consistency

> In the current prototype, these metrics are demonstrated through simulated events and should not be interpreted as results from a real-world user study.

---

## Environment

The intended environment includes:

* Laptop / desktop
* Smartphone
* Applications
* Notification systems
* Calendar
* Digital workspace
* User interaction environment

---

## Actuators

The agent can conceptually perform actions such as:

* Allow notification
* Delay notification
* Block notification
* Activate focus mode
* Modify notification behavior
* Recommend a break

The current prototype demonstrates these actions through a simulated digital environment.

---

## Sensors

AttentionOS uses observable digital interaction signals such as:

* Current activity
* Focus duration
* Typing activity
* Mouse activity
* Notification count
* Notification type
* Time/context information

---

# 🏗️ System Architecture

```text
                    DIGITAL ENVIRONMENT
                           │
                           ▼
                    ┌──────────────┐
                    │    SENSORS   │
                    └──────┬───────┘
                           │
                           ▼
                    OBSERVABLE INPUTS
                           │
                           ▼
                 ┌────────────────────┐
                 │  ML ATTENTION       │
                 │  PREDICTOR          │
                 │  Random Forest      │
                 └──────────┬─────────┘
                            │
                            ▼
                    ATTENTION STATE
                            │
                            ▼
                 ┌────────────────────┐
                 │  DECISION ENGINE   │
                 │                    │
                 │ Importance         │
                 │ Interruption Cost  │
                 │ User Preferences   │
                 └──────────┬─────────┘
                            │
                 ┌──────────┼──────────┐
                 ▼          ▼          ▼
              ALLOW       DELAY      BLOCK
                 │          │          │
                 └──────────┼──────────┘
                            ▼
                    USER FEEDBACK
                            │
                            ▼
                    LEARNING MODULE
                            │
                            ▼
                  USER PREFERENCE MODEL
                            │
                            └───────────►
```

---

# 🤖 Machine Learning Component

AttentionOS uses a **Random Forest Classifier** to estimate the user's attention state.

### Input Features

The model uses:

```text
activity
focus_duration
typing_activity
mouse_activity
notification_count
```

### Output

The model predicts an attention state such as:

```text
AVAILABLE
MODERATE
FOCUS
DEEP_FOCUS
UNAVAILABLE
```

The model also produces a prediction confidence value based on its class probabilities.

---

# 📊 Important Note About the ML Model

The current prototype uses a **synthetically generated training dataset** to demonstrate the complete machine-learning pipeline.

Therefore:

> The model's current accuracy is a demonstration of the implemented ML pipeline and should not be interpreted as validated real-world accuracy.

A production version would require a significantly larger dataset collected under appropriate privacy, consent, and ethical constraints.

---

# ⚙️ Decision Engine

After estimating the user's attention state, AttentionOS evaluates the incoming notification.

The decision engine considers:

```text
Attention State
       +
Notification Importance
       +
Interruption Cost
       +
User Preferences
       ↓
Final Decision
```

### Example

```text
User State:
DEEP_FOCUS

Notification:
Social

Importance:
20 / 100

Interruption Cost:
90 / 100

Decision:
BLOCK
```

Another example:

```text
User State:
DEEP_FOCUS

Notification:
Emergency

Importance:
100 / 100

Interruption Cost:
90 / 100

Decision:
ALLOW
```

---

# 🔍 Explainable Decisions

AttentionOS does not only display the final action.

It also presents the factors used in the decision:

```text
Attention State      → DEEP_FOCUS
ML Confidence        → 94%
Notification         → SOCIAL
Importance           → 20
Interruption Cost    → 90
Final Decision       → BLOCK
```

Example explanation:

> "You are in deep focus and the notification has low importance compared with the estimated interruption cost. The agent blocked it to protect your focus."

This makes the system easier to understand and demonstrate.

---

# 🔄 Learning Mechanism

The user can provide feedback after an agent decision.

For example:

```text
Agent Decision
      ↓
BLOCK
      ↓
User Feedback
      ↓
User agrees
      ↓
Preference Updated
      ↓
Future decisions adapt
```

The prototype stores learned notification preferences in:

```text
user_preferences.json
```

---

# 🖥️ Dashboard

AttentionOS includes a Flask-based interactive dashboard.

The dashboard provides:

* Current attention state
* Focus score
* ML confidence
* Notification simulator
* Agent decision
* Notification importance
* Interruption cost
* Decision explanation
* User feedback
* Learning information
* Event history
* Performance analytics
* Live simulation

---

# 🧪 Simulation

The prototype includes a simulated stream of notification events.

Example:

```text
Deep Work + Social
        ↓
      BLOCK

Deep Work + College
        ↓
      DELAY

Deep Work + Work
        ↓
      ALLOW

Deep Work + Emergency
        ↓
      ALLOW
```

This allows the complete agent pipeline to be demonstrated without requiring privileged access to real notification systems.

---

# 📈 Performance Analytics

The dashboard tracks simulation-level metrics including:

* Total events
* Blocked events
* Delayed events
* Allowed events
* Critical events
* Average model confidence
* Simulation interruption-handling rate

The prototype's analytics describe **simulated behavior**, not validated human productivity improvements.

---

# 🛠️ Technology Stack

### Programming

* Python
* JavaScript
* HTML
* CSS

### AI / Machine Learning

* Scikit-learn
* Random Forest
* Pandas
* NumPy

### Backend

* Flask

### Model Persistence

* Joblib

### Frontend

* HTML
* CSS
* JavaScript

### Data

* CSV-based synthetic training dataset
* JSON-based user preference storage

---

# 📂 Project Structure

```text
Attention_OS/
│
├── agent.py
├── app.py
│
├── training_data.py
├── train_model.py
├── predict_attention.py
│
├── attention_training_data.csv
├── attention_model.joblib
│
├── user_preferences.json
│
├── learning_test.py
│
├── templates/
│   └── dashboard.html
│
├── static/
│   └── style.css
│
├── README.md
└── .gitignore
```

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/DhwaniShetty/Attention_OS.git
```

Move into the project directory:

```bash
cd Attention_OS
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install flask scikit-learn pandas numpy joblib
```

---

# ▶️ Running the Project

Start the Flask application:

```bash
python app.py
```

Then open the local address shown by Flask in your browser.

The dashboard provides the interactive AttentionOS interface.

---

# 🧠 Training the ML Model

To generate the synthetic training dataset:

```bash
python training_data.py
```

Train the Random Forest model:

```bash
python train_model.py
```

Test predictions:

```bash
python predict_attention.py
```

The trained model is saved as:

```text
attention_model.joblib
```

---

# 🌍 Real-Life Applications

AttentionOS can be extended to several real-world environments.

### 🎓 Students

Automatically reduce low-priority notifications during study sessions.

### 👨‍💻 Software Developers

Protect coding and debugging sessions from unnecessary interruptions.

### 🔬 Researchers

Prioritize important communication while maintaining long research sessions.

### 🏢 Professionals

Manage notifications according to meetings, work sessions, and availability.

### 🧑‍💼 Remote Workers

Adapt notification behavior based on working context.

### 🚗 High-Attention Environments

The underlying architecture could be adapted to systems where unnecessary information interruptions should be minimized.

---

# ✅ Advantages

* Context-aware notification management
* Machine-learning-based attention estimation
* Utility-based decision making
* Adaptive user preferences
* Explainable decisions
* Autonomous notification handling
* Real-time visualization
* Modular architecture
* Can be extended to multiple digital environments

---

# ⚠️ Limitations

The current prototype has several limitations:

1. The training dataset is synthetic.
2. The dataset is relatively small and requires real-world validation.
3. Attention state is estimated from observable digital signals rather than directly measuring human cognition.
4. The current prototype simulates notification events instead of integrating with every real notification platform.
5. Model performance may differ significantly with real-world users and environments.
6. A production implementation would require strong privacy and security mechanisms.
7. User preferences currently use a simple feedback-based learning mechanism.

---

# 🔮 Future Scope

Possible future improvements include:

* Real-time desktop activity sensing
* Integration with operating-system notification APIs
* Calendar and meeting integration
* Email and messaging prioritization
* Personalized ML models
* Larger real-world datasets
* Online learning
* Reinforcement learning
* Privacy-preserving local inference
* Smartphone integration
* Cross-device attention management
* More advanced explainability techniques
* Personalized interruption policies

---

# 🎓 Academic Context

**Project:** Self-Learning Activity – Artificial Intelligence

**Project Title:**

### AI Agent That Manages Human Attention

**System:**

### AttentionOS – AI-Based Cognitive Environment Management Agent

The project demonstrates concepts including:

* Intelligent Agents
* PEAS
* Model-Based Agents
* Utility-Based Agents
* Learning Agents
* Machine Learning
* Classification
* Decision Making
* Feedback-Based Learning
* Human-AI Interaction

---

# 👩‍💻 Author

**Dhwani Shetty**

Computer Engineering
Pillai College of Engineering

---

# 📌 Project Status

```text
AttentionOS v1.0
```

### Current status:

* ✅ Intelligent agent architecture
* ✅ Rule-based decision engine
* ✅ User feedback learning
* ✅ Flask backend
* ✅ Interactive dashboard
* ✅ Machine Learning attention predictor
* ✅ Random Forest model
* ✅ Explainable decisions
* ✅ Live event simulation
* ✅ Performance analytics
* ✅ GitHub project

---

# 📜 License

This project is developed as an academic prototype for educational and demonstration purposes.


