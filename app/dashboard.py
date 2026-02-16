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
from app.ui.enhanced import render_progress_stepper
from app.ui.mode_switcher import render_mode_switcher, render_quick_mode_info

# Import des vues
from app.views import os0_invariants, os1_observation, os2_simulation, os3_governance, os5_autorun, os6_exploration
from app.views import os4_reports_extended as os4_reports
from app.views import landing_page, guided_workflow, domain_analytics

# Session state initialization
if "run_id" not in st.session_state:
    st.session_state.run_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

if "build_hash" not in st.session_state:
    st.session_state.build_hash = BUILD_HASH

if "app_mode" not in st.session_state:
    st.session_state["app_mode"] = None  # None = landing, "guided" = mode guidé, "expert" = mode expert

# Vérifier si on est sur la landing page
if st.session_state["app_mode"] is None:
    landing_page.render()
    st.stop()

# Mode switcher (always visible)
render_mode_switcher()

# Sidebar controls
config = sidebar_controls()

# Invariant panel (sticky)
invariant_panel()

# Bouton Domain Analytics
if st.sidebar.button("📊 Dashboard Comparatif des Domaines", use_container_width=True):
    st.session_state["show_domain_analytics"] = True

if st.session_state.get("show_domain_analytics", False):
    domain_analytics.render()
    if st.button("⬅️ Retour", key="back_from_analytics"):
        st.session_state["show_domain_analytics"] = False
        st.rerun()
    st.stop()

# Mode guidé
if st.session_state["app_mode"] == "guided":
    header(
        run_id=st.session_state.run_id,
        domain=config["domain"],
        mode=config["mode"],
        build_hash=st.session_state.build_hash
    )
    guided_workflow.render(BASE_DIR, config)
    st.stop()

# Mode expert (comportement normal)
os_level = select_os_level()
os_key = get_os_key(os_level)

# Header
header(
    run_id=st.session_state.run_id,
    domain=config["domain"],
    mode=config["mode"],
    build_hash=st.session_state.build_hash
)

# Progress Stepper
render_progress_stepper(os_key, st.session_state)

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

elif os_key == "OS5":
    os5_autorun.render(BASE_DIR, config)

elif os_key == "OS6":
    os6_exploration.render(BASE_DIR, config)

else:
    st.error(f"Unknown OS level: {os_key}")

# Footer
st.markdown("---")
st.caption(f"Obsidia Unified Interface v{BUILD_VERSION} • Run ID: `{st.session_state.run_id}`")
