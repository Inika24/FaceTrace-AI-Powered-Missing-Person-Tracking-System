import json
import re
from pages.helper import db_queries

def query_avinashi_ai(user_query: str, current_user: str = "inika") -> str:
    """
    AVINASHI-AI Conversational Police Command Assistant.
    Parses natural language queries and queries live PostgreSQL/SQLite database records.
    """
    query = user_query.lower().strip()

    if not query:
        return "👋 Hello Officer Inika! I am **AVINASHI-AI**, your Police Command Assistant. How can I assist you with case analytics, location tracking, or missing person records today?"

    # 1. Total Case Metrics Query
    if any(k in query for k in ["total", "how many cases", "count", "cases registered"]):
        found_cases = db_queries.get_registered_cases_count(current_user, "F")
        active_cases = db_queries.get_not_confirmed_registered_cases(current_user)
        total = len(found_cases) + len(active_cases)
        return (
            f"📊 **AVINASHI-AI Database Intelligence Report:**\n\n"
            f"• **Total Registered Cases:** `{total}`\n"
            f"• **Active Missing (NF):** `{len(active_cases)}`\n"
            f"• **Resolved / Found (F):** `{len(found_cases)}`\n"
            f"• **Station Jurisdiction:** Avinashi Police Station, Tiruppur"
        )

    # 2. City / Location Specific Queries
    cities = ["tiruppur", "avinashi", "chennai", "coimbatore", "delhi", "mumbai", "bengaluru", "noida", "hyderabad", "kolkata"]
    for city in cities:
        if city in query:
            counts = db_queries.get_case_counts_by_city()
            city_data = counts.get(city.capitalize()) or counts.get(city.upper()) or counts.get(city)
            if city_data:
                return (
                    f"📍 **Jurisdiction Intelligence for {city.capitalize()}:**\n\n"
                    f"• **Active Unresolved Cases:** `{city_data['not_found']}`\n"
                    f"• **Resolved Cases:** `{city_data['found']}`\n"
                    f"• **Total Volume:** `{city_data['found'] + city_data['not_found']}`"
                )
            else:
                return f"📍 **Location Search:** Currently no cases registered under **{city.capitalize()}** in the active database."

    # 3. Search by Birthmark / Distinguishing Features
    if any(k in query for k in ["birthmark", "mark", "mole", "scar", "tattoo", "feature"]):
        cases = db_queries.get_not_confirmed_registered_cases(current_user)
        matches = []
        for c in cases:
            if c.birth_marks and any(w in c.birth_marks.lower() for w in query.split()):
                matches.append(f"• **{c.name}** (ID: `{c.id[:8]}`) — Marks: *{c.birth_marks}*")
        if matches:
            return "🔍 **Matching Distinguishing Feature Records:**\n\n" + "\n".join(matches)
        else:
            return "ℹ️ **Feature Search Complete:** No active missing cases match the specific feature terms in your query."

    # 4. Officer / Station Info Query
    if any(k in query for k in ["officer", "who am i", "station", "jurisdiction", "inika"]):
        return (
            "👮 **Station Officer Profile & System Info:**\n\n"
            "• **Officer Name:** Inika B\n"
            "• **Role:** Command Center Admin\n"
            "• **Station:** Avinashi Police Station\n"
            "• **Jurisdiction:** Tiruppur District, Tamil Nadu\n"
            "• **Database Backend:** Live Neon Cloud PostgreSQL Engine"
        )

    # 5. Technical AI Pipeline Explanation
    if any(k in query for k in ["how it works", "technical", "algorithm", "mediapipe", "knn", "vector", "mesh", "accuracy"]):
        return (
            "🧠 **AVINASHI-AI Technical Core Architecture:**\n\n"
            "1. **Facial Extraction:** MediaPipe 3D Neural Network extracts **468 landmark coordinates** per face.\n"
            "2. **Vector Space Embedding:** Normalizes 3D coordinates into a $1404$-dimensional geometric feature vector.\n"
            "3. **Similarity Classification:** K-Nearest Neighbors (KNN) evaluates L2 Euclidean Norm distance.\n"
            "4. **Matching Threshold:** Distances $\\le 3.0$ trigger an automatic status update to *Found* with instant alerts!"
        )

    # 6. Default Helpful Fallback Response
    return (
        f"🤖 **AVINASHI-AI Command Assistant:**\n\n"
        f"I received your query: *'{user_query}'*.\n\n"
        f"I can help you analyze live database records, search by location, query distinguishing features, or explain system algorithms. "
        f"Try asking:\n"
        f"• *'How many cases are registered in Tiruppur?'*\n"
        f"• *'Show total active cases count'*\n"
        f"• *'Explain the KNN AI facial mesh algorithm'*\n"
        f"• *'Show station officer info'*"
    )
