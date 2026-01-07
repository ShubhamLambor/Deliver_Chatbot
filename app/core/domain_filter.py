# app/core/domain_filter.py

def is_delivery_related(text: str) -> bool:
    """
    Enhanced domain filter to check if message is delivery-related.
    Supports English, Hindi, and Hinglish queries.
    """
    text = text.lower()

    valid_keywords = [
        # English - Delivery Operations
        "delivery", "order", "pickup", "drop", "restaurant", "food", "customer",
        "address", "location", "map", "late", "time", "cancel", "reject",
        "assigned", "active", "pending", "completed", "current", "next",

        # English - Financial
        "money", "earn", "earning", "earnings", "cash", "income", "paid", "payment",
        "wallet", "rupee", "salary", "payout", "balance", "summary", "total",
        "collection", "today", "daily", "weekly", "history", "received",

        # Hindi - Financial
        "paisa", "paise", "kamaya", "mila", "aaya", "bana", "kitna", "kitne",
        "aaj", "kal", "abhi",

        # Pickup & Restaurant Issues
        "closed", "shut", "delayed", "waiting", "ready", "preparation",
        "kitchen", "shop", "band", "khula", "tayar", "tyaar",

        # Delivery Issues
        "wrong", "incorrect", "unavailable", "unreachable", "responding",
        "switched off", "offline", "gate", "flat", "building",
        "galat", "nahi mil raha", "phone", "call",

        # Support & Issues
        "help", "support", "issue", "problem", "complain", "complaint",
        "contact", "care", "helpline", "manager", "escalate", "ticket",
        "hlp", "suport", "problm", "chahiye", "shikayat", "madad",

        # Navigation & App Usage
        "navigate", "navigation", "direction", "route", "maps",
        "app", "feature", "use", "kaise", "chalaye", "sikhna",

        # UI Elements & Screens
        "where", "see", "find", "check", "view", "show", "tab",
        "page", "screen", "button", "icon", "menu", "dikhao", "dekho",

        # Status & Tracking
        "status", "track", "update", "available", "online", "offline",

        # Hindi/Hinglish Common Words
        "kaha", "kahan", "kaise", "kitna", "nahi", "hai", "band",
        "khula", "chahiye", "koi", "milega", "hoga", "karna",

        # Order Actions
        "accept", "reject", "complete", "start", "finish", "mark",
        "swipe", "tap", "click", "press"
    ]

    # Check for any keyword match
    for word in valid_keywords:
        if word in text:
            return True

    # Allow short questions (likely delivery-related)
    question_words = ["how", "what", "where", "why", "when", "which",
                      "kya", "kaise", "kahan", "kab", "kaun", "kitna"]

    if len(text.split()) <= 5:  # Increased from 3 to 5 words
        for qword in question_words:
            if qword in text:
                return True

    return False
