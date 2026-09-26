# 🛡️ FaceTrace — Complete Project Review & Viva Defense Manual
> **Project Title:** FaceTrace: AI-Powered Missing Person Identification & Police Command System  
> **Station Officer Profile:** Officer Inika B (Avinashi Police Station, Tiruppur)  
> **Backend Database:** Cloud PostgreSQL (Neon Cloud) + SQLModel ORM (with SQLite Fallback)  
> **Live Web Application:** `https://facetrace-ai-powered-missing-person-tracking-system-ho3okwtnyd.streamlit.app/`

---

## 🎯 1. The 1-Minute Elevator Pitch (What to Say When You Begin)

> *"Good morning respected professors. My name is **Inika B**, and today I am presenting my final year project: **FaceTrace — An AI-Powered Missing Person Identification & Police Command Platform**.*
>
> *Traditionally, locating missing persons relies on paper flyers, manual physical searching, and human memory—which is slow, error-prone, and inefficient. My system replaces this with an enterprise-grade AI command portal equipped with **468-point 3D facial landmark mesh analysis**, **K-Nearest Neighbors (KNN) Machine Learning matching**, **Generative AI predictive age progression (+5 to +20 years)**, **real-time CCTV crowd video surveillance scanning**, and **live Cloud PostgreSQL database synchronization**.*
>
> *I have configured the system specifically for **Avinashi Police Station, Tiruppur**, and deployed it live on the web with full HTTPS SSL security."*

---

## 💡 2. The Real-World Problem & Why Your Project is Needed

| Traditional Missing Person Tracking | Your AI Platform (FaceTrace) |
| :--- | :--- |
| **Paper Wanted Flyers**: Easily damaged, lost, or ignored. | **Official PDF Wanted Poster with Scannable QR Code**: Anyone can scan with a smartphone camera to view live case updates. |
| **Slow Human Memory Matching**: Hard to recognize children missing for years. | **Generative AI Age Progression Studio**: Predicts facial growth (+5Y, +10Y, +15Y, +20Y) with wrinkle folds & jawline morphing. |
| **Manual CCTV Video Inspection**: Officers must watch hours of video manually. | **Automated CCTV Scanner**: Scans video frames automatically, detects multiple faces, logs timestamps, and triggers instant alerts. |
| **Isolated Paper Files**: Records trapped in local station notebooks. | **Neon Cloud PostgreSQL Database**: Live 24/7 cloud relational database accessible anywhere across stations. |

---

## 🧩 3. Page-by-Page Tour & Module Explanation

### 🏠 Home Dashboard
* **Officer Authentication**: Secured sign-in (`inika` / `abc`).
* **Sidebar Profile Card**: Displays logged-in officer details (**Officer Inika B**, Avinashi, Tiruppur, Admin).
* **Live Case Metrics**: Displays total cases, resolved cases (`Found`), active missing cases (`Not Found`), and resolution percentage.
* **Command Shortcuts**: Quick navigation grid.
* **🤖 SENTINEL-AI Assistant**: Conversational AI chatbot where officers can ask natural language questions about database records, city case counts, or technical algorithms.
* **📍 Nationwide Case Density Map**: Interactive GIS map plotting case volume across Indian cities using clean OpenStreetMap tiles.

### 🔍 Page 0: Track Case
* **Multi-Identifier Lookup**: Search any registered case by **Aadhaar Card Number**, **Mobile Phone**, **Person Name**, or **Case Tracking ID**.
* **Live Progress Timeline**: Shows step-by-step case status (FIR Registered $\rightarrow$ Public Sighting Uploaded $\rightarrow$ AI Vector Match $\rightarrow$ Case Resolved).

### 📸 Page 1: Report Sighting
* **Public Citizen Portal**: Allows citizens to upload photo or video evidence when they spot a missing person in public, logging sighting location, reporter phone, and distinguishing birthmarks.

### 📝 Page 2: Register New Case
* **Official Case Entry**: Station officers register missing persons with photos, Aadhaar details, complainant contact, and last seen location.
* **MediaPipe 468 3D Mesh Core**: Automatically extracts 468 facial landmark coordinates and saves them into the database as a 1404-element vector array.

### 📂 Page 3: All Cases Database
* **Case Gallery & Poster Generator**: Displays all registered cases with filter options (`All`, `Found`, `Not Found`).
* **PDF Wanted Poster Download**: Generates an official downloadable PDF poster with a scannable QR Code.

### 🤖 Page 4: Match Cases
* **KNN Machine Learning Engine**: Compares public citizen sighting uploads against registered missing persons using K-Nearest Neighbors vector classification ($k=1$).
* **Automatic Status Resolution**: If the landmark distance is $\le 3.0$, status automatically updates from `Not Found` to `Found`.

### ⏳ Page 5: Age Progression Studio
* **Generative AI Predictive Aging**: Extrapolates how a missing child or person looks after **+5, +10, +15, or +20 years**.
* **Visual Aging Features**: Generates forehead wrinkle micro-textures, silver hair highlights, and lower-face jawline broadening.
* **Aged Vector Rescan**: Re-indexes the projected +aged landmark coordinates against public sighting reports.

### 📹 Page 6: CCTV Scanner Console
* **Automated Video Crowd Surveillance**: Scans uploaded CCTV video recordings (`MP4`, `MOV`, `AVI`) frame-by-frame.
* **Diagnostics Grid**: Displays sampled frames, total faces detected, and minimum match distance observed.
* **Bounding Box Snapshot Alerts**: Crops and saves bounding box face match snapshots with exact video timestamps (`e.g., 00:01:24`).

### 🗺️ Page 7: Cases Map (GIS Location Analytics)
* **City Density Mapping**: Plots interactive circle markers across Indian cities (Tiruppur, Chennai, Coimbatore, Delhi, Mumbai, etc.) where circle radius reflects case volume.

### ❓ Page 8: Help & Support
* **Documentation Center**: Comprehensive user manuals, photo upload standards, AI technical specs, and emergency contacts.

---

## 🧠 4. The AI & Technology Stack Explained (Simple vs. Technical)

### A. MediaPipe 3D Face Mesh (Computer Vision / Deep Learning)
* **Simple Explanation**: Think of MediaPipe as placing a digital 3D spiderweb mask over a person's face made of 468 specific dots (nose tip, eye corners, lip edges, jawline). Because it measures 3D geometry rather than colors, it works even if lighting or skin tone changes.
* **Technical Terms**: *Normalized 3D Facial Landmarks ($x, y, z$), Single-Shot Multibox Detector (SSD), Deep Neural Network Landmark Regression.*

### B. K-Nearest Neighbors (KNN) (Machine Learning Algorithm)
* **Simple Explanation**: Imagine placing all facial landmarks as points on a huge 3D map. KNN measures the shortest distance between two facial maps. If the distance between a missing person's face map and a CCTV face map is very small (less than 3.0), KNN identifies them as the same person.
* **Technical Terms**: *Supervised Machine Learning, $L_2$ Euclidean Distance Metric, 1404-Dimensional Feature Space Vector, Ball-Tree Spatial Indexing.*

### C. Generative AI Age Progression Engine
* **Simple Explanation**: It uses mathematical warping and texture filters to simulate natural human aging. It adds soft forehead wrinkles, silver hair highlights, and broadens the jawline to predict what a child will look like 10 or 20 years later.
* **Technical Terms**: *Black-Hat Morphological Filtering, Bilateral Texture Synthesis, Perspective Transform Warping, CLAHE Contrast Adjustment.*

### D. Cloud PostgreSQL Database (Neon Cloud) + SQLModel
* **Simple Explanation**: Instead of saving data on one single laptop, your database is hosted 24/7 on a cloud server in Singapore. If PostgreSQL is offline, the app automatically uses embedded SQLite without crashing.
* **Technical Terms**: *Relational Database Management System (RDBMS), SQLModel ORM, SQLAlchemy Engine, psycopg2 Driver, Cloud Database.*

---

## 🎓 5. Top 10 Viva / Professor Questions & Answers

### Q1: What is the main objective of your project?
> **Answer:** *"The objective is to provide law enforcement with an automated AI platform that replaces slow manual missing person searches with 468-point 3D facial landmark mesh identification, KNN ML matching, CCTV crowd video scanning, and predictive age progression."*

### Q2: How does your facial recognition system handle lighting variations or head tilts?
> **Answer:** *"Unlike basic pixel-matching algorithms, our system uses MediaPipe 3D Face Mesh. It extracts relative 3D coordinate ratios ($x, y, z$) between facial landmarks (eye corners, nose ridge, mouth contours), which remain geometrically stable regardless of lighting or minor head angles."*

### Q3: What Machine Learning algorithm did you use for face matching and why?
> **Answer:** *"We implemented K-Nearest Neighbors (KNN) with $k=1$ and Ball-Tree spatial indexing. KNN is ideal because it measures $L_2$ Euclidean distance across 1404 landmark coordinates ($468 \times 3$). When distance $\le 3.0$, it classifies the match with high accuracy."*

### Q4: How does your Age Progression module work?
> **Answer:** *"It uses a multi-stage generative computer vision pipeline: Black-Hat morphological filtering for skin micro-texture wrinkles, HSV desaturation for silver hair highlights, and perspective affine warping to simulate lower-face jawline broadening over +5 to +20 years."*

### Q5: What database are you using, and how is it connected?
> **Answer:** *"We use Cloud PostgreSQL hosted on Neon Cloud, connected via SQLModel ORM and the `psycopg2` driver. We also built an automatic SQLite fallback mechanism so the system remains 100% operational offline."*

### Q6: How does the CCTV Scanner process video files?
> **Answer:** *"It reads video recordings frame-by-frame, extracts unique faces per frame, computes 3D landmark mesh vectors, calculates KNN distances against active missing person database records, and logs matching snapshots with exact timestamps."*

### Q7: What is the purpose of the QR code on the Wanted Poster?
> **Answer:** *"The QR code embeds a structured digital case payload containing the FIR ID, Missing Person details, Police Station contact, and Web Tracker URL so citizens can scan it with any smartphone camera for instant live tracking."*

### Q8: What is SENTINEL-AI in your Home Dashboard?
> **Answer:** *"SENTINEL-AI is an embedded conversational intelligence chatbot. It parses natural language queries from station officers to query live database records, calculate location metrics, search distinguishing features, or explain system algorithms."*

### Q9: How is your system secured?
> **Answer:** *"It uses bcrypt password hashing and session cookie authentication via Streamlit Authenticator, restricting administrative functions (like triggering AI scans) to authorized station officers."*

### Q10: How can your project be scaled for real-world police deployment?
> **Answer:** *"Because it uses a cloud PostgreSQL database and web-based architecture, it can be scaled across all district police stations in Tamil Nadu or nationwide, integrating with live CCTV camera feeds via RTSP video streaming."*
