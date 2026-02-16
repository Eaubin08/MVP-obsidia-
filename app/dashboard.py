"""Main dashboard for Obsidia Unified Interface."""
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
from app.ui.styles import inject_custom_css
from app.ui.header import render_header_guided, render_header_expert
from app.ui.expert_navigation import render_expert_sidebar

# Import des vues
from app.views import os0_invariants, os1_observation, os2_simulation, os3_governance, os5_autorun, os6_exploration
from app.views import os4_reports_extended as os4_reports
from app.views import landing_page, guided_workflow, domain_analytics

# Inject custom CSS for professional appearance
inject_custom_css()

# Session state initialization
if "run_id" not in st.session_state:
    st.session_state.run_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

if "build_hash" not in st.session_state:
    st.session_state.build_hash = BUILD_HASH

if "app_mode" not in st.session_state:
    st.session_state["app_mode"] = None  # None = landing, "guided" = mode guidé, "expert" = mode expert

if "os_level" not in st.session_state:
    st.session_state["os_level"] = "OS0"

if "guided_step" not in st.session_state:
    st.session_state["guided_step"] = 1

if "seed" not in st.session_state:
    st.session_state["seed"] = 42

if "tau" not in st.session_state:
    st.session_state["tau"] = 10.0

if "domain" not in st.session_state:
    st.session_state["domain"] = "trading"

# Vérifier si on est sur la landing page
if st.session_state["app_mode"] is None:
    landing_page.render()
    st.stop()

# Configuration object
config = {
    "domain": st.session_state.get("domain", "trading"),
    "mode": "proof" if st.session_state.get("seed", 42) == 42 else "free",
    "seed": st.session_state.get("seed", 42),
    "tau": st.session_state.get("tau", 10.0),
    "run_id": st.session_state.run_id,
    "build_hash": st.session_state.build_hash
}

# ========================================
# MODE GUIDÉ
# ========================================
if st.session_state["app_mode"] == "guided":
    # Header with progress bar (no sidebar)
    render_header_guided()
    
    # Render guided workflow
    guided_workflow.render(BASE_DIR, config)
    st.stop()

# ========================================
# MODE EXPERT
# ========================================
if st.session_state["app_mode"] == "expert":
    # Header with breadcrumb
    render_header_expert()
    
    # Sidebar navigation
    selected_os = render_expert_sidebar()
    
    # Check if Domain Analytics is requested
    if st.session_state.get("show_domain_analytics", False):
        domain_analytics.render()
        if st.button("⬅️ Retour", key="back_from_analytics"):
            st.session_state["show_domain_analytics"] = False
            st.rerun()
        st.stop()
    
    # Render selected OS level
    if selected_os == "OS0":
        st.markdown("""
        ### 📖 À PROPOS DE CE NIVEAU
        
        **OS0** définit les **lois fondamentales** qui régissent tout le système. Ces invariants garantissent la sécurité et la traçabilité des décisions.
        
        **Rôle** : Comprendre les règles du jeu (avant d'explorer ou d'agir).
        """)
        os0_invariants.render(BASE_DIR, config)
    
    elif selected_os == "OS1":
        st.markdown("""
        ### 📖 À PROPOS DE CE NIVEAU
        
        **OS1** permet d'explorer les données sans prendre de décision. Vous êtes dans le rôle **Explorer** (séparation Explorer ≠ Executor ≠ Roi).
        
        **Rôle** : Analyser et extraire les features (aucune action irréversible possible).
        """)
        os1_observation.render(BASE_DIR, config)
    
    elif selected_os == "OS2":
        st.markdown("""
        ### 📖 À PROPOS DE CE NIVEAU
        
        **OS2** projette les scénarios futurs possibles via **simulation Monte Carlo**. Aucune décision n'est prise, seulement des projections.
        
        **Rôle** : Simuler (évaluer les risques avant de décider).
        """)
        os2_simulation.render(BASE_DIR, config)
    
    elif selected_os == "OS3":
        st.markdown("""
        ### 📖 À PROPOS DE CE NIVEAU
        
        **OS3** applique les **3 gates de validation** (Integrity, X-108, Risk) et la politique **ROI** pour émettre un intent papier.
        
        **Rôle** : Gouverner (décider selon les lois fondamentales).
        """)
        os3_governance.render(BASE_DIR, config)
    
    elif selected_os == "OS4":
        st.markdown("""
        ### 📖 À PROPOS DE CE NIVEAU
        
        **OS4** permet de consulter tous les artefacts générés, d'exporter les résultats et d'analyser les preuves.
        
        **Rôle** : Auditer (traçabilité et reproductibilité).
        """)
        os4_reports.render(BASE_DIR, config)
    
    elif selected_os == "OS5":
        st.markdown("""
        ### 📖 À PROPOS DE CE NIVEAU
        
        **OS5** exécute automatiquement des scénarios prédéfinis pour démonstration et validation.
        
        **Rôle** : Démontrer (prouver le fonctionnement du système).
        """)
        os5_autorun.render(BASE_DIR, config)
    
    elif selected_os == "OS6":
        st.markdown("""
        ### 📖 À PROPOS DE CE NIVEAU
        
        **OS6** génère des scénarios aléatoires pour tester la robustesse du système dans des conditions extrêmes.
        
        **Rôle** : Stresser (valider la résilience).
        """)
        os6_exploration.render(BASE_DIR, config)
