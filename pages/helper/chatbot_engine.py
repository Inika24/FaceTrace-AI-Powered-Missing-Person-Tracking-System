import json
import re
from pages.helper import db_queries

def query_avinashi_ai(user_query: str, current_user: str = "inika") -> str:
    """
    AVINASHI-AI Conversational Police Command Assistant.
    Parses natural language queries and queries live PostgreSQL/SQLite database records.
    """
    query = user_query.lower().strip()
    words = re.findall(r'\w+', query)

    if not query:
        return (
            "👋 Hello Officer Inika! I am **AVINASHI-AI**, your Police Command Assistant. "
            "How can I assist you with case analytics, location tracking, or missing person records today?"
        )

    # 1. Greetings & Friendly Salutations
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "namaste", "vanakkam", "greetings", "hi there", "hey ai", "yo"]
    if any(query == g or query.startswith(g + " ") for g in greetings):
        return (
            "👋 **Hello Officer Inika! Welcome to the Avinashi Police Command Network.**\n\n"
            "I am **AVINASHI-AI**, your 24/7 Police Command Assistant. How can I help you today?\n\n"
            "**Here are quick questions you can ask me:**\n"
            "• 📊 *'Show total case analytics'*\n"
            "• 📍 *'How many cases in Tiruppur?'*\n"
            "• 🔍 *'Find missing person records'*\n"
            "• 🧠 *'How does 468 landmark mesh work?'*\n"
            "• 👮 *'Show station officer profile'*"
        )

    # 2. Identity, Capabilities & Assistance Overview
    identity_keys = ["who are you", "what is your name", "what can you do", "help", "capabilities", "features", "commands", "about"]
    if any(k in query for k in identity_keys):
        return (
            "🛡️ **AVINASHI-AI — Police Command Intelligence Assistant**\n\n"
            "I am an intelligent conversational assistant integrated directly into your station command portal.\n\n"
            "**My Core Capabilities:**\n"
            "1. 📁 **Live Database Intelligence:** Query active missing persons & resolved cases from Neon Cloud PostgreSQL.\n"
            "2. 📍 **Geographic Analytics:** Check case density in Tiruppur, Avinashi, Chennai, Coimbatore, Delhi, etc.\n"
            "3. 🔍 **Person & Feature Search:** Search records by name, birthmark, tattoo, scar, or tracking code.\n"
            "4. 🧠 **AI Architecture Insights:** Explain MediaPipe 468 3D landmark extraction & KNN similarity math.\n"
            "5. 🚔 **Station System Support:** Guide you through registration, CCTV crowd scanning, and age progression.\n\n"
            "Try typing any question in natural English!"
        )

    # 3. Gratitude & Politeness
    thanks_keys = ["thank", "thanks", "awesome", "great", "good job", "nice", "ok", "okay", "bye", "goodbye"]
    if any(k in query for k in thanks_keys):
        return (
            "You're very welcome, Officer Inika! 🛡️\n\n"
            "Always at your service for public safety and rapid case resolution. "
            "Let me know whenever you need further intelligence analysis!"
        )

    # 4. Total Case Metrics & System Summary
    metrics_keys = ["total", "how many cases", "count", "active missing", "found", "resolved", "statistics", "summary", "analytics", "metrics", "registered cases"]
    if any(k in query for k in metrics_keys):
        found_cases = db_queries.get_registered_cases_count(current_user, "F")
        active_cases = db_queries.get_not_confirmed_registered_cases(current_user)
        total = len(found_cases) + len(active_cases)
        rate = f"{(len(found_cases) / total * 100):.1f}%" if total > 0 else "0.0%"
        
        return (
            f"📊 **AVINASHI-AI Live Command Intelligence Report:**\n\n"
            f"• 📁 **Total Registered Cases:** `{total}`\n"
            f"• 🚨 **Active Missing (Searching):** `{len(active_cases)}`\n"
            f"• ✅ **Resolved / Found:** `{len(found_cases)}`\n"
            f"• 📈 **Overall Resolution Rate:** `{rate}`\n"
            f"• 🏛️ **Station Jurisdiction:** Avinashi Police Station, Tiruppur District\n"
            f"• ☁️ **Database Status:** Live Neon Cloud PostgreSQL Engine Connected"
        )

    # 5. Station / Officer Info
    officer_keys = ["officer", "who am i", "station", "jurisdiction", "inika", "profile", "admin"]
    if any(k in query for k in officer_keys):
        return (
            "👮 **Station Officer Profile & System Info:**\n\n"
            "• **Officer Name:** Inika B\n"
            "• **Role:** Command Center Admin\n"
            "• **Station:** Avinashi Police Station\n"
            "• **Jurisdiction:** Tiruppur District, Tamil Nadu\n"
            "• **AI Mesh Version:** MediaPipe 468 3D Vector Core v3.0\n"
            "• **Cloud Database:** Neon Cloud PostgreSQL Serverless"
        )

    # 6. City / Location Specific Queries
    cities = ["tiruppur", "avinashi", "chennai", "coimbatore", "delhi", "mumbai", "bengaluru", "noida", "hyderabad", "kolkata", "pune", "madurai", "salem", "trichy"]
    for city in cities:
        if city in query:
            counts = db_queries.get_case_counts_by_city()
            city_data = counts.get(city.capitalize()) or counts.get(city.upper()) or counts.get(city)
            
            # Also search active cases in this city for specific names
            active_cases = db_queries.get_not_confirmed_registered_cases(current_user)
            city_names = [f"• **{c.name}** (Age: {c.age}, Code: `{c.id[:8]}`)" for c in active_cases if c.city and city.lower() in c.city.lower()]
            
            if city_data:
                names_str = ("\n\n**Active Missing Persons in " + city.capitalize() + ":**\n" + "\n".join(city_names)) if city_names else ""
                return (
                    f"📍 **Jurisdiction Intelligence for {city.capitalize()}:**\n\n"
                    f"• **Active Unresolved Cases:** `{city_data['not_found']}`\n"
                    f"• **Resolved Cases:** `{city_data['found']}`\n"
                    f"• **Total Case Volume:** `{city_data['found'] + city_data['not_found']}`"
                    f"{names_str}"
                )
            elif city_names:
                return f"📍 **Active Cases in {city.capitalize()}:**\n\n" + "\n".join(city_names)
            else:
                return f"📍 **Location Search:** Currently no active missing cases registered under **{city.capitalize()}** in the live database."

    # 7. Search by Distinguishing Feature / Birthmark / Tattoo / Clothing
    feature_keys = ["birthmark", "mark", "mole", "scar", "tattoo", "feature", "beard", "glasses", "height", "cloth", "color"]
    if any(k in query for k in feature_keys):
        cases = db_queries.get_not_confirmed_registered_cases(current_user)
        matches = []
        for c in cases:
            if c.birth_marks:
                bm_lower = c.birth_marks.lower()
                if any(w in bm_lower for w in words if len(w) > 2):
                    matches.append(
                        f"• **{c.name}** (Age: {c.age}, {c.gender}) — Tracking Code: `{c.id[:8]}`\n"
                        f"  - *Marks:* {c.birth_marks}\n"
                        f"  - *City:* {c.city or 'Unspecified'}"
                    )
        if matches:
            return f"🔍 **Found {len(matches)} Matching Case Record(s) for Feature Search:**\n\n" + "\n\n".join(matches)
        else:
            return f"ℹ️ **Feature Search Complete:** No active missing cases currently match the specific physical terms in *'{user_query}'*."

    # 8. Search by Name / Individual Case Search
    search_triggers = ["find", "search", "who is", "is there", "look for", "person", "name", "show case"]
    if any(t in query for t in search_triggers) or len(words) == 1:
        active_cases = db_queries.get_not_confirmed_registered_cases(current_user)
        found_cases = db_queries.get_registered_cases_count(current_user, "F")
        all_cases = active_cases + found_cases
        
        person_matches = []
        for c in all_cases:
            name_lower = (c.name or "").lower()
            if any(w in name_lower for w in words if len(w) > 2 and w not in search_triggers):
                status_str = "🟢 RESOLVED / FOUND" if c.status == "F" else "🚨 ACTIVE MISSING"
                person_matches.append(
                    f"• **{c.name}** (Age: {c.age}, {c.gender})\n"
                    f"  - **Status:** {status_str}\n"
                    f"  - **Tracking Code:** `{c.id[:8]}`\n"
                    f"  - **City:** {c.city or 'Avinashi'}\n"
                    f"  - **Distinguishing Marks:** {c.birth_marks or 'None listed'}"
                )
        if person_matches:
            return f"🔍 **Matching Person Database Records ({len(person_matches)}):**\n\n" + "\n\n".join(person_matches)

    # 9. Technical AI Pipeline Explanation
    tech_keys = ["how it works", "technical", "algorithm", "mediapipe", "knn", "vector", "mesh", "accuracy", "468", "distance", "cctv"]
    if any(k in query for k in tech_keys):
        return (
            "🧠 **AVINASHI-AI Technical Core Architecture:**\n\n"
            "1. **Facial Mesh Extraction:** MediaPipe 3D Neural Network detects and extracts **468 landmark coordinates** per face.\n"
            "2. **Vector Space Embedding:** Maps 3D spatial points into a normalized $1404$-dimensional geometric feature vector.\n"
            "3. **Similarity Classification:** K-Nearest Neighbors (KNN) calculates L2 Euclidean Norm distance between vectors.\n"
            "4. **Automated Matching:** Euclidean distance threshold $\\le 3.0$ triggers positive identification and instant officer notification!"
        )

    # 10. App Navigation & Module Guidance
    nav_keys = ["how to register", "register case", "how to track", "report sighting", "cctv scanner", "age progression", "map"]
    if any(k in query for k in nav_keys):
        return (
            "🧭 **Avinashi Portal Navigation Guide:**\n\n"
            "• 📝 **Register a Case:** Click `2_Register New Case` in sidebar to upload a photo and person details.\n"
            "• 🔍 **Track Case:** Use `0_Track Case` to search by Aadhaar, Mobile Number, Name, or Tracking Code.\n"
            "• 👁️ **Report Sighting:** Public citizens or officers can upload sighting photos via `1_Report Sighting`.\n"
            "• 🤖 **Run AI Match:** Navigate to `4_Match Cases` to compute 468 landmark KNN similarity scores.\n"
            "• ⏳ **Age Progression:** Use `5_Age Progression Studio` for +5Y / +10Y predictive face growth.\n"
            "• 📹 **CCTV Scanner:** Use `6_CCTV Scanner` for real-time crowd video frame analysis."
        )

    # 11. Smart Database Fallback Search
    active_cases = db_queries.get_not_confirmed_registered_cases(current_user)
    fallback_matches = []
    for c in active_cases:
        searchable_text = f"{c.name} {c.city} {c.birth_marks} {c.id}".lower()
        if any(w in searchable_text for w in words if len(w) > 2):
            fallback_matches.append(f"• **{c.name}** ({c.city or 'Avinashi'}) — Tracking Code: `{c.id[:8]}`")

    if fallback_matches:
        return (
            f"🔍 **AVINASHI-AI Record Search Results for '{user_query}':**\n\n" +
            "\n".join(fallback_matches)
        )

    # 12. Final Conversational Fallback
    return (
        f"🤖 **AVINASHI-AI Intelligence Assistant:**\n\n"
        f"I parsed your question: *'{user_query}'*.\n\n"
        f"I am ready to help! Try asking me:\n"
        f"• *'Show total registered cases'* — Live database breakdown\n"
        f"• *'Cases in Tiruppur'* — Location density & active missing list\n"
        f"• *'Find birthmark on chin'* — Physical feature search\n"
        f"• *'Explain 468 landmark algorithm'* — Technical AI architecture\n"
        f"• *'How to register a case'* — Navigation guide"
    )

def query_sentinel_ai(user_query: str, current_user: str = "inika") -> str:
    """Alias for backwards compatibility."""
    return query_avinashi_ai(user_query, current_user)

