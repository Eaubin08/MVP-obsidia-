"""Composants de layout réutilisables."""
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
    with st.sidebar.expander("⚖️ Invariant Panel (sticky)", expanded=True):
        st.markdown("**Core Laws:**")
        st.markdown("- Priority: **BLOCK > HOLD > ALLOW**")
        st.markdown("- X-108: **HOLD→ACT** for irreversible intents")
        st.markdown("- Separation: **Exploration ≠ Action**")
        st.markdown("- Non-anticipation: **ACT MUST NOT before τ**")

def sidebar_controls():
    """Affiche les contrôles globaux dans la sidebar."""
    st.sidebar.title("🎛️ Console")
    
    from app.config import MODES, DOMAINS, DEFAULT_SEED, DEFAULT_TAU
    
    mode = st.sidebar.selectbox("Mode", MODES, index=0)
    domain = st.sidebar.selectbox("Domain", DOMAINS, index=0)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        seed = st.number_input("Seed", min_value=0, value=DEFAULT_SEED, step=1)
    with col2:
        tau = st.slider("τ (s)", 1.0, 30.0, DEFAULT_TAU, 1.0)
    
    return {
        "mode": mode,
        "domain": domain,
        "seed": int(seed),
        "tau": float(tau),
        "nondeterministic": mode.startswith("Free")
    }
