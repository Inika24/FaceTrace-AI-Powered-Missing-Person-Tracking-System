import os
import cv2
import json
import time
import numpy as np
from PIL import Image
import streamlit as st

from pages.helper.utils import detect_all_faces, draw_face_boxes
from pages.helper import db_queries, match_algo

def scan_video_stream(video_path: str, user: str, frame_skip: int = 5, distance_threshold: float = 3.0):
    """
    Scans a CCTV video recording frame-by-frame against the missing person landmark database.
    Returns: tuple of (alerts, stats_dict)
    """
    stats = {
        "total_frames": 0,
        "faces_detected": 0,
        "min_distance": 999.0,
        "min_distance_case": None,
        "db_cases_count": 0
    }

    if not os.path.exists(video_path):
        return [], stats

    # Get active missing cases in database
    db_cases = db_queries.get_not_confirmed_registered_cases(user)
    if not db_cases:
        # Fallback to all unresolved registered cases across system
        with db_queries.Session(db_queries.engine) as session:
            db_cases = session.exec(
                db_queries.select(db_queries.RegisteredCases).where(db_queries.RegisteredCases.status == "NF")
            ).all()

    stats["db_cases_count"] = len(db_cases) if db_cases else 0

    if not db_cases:
        return [], stats

    cap = cv2.VideoCapture(video_path)
    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if not fps or fps <= 0 or np.isnan(fps):
            fps = 30.0
    except Exception:
        fps = 30.0
    frame_count = 0

    alerts = []
    output_dir = "./resources/cctv_matches"
    os.makedirs(output_dir, exist_ok=True)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        stats["total_frames"] += 1
        timestamp_sec = frame_count / fps
        time_str = time.strftime("%H:%M:%S", time.gmtime(timestamp_sec))

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detected_faces = detect_all_faces(frame_rgb, max_faces=5)

        if not detected_faces:
            continue

        stats["faces_detected"] += len(detected_faces)

        for face in detected_faces:
            landmarks = face["landmarks"]
            
            # Compare face against all missing cases in DB
            for case_obj in db_cases:
                try:
                    target_landmarks = json.loads(case_obj.face_mesh)
                    dist = match_algo.calculate_distance(landmarks, target_landmarks)
                    
                    if dist < stats["min_distance"]:
                        stats["min_distance"] = round(dist, 2)
                        stats["min_distance_case"] = case_obj.name

                    if dist <= distance_threshold:
                        confidence = max(0.0, min(100.0, (1.0 - dist / max(0.1, distance_threshold)) * 100))
                        
                        # Save annotated snapshot
                        annotated_frame = draw_face_boxes(frame_rgb, [face], selected_idx=0)
                        snapshot_name = f"cctv_match_{case_obj.id[:8]}_{int(timestamp_sec)}s.jpg"
                        snapshot_path = os.path.join(output_dir, snapshot_name)
                        
                        pil_img = Image.fromarray(np.array(annotated_frame))
                        pil_img.save(snapshot_path)

                        alerts.append({
                            "case_id": case_obj.id,
                            "name": case_obj.name,
                            "timestamp": time_str,
                            "timestamp_sec": int(timestamp_sec),
                            "confidence": round(confidence, 1),
                            "distance": round(dist, 2),
                            "snapshot_path": snapshot_path,
                            "last_seen": case_obj.last_seen,
                            "city": case_obj.city or "Unknown"
                        })
                        break  # Match found for this face
                except Exception:
                    continue

    cap.release()
    if stats["min_distance"] == 999.0:
        stats["min_distance"] = None
    return alerts, stats
