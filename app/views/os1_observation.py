"""OS1 — Observation / Exploration (zéro exécution)."""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

from src.core_pipeline import run_observation
from src.score.human_algebra import features_summary

def render(base_dir: Path, config: dict):
    """Affiche l'interface d'observation."""
    st.subheader("OS1 — Observation / Exploration")
    st.caption("⚠️ Compute features only. No execution here.")
    
    # Charger les données de marché
    data_path = base_dir / "data" / "trading" / "BTC_1h.csv"
    
    if not data_path.exists():
        st.error(f"❌ Data file not found: {data_path}")
        return
    
    df = pd.read_csv(data_path)
    
    st.markdown("#### 📊 Market Data Overview")
    st.dataframe(df.tail(10), use_container_width=True)
    
    # Calculer les returns
    if "close" in df.columns:
        prices = df["close"].values
        returns = np.diff(np.log(prices))
    else:
        st.error("❌ 'close' column not found in data")
        return
    
    st.markdown("#### 🔍 Feature Extraction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(f"**Data points**: {len(df)}")
        st.write(f"**Returns computed**: {len(returns)}")
        st.write(f"**Latest price**: {prices[-1]:.2f}")
    
    with col2:
        if st.button("🧮 Compute Features", type="primary"):
            with st.spinner("Computing features..."):
                features = run_observation(returns, base_dir)
                
                st.success("✅ Features computed!")
                
                # Afficher les features
                st.markdown("##### Raw Features")
                st.json(features)
                
                # Algèbre humaine
                st.markdown("##### Human Algebra Summary")
                summary = features_summary(features)
                st.info(summary)
                
                # Sauvegarder dans session state
                st.session_state["features"] = features
                st.session_state["returns"] = returns
    
    # Afficher les features existantes si disponibles
    if "features" in st.session_state:
        st.markdown("---")
        st.markdown("#### 📋 Current Features (from session)")
        st.json(st.session_state["features"])
        
        summary = features_summary(st.session_state["features"])
        st.code(summary, language="text")
