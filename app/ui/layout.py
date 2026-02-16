"""Layout components for the Obsidia Unified Interface."""
import streamlit as st
from datetime import datetime

def header(run_id: str, domain: str, mode: str, build_hash: str):
    """Affiche le header principal avec les informations de contexte."""
    st.markdown("### Obsidia Unified Interface")
    st.caption(
        f"Run: `{run_id}` • Domain: `{domain}` • Mode: `{mode}` • Build: `{build_hash}` • "
        f"Time: {datetime.now().strftime('%H:%M:%S')}"
    )

def invariant_panel():
    """Affiche le panneau des invariants dans la sidebar."""
    with st.sidebar.expander("⚖️ Lois Fondamentales (Invariants)", expanded=False):
        st.markdown("**🔒 Lois du Système:**")
        st.markdown("- Priorité: **BLOCK > HOLD > ALLOW**")
        st.markdown("- X-108: **HOLD→ACT** pour intents irréversibles")
        st.markdown("- Séparation: **Exploration ≠ Action**")
        st.markdown("- Non-anticipation: **ACT INTERDIT avant τ**")
        
        st.markdown("---")
        st.markdown("**💡 Rappel:**")
        st.caption("Ces lois sont **non-négociables** et s'appliquent à tous les niveaux OS.")

def sidebar_controls():
    """Affiche les contrôles globaux dans la sidebar."""
    st.sidebar.title("🏛️ Console de Contrôle")
    
    from app.config import MODES, DOMAINS, DEFAULT_SEED, DEFAULT_TAU, BASE_DIR
    from src.scenarios import load_scenarios
    
    # Section Configuration
    with st.sidebar.expander("⚙️ Configuration Générale", expanded=True):
        mode = st.selectbox("🎭 Mode d'exécution", MODES, index=0, 
                           help="Proof: Scénarios déterministes pour validation | Free: Exploration libre")
        domain = st.selectbox("🎯 Domaine d'application", DOMAINS, index=0,
                             help="Sélectionnez le domaine métier à analyser")
    
    # Scenario picker (Proof Mode only)
    selected_scenario = None
    if mode.startswith("Proof"):
        with st.sidebar.expander("🎯 Scénarios de Test", expanded=False):
            scenarios = load_scenarios(BASE_DIR, "trading")
            if scenarios:
                scenario_names = ["(Aucun)"] + [f"{s['id']}: {s['name']}" for s in scenarios]
                scenario_choice = st.selectbox("Choisir un scénario", scenario_names, index=0,
                                              help="Scénarios prédéfinis pour tests de validation")
                
                if scenario_choice != "(Aucun)":
                    scenario_id = scenario_choice.split(":")[0]
                    selected_scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
                    
                    if selected_scenario:
                        st.info(f"✅ {selected_scenario['description']}")
    
    # Section Paramètres
    with st.sidebar.expander("⏱️ Paramètres Temporels & Aléatoires", expanded=True):
        seed = st.number_input("🎲 Graine aléatoire", min_value=0, value=DEFAULT_SEED, step=1,
                              help="Pour reproduire exactement les mêmes résultats")
        tau = st.slider("🔒 Délai de sécurité τ (secondes)", 1.0, 30.0, DEFAULT_TAU, 1.0,
                       help="Temps d'attente obligatoire avant action irréversible (X-108)")
    
    return {
        "mode": mode,
        "domain": domain,
        "seed": int(seed),
        "tau": float(tau),
        "nondeterministic": mode.startswith("Free"),
        "selected_scenario": selected_scenario
    }
