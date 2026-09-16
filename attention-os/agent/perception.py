# This module can be used to simulate incoming events from digital environment
def parse_incoming_event(raw_event):
    """
    Parses a raw event dictionary into a structured notification.
    """
    return {
        "id": raw_event.get("id"),
        "source": raw_event.get("source", "system"),
        "sender_name": raw_event.get("sender_name", "Unknown"),
        "sender_type": raw_event.get("sender_type", "known"),
        "content": raw_event.get("content", ""),
        "timestamp": raw_event.get("timestamp", "")
    }
