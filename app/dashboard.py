"""Dashboard principal - Obsidia Unified Interface."""
import streamlit as st
import hashlib
import time
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Obsidia Unified Interface",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports locaux - Compatible Streamlit Cloud
import sys

# Ajouter le répertoire parent au path si nécessaire
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import BASE_DIR, BUILD_VERSION, BUILD_HASH
from app.router import select_os_level, get_os_key
from app.ui.layout import header, invariant_panel, sidebar_controls

# Import des vues
from app.views import os0_invariants, os1_observation, os2_simulation, os3_governance, os4_reports

# Session state initialization
if "run_id" not in st.session_state:
    st.session_state.run_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

if "build_hash" not in st.session_state:
    st.session_state.build_hash = BUILD_HASH

# Sidebar controls
config = sidebar_controls()

# OS Level selection
os_level = select_os_level()
os_key = get_os_key(os_level)

# Invariant panel (sticky)
invariant_panel()

# Header
header(
    run_id=st.session_state.run_id,
    domain=config["domain"],
    mode=config["mode"],
    build_hash=st.session_state.build_hash
)

# Router - Dispatch vers la vue appropriée
if os_key == "OS0":
    os0_invariants.render(BASE_DIR)

elif os_key == "OS1":
    os1_observation.render(BASE_DIR, config)

elif os_key == "OS2":
    os2_simulation.render(BASE_DIR, config)

elif os_key == "OS3":
    os3_governance.render(BASE_DIR, config)

elif os_key == "OS4":
    os4_reports.render(BASE_DIR, config)

else:
    st.error(f"Unknown OS level: {os_key}")

# Footer
st.markdown("---")
st.caption(f"Obsidia Unified Interface v{BUILD_VERSION} • Run ID: `{st.session_state.run_id}`")
