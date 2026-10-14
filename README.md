OUR SHARED UNIVERSE — SIMPLE SETUP

Files:
- app.py: the full Streamlit app
- requirements.txt: Python packages
- .streamlit/secrets.toml.example: example API-key configuration

Run locally:
1. Install Python 3.10+ if it is not installed.
2. Put app.py and requirements.txt in the same folder.
3. Open a terminal in that folder and run:
   python -m pip install -r requirements.txt
4. Create a folder named .streamlit
5. Copy secrets.toml.example into that folder and rename the copy to secrets.toml
6. Open secrets.toml and replace the placeholder with your real Gemini API key.
7. Run:
   streamlit run app.py

IMPORTANT:
- Never share your real API key or upload secrets.toml publicly.
- The profile selector is not a secure login.
- Notes, recipes, songs, memories, and chat are stored in a local SQLite database
  named our_shared_universe.db beside app.py. They survive normal refreshes and
  app restarts as long as that file is kept.
- This local SQLite setup does not automatically sync between two different devices
  or provide backups. A hosted deployment may have ephemeral storage; for reliable
  multi-device sharing, use a persistent hosted database later.
- Song metadata is saved; this version does not store audio uploads.
- Nutrition content is general information, not personal medical advice.
