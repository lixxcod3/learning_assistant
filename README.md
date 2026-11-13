<div align="center">

# 💡 LectureMind
**An AI-Powered, Minimalist Lecture Management & Active Recall Web Application**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![AI Pipeline](https://img.shields.io/badge/AI-Local%20ASR%20%26%20LLM-10A37F?style=for-the-badge)](https://ollama.com/)

*Transform raw lecture recordings (.mp3, .mp4, .wav) into structured summaries, interactive flashcards, and gamified quizzes inside an ultra-clean, Notion-inspired workspace.*

</div>

---

## ✨ Key Features

* **🎙️ Automated Multimedia Parsing & ASR:** Upload `.mp3`, `.wav`, or `.mp4` files. The pipeline automatically demultiplexes video streams, downsamples audio tracks, and runs Automatic Speech Recognition (ASR) to generate accurate lecture transcripts.
* **🧠 Grounded AI Generation (Zero-Overwrite Appending):** Generate structured lecture summaries, key takeaways, flashcards, and multiple-choice quizzes. Newly generated flashcards and quizzes dynamically **append** to existing saved decks rather than overwriting them, allowing you to build comprehensive study banks over time.
* **🎨 Liquid-Glass & Notion-Style UI:** Custom DOM-injected CSS overrides standard Streamlit blocks with a dark glassmorphism navigation bar, centered `@st.dialog` modal notifications, and flat, hover-responsive sidebar file trees.
* **🔊 Base64 Invisible Audio Engine:** Instantaneous, non-looping sound effects (`flipcard.mp3`, `right.mp3`, `wrong.mp3`, `finish.mp3`) are injected directly into the DOM via Base64-encoded `<audio autoplay>` tags—delivering tactile feedback without bulky media player widgets.
* **🏅 Gamified Achievement System:** Track study milestones and unlock persistent achievement badges stored inside a local relational SQLite database (`progress.db`).
* **🔄 Collision-Free State Management:** Engineered with strict session-state resets and namespaced widget keys (`side_` vs `dash_`) to prevent `IndexError` and `StreamlitDuplicateElementKey` crashes across multi-view rendering.

---

## 🏗️ Project Architecture

```text
LectureMind/
├── app.py                      # Main entry point, global CSS injection, and top navbar routing
├── requirements.txt            # Python package dependencies
├── database/
│   └── db.py                   # SQLite3 relational schema, JSON serialization, and user auth
├── ai/
│   ├── transcriber.py          # Audio extraction and ASR speech-to-text pipeline
│   ├── summarizer.py           # Transcript chunking and LLM summary/key-point extraction
│   ├── flashcards.py           # JSON-enforced LLM flashcard generation
│   └── quiz_generator.py       # JSON-enforced LLM multiple-choice quiz generation
├── gamification/
│   └── badges.py               # Achievement unlocking logic and status verification
├── ui/
│   ├── components.py           # Reusable Notion-style folder renderer and state-reset callbacks
│   ├── upload_page.py          # User authentication and multimedia upload handler
│   ├── summary_page.py         # Lecture summary viewer, AI generators, and @st.dialog modals
│   ├── flashcard_page.py       # Interactive card-flipping engine with Base64 SFX triggers
│   ├── quiz_page.py            # Interactive MCQ engine with live feedback and score tracking
│   └── dashboard.py            # User profile, full lecture repository, and badge showcase
├── data/                       # Auto-generated local storage
│   ├── progress.db             # SQLite relational database
│   └── lectures/               # Local media storage organized by lecture title
├── sfx/                        # Required audio assets for interaction feedback
│   ├── flipcard.mp3
│   ├── right.mp3
│   ├── wrong.mp3
│   └── finish.mp3
└── images/
    └── bg.jpg                  # Custom background wallpaper encoded via Base64

```

---

## ⚙️ Prerequisites & System Dependencies

Before installing the Python packages, ensure the following system tools and assets are configured on your machine:

1. **Python 3.9+** (Ensure Python is added to your system `PATH`).
2. **FFmpeg:** Required for parsing `.mp4` video containers and processing audio streams.
* *Windows:* `winget install Gyan.FFmpeg` (or download binaries and add to `PATH`).
* *macOS:* `brew install ffmpeg`
* *Linux:* `sudo apt update && sudo apt install ffmpeg`


3. **Local AI Engine / API Configuration:**
* If running local open-source LLMs (e.g., via **Ollama**), ensure the Ollama background service is running (`ollama serve`) and your target model (such as `qwen2.5` or `llama3.2`) is pulled.


4. **Required Static Assets:**
* Ensure the `sfx/` directory exists in the project root containing `flipcard.mp3`, `right.mp3`, `wrong.mp3`, and `finish.mp3`.
* Place a background image at `images/bg.jpg` (if omitted, the UI gracefully falls back to a `#121212` dark theme).



---

## 🚀 Installation & Setup Guide

### 1. Clone the Repository

```bash
git clone [https://github.com/yourusername/LectureMind.git](https://github.com/yourusername/LectureMind.git)
cd LectureMind

```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Python Dependencies

Make sure your `Streamlit` version is **1.35.0 or higher** to support the `@st.dialog` modal decorator:

```bash
pip install --upgrade pip
pip install streamlit>=1.35.0
pip install -r requirements.txt

```

### 4. Launch the Application

```bash
streamlit run app.py

```

The application will automatically initialize `data/progress.db` on first launch and open in your default browser at `http://localhost:8501`.

---

## 📖 Usage Workflow

1. **Authenticate:** Navigate to the **Upload** tab to create a local account or sign in.
2. **Upload Lecture Media:** Upload an `.mp3`, `.wav`, or `.mp4` lecture recording. The system will transcribe the audio, extract key points, save the media locally under `data/lectures/`, and populate your sidebar folder tree.
3. **Generate Study Materials:** Open the **Summary** tab, choose your desired item count (5, 10, 15, or 20), and click **Generate Flashcards** or **Generate Quiz**.
4. **Interactive Study & Appending:** Use the centered popup modal to jump directly into your **Flashcards** or **Quiz**. Complete the session and click **Save** to permanently append the new items to that lecture's database record.
5. **Review & Track Progress:** Play lecture audio directly inside the sidebar folders or visit the **Dashboard** to browse all lectures and view unlocked **Achievement Badges**.

---

## ⚠️ Known Limitations & Engineering Trade-offs

* **Local Compute & Inference Latency:** Because the AI pipeline utilizes free-tier/local models running on consumer hardware (e.g., an 8GB VRAM laptop GPU) rather than paid enterprise cloud endpoints, transcription and quiz generation exhibit noticeable processing latency on longer recordings.
* **200MB File Upload Cap:** File uploads are capped at Streamlit's default 200MB limit. Supporting multi-gigabyte video lectures would require an asynchronous task queue (e.g., Celery/Redis) and dedicated cloud bucket storage.
* **LLM Context Window Constraints:** Very long lectures (2+ hours) can exceed the token context window of smaller local LLMs, requiring transcript chunking or truncation during summary and quiz extraction.
* **Local-First Ephemeral Storage:** Media files and the SQLite database (`progress.db`) are stored directly on the local filesystem. Deploying to ephemeral cloud containers (such as Streamlit Community Cloud) without attaching a persistent volume or migrating to PostgreSQL/S3 will result in data resets upon container sleep.
* **Prototype Authentication:** User credentials in `db.py` are designed for local, single-machine profiles. Production deployment requires integrating cryptographic password hashing (e.g., `bcrypt`) and token-based session cookies.

---

## 👥 Contributors & Roles

* **Person 1:** AI Pipeline & Prompt Engineering (ASR transcription, LLM summarization, JSON schema enforcement for quizzes & flashcards).
* **Person 2:** Database Architecture & Gamification Logic (SQLite schema design, user authentication, badge unlocking rules).
* **Person 3 (Lead Integrator):** Full-Stack Integration, State Architecture & UI/UX Engineering (Streamlit session-state synchronization, custom liquid-glass & Notion CSS injection, Base64 SFX engine, modal workflows, and cross-module debugging).