"""Guided workflow for step-by-step user experience."""
import streamlit as st
from pathlib import Path
from app.views import os1_observation, os2_simulation, os3_governance, os4_reports_extended
from app.ui.navigation import render_permanent_header, render_breadcrumb, render_enhanced_stepper
from src.state_manager import init_config_state, get_data_flags

def render(base_dir: Path, config: dict):
    """Affiche le workflow guidé."""
    
    # Initialiser state
    init_config_state()
    
    # Initialiser l'étape si nécessaire
    if "guided_step" not in st.session_state:
        st.session_state["guided_step"] = 1
    
    current_step = st.session_state["guided_step"]
    
    # Header permanent
    render_permanent_header(mode="guided", step=current_step)
    
    # Breadcrumb
    step_names = ["Mode Guidé", "Configuration", "Exploration", "Simulation", "Gouvernance", "Rapport"]
    render_breadcrumb(step_names[:current_step+1], current_step)
    
    # Stepper amélioré
    steps = [
        ("⚙️", "Configuration"),
        ("🔍", "Exploration"),
        ("🎲", "Simulation"),
        ("⚖️", "Gouvernance"),
        ("📊", "Rapport")
    ]
    
    # Déterminer les étapes complétées
    flags = get_data_flags()
    completed = []
    if current_step > 1:
        completed.append(0)  # Config toujours complétée après étape 1
    if flags["features_computed"] and current_step > 2:
        completed.append(1)  # Exploration complétée
    if flags["simulation_done"] and current_step > 3:
        completed.append(2)  # Simulation complétée
    if flags["governance_tested"] and current_step > 4:
        completed.append(3)  # Gouvernance complétée
    
    render_enhanced_stepper(steps, current_step - 1, completed)
    
    # Contenu selon l'étape
    if current_step == 1:
        render_step1_config(config)
    elif current_step == 2:
        render_step2_exploration(base_dir, config)
    elif current_step == 3:
        render_step3_simulation(base_dir, config)
    elif current_step == 4:
        render_step4_governance(base_dir, config)
    elif current_step == 5:
        render_step5_report(base_dir, config)

def render_guided_stepper(current_step: int):
    """Affiche le stepper du mode guidé."""
    steps = [
        ("1", "Configuration", "⚙️"),
        ("2", "Exploration", "🔍"),
        ("3", "Simulation", "🎲"),
        ("4", "Gouvernance", "⚖️"),
        ("5", "Rapport", "📊")
    ]
    
    cols = st.columns(5)
    
    for i, (num, label, icon) in enumerate(steps, 1):
        with cols[i-1]:
            if i < current_step:
                st.markdown(f"<div style='text-align: center; color: #4CAF50;'>{icon}<br><strong>✓ {label}</strong></div>", unsafe_allow_html=True)
            elif i == current_step:
                st.markdown(f"<div style='text-align: center; color: #FF9800;'>{icon}<br><strong>▶️ {label}</strong></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: center; color: #9E9E9E;'>{icon}<br>{label}</div>", unsafe_allow_html=True)
    
    st.markdown("---")

def render_step1_config(config: dict):
    """Étape 1: Configuration."""
    st.markdown("## ⚙️ Étape 1 : Configuration")
    
    st.markdown("""
    ### Bienvenue dans le mode guidé !
    
    Dans cette première étape, vous allez configurer les paramètres de base pour votre analyse.
    
    #### 💡 Ce que vous allez faire :
    1. Choisir un **domaine d'application** (Trading, Santé, etc.)
    2. Définir le **délai de sécurité τ** (X-108 Temporal Lock)
    3. Sélectionner une **graine aléatoire** pour la reproductibilité
    """)
    
    st.info("ℹ️ **Astuce** : Pour votre première utilisation, nous recommandons le domaine **Trading (ERC-8004)** avec les paramètres par défaut.")
    
    # Afficher la configuration actuelle
    st.markdown("### 📋 Configuration Actuelle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🎯 Domaine", config["domain"])
        st.metric("🎲 Seed", config["seed"])
    
    with col2:
        st.metric("🔒 Délai τ", f"{config['tau']}s")
        st.metric("🎭 Mode", config["mode"])
    
    st.markdown("---")
    
    st.markdown("""
    ### ✅ Configuration validée !
    
    Vous pouvez maintenant passer à l'étape suivante : **Exploration des données**.
    
    ⚠️ **Note** : Vous pouvez modifier ces paramètres à tout moment dans la console latérale (à gauche).
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Retour au menu", use_container_width=True):
            st.session_state["app_mode"] = None
            del st.session_state["guided_step"]
            st.rerun()
    
    with col3:
        if st.button("Suivant ➡️", type="primary", use_container_width=True):
            st.session_state["guided_step"] = 2
            st.rerun()

def render_step2_exploration(base_dir: Path, config: dict):
    """Étape 2: Exploration."""
    st.markdown("## 🔍 Étape 2 : Exploration des Données")
    
    st.markdown("""
    ### Découvrez les données du marché
    
    Dans cette étape, vous allez :
    1. **Visualiser** les données de marché (prix, volatilité)
    2. **Calculer les features** nécessaires pour la simulation
    3. **Comprendre** les métriques clés (cohérence, stabilité, friction)
    
    ⚠️ **Important** : Aucune action réelle n'est exécutée ici. C'est une phase d'**exploration sans risque**.
    """)
    
    st.markdown("---")
    
    # Appeler la vue OS1
    os1_observation.render(base_dir, config)
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Précédent", use_container_width=True):
            st.session_state["guided_step"] = 1
            st.rerun()
    
    with col3:
        # Vérifier si les features sont calculées
        has_features = "features" in st.session_state
        
        if st.button("Suivant ➡️", type="primary", use_container_width=True, disabled=not has_features):
            if has_features:
                st.session_state["guided_step"] = 3
                st.rerun()
            else:
                st.warning("⚠️ Veuillez d'abord calculer les features en cliquant sur '🧮 Compute Features'")

def render_step3_simulation(base_dir: Path, config: dict):
    """Étape 3: Simulation."""
    st.markdown("## 🎲 Étape 3 : Simulation Monte Carlo")
    
    st.markdown("""
    ### Projetez les risques futurs
    
    Dans cette étape, vous allez :
    1. **Exécuter** une simulation Monte Carlo (1000 scénarios)
    2. **Analyser** la distribution des retours possibles
    3. **Évaluer** le risque (CVaR 95%)
    
    💡 **Rappel** : Cette simulation utilise les features calculées à l'étape précédente.
    """)
    
    st.markdown("---")
    
    # Appeler la vue OS2
    os2_simulation.render(base_dir, config)
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Précédent", use_container_width=True):
            st.session_state["guided_step"] = 2
            st.rerun()
    
    with col3:
        has_simulation = "simulation" in st.session_state
        
        if st.button("Suivant ➡️", type="primary", use_container_width=True, disabled=not has_simulation):
            if has_simulation:
                st.session_state["guided_step"] = 4
                st.rerun()
            else:
                st.warning("⚠️ Veuillez d'abord exécuter la simulation")

def render_step4_governance(base_dir: Path, config: dict):
    """Étape 4: Gouvernance."""
    st.markdown("## ⚖️ Étape 4 : Gouvernance et Décision")
    
    st.markdown("""
    ### Évaluez les gates et émettez un intent
    
    Dans cette étape, vous allez :
    1. **Vérifier** les 3 gates de validation (Integrity, X-108, Risk)
    2. **Appliquer** la politique ROI (Return on Intent)
    3. **Émettre** un intent papier (ERC-8004)
    
    🔒 **Important** : C'est ici que les **lois fondamentales** (X-108, Gate Priority) s'appliquent.
    """)
    
    st.markdown("---")
    
    # Appeler la vue OS3
    os3_governance.render(base_dir, config)
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Précédent", use_container_width=True):
            st.session_state["guided_step"] = 3
            st.rerun()
    
    with col3:
        if st.button("Suivant ➡️", type="primary", use_container_width=True):
            st.session_state["guided_step"] = 5
            st.rerun()

def render_step5_report(base_dir: Path, config: dict):
    """Étape 5: Rapport."""
    st.markdown("## 📊 Étape 5 : Rapport et Export")
    
    st.markdown("""
    ### Exportez et analysez les résultats
    
    Félicitations ! Vous avez complété le workflow guidé. 🎉
    
    Dans cette dernière étape, vous pouvez :
    1. **Consulter** tous les artefacts générés
    2. **Exporter** les résultats (JSON, ZIP)
    3. **Analyser** les preuves et tests
    4. **Comparer** Naive vs Governed
    """)
    
    st.markdown("---")
    
    # Appeler la vue OS4
    os4_reports_extended.render(base_dir, config)
    
    st.markdown("---")
    
    # Navigation finale
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Précédent", use_container_width=True):
            st.session_state["guided_step"] = 4
            st.rerun()
    
    with col2:
        if st.button("🔄 Recommencer", use_container_width=True):
            st.session_state["guided_step"] = 1
            # Nettoyer le session state
            for key in ["features", "simulation", "gates_result", "roi_decision"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col3:
        if st.button("⚡ Mode Expert", type="primary", use_container_width=True):
            st.session_state["app_mode"] = "expert"
            del st.session_state["guided_step"]
            st.rerun()
