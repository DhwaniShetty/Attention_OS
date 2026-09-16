from agent import AttentionAgent


agent = AttentionAgent()


print("\nCURRENT PREFERENCE")
print(
    "Social:",
    agent.user_preferences["social"]
)


print("\nAGENT DECISION")

result = agent.process_event(
    "deep_work",
    90,
    "social"
)

print(
    "Decision:",
    result["decision"]
)


print("\nUSER FEEDBACK")

print(
    "User says: ALLOW"
)


new_value = agent.learn(
    "social",
    "allow"
)


print(
    "New social importance:",
    new_value
)


print("\nNEXT DECISION")

result = agent.process_event(
    "deep_work",
    90,
    "social"
)


print(
    "Decision:",
    result["decision"]
)
