"""OS1 — Observation / Exploration (zéro exécution)."""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

from src.core_pipeline import run_observation
from src.score.human_algebra import features_summary
from src.visualization import plot_market_with_decision, plot_features_radar
from src.explainer import explain_features_realtime
from app.ui.enhanced import render_section_header, render_info_card, show_toast
from src.domains_data import generate_domain_specific_data, get_domain_description, get_domain_recommended_tau

def render(base_dir: Path, config: dict):
    """Affiche l'interface d'observation."""
    render_section_header(
        "OS1 — Exploration (Découverte)",
        "🔍 Visualisez les données du marché et calculez les features. Aucune action réelle n'est exécutée ici.",
        "🔍"
    )
    
    render_info_card(
        "Mode Exploration Uniquement",
        "Cette étape permet de découvrir et analyser les données sans risque. Calculez les features pour débloquer OS2 (Simulation).",
        "⚠️",
        "#FF9800"
    )
    
    # Afficher les informations du domaine
    domain_desc = get_domain_description(config["domain"])
    recommended_tau = get_domain_recommended_tau(config["domain"])
    
    st.info(f"🎯 **Domaine sélectionné** : {domain_desc}")
    st.caption(f"🔒 τ recommandé pour ce domaine : {recommended_tau}s")
    
    # Charger les données de marché
    data_path = base_dir / "data" / "trading" / "BTC_1h.csv"
    
    # Essayer de charger les données du fichier, sinon générer
    if data_path.exists() and config["domain"] == "Trading (ERC-8004)":
        df = pd.read_csv(data_path)
    else:
        # Générer des données synthétiques pour le domaine
        st.info("📦 Génération de données synthétiques pour ce domaine...")
        df = generate_domain_specific_data(config["domain"], config["seed"])
    
    st.markdown("#### 📊 Market Data Overview")
    
    # Graphique de prix
    features_for_viz = st.session_state.get("features")
    fig_market = plot_market_with_decision(df.tail(100), features_for_viz or {})
    st.plotly_chart(fig_market, use_container_width=True, key="os1_market_chart")
    
    # Table de données
    with st.expander("📊 View Raw Data"):
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
                
                show_toast("Features calculées avec succès ! OS2 débloqué.", "✅")
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
        st.markdown("#### 📋 Current Features Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Radar chart
            fig_radar = plot_features_radar(st.session_state["features"])
            st.plotly_chart(fig_radar, use_container_width=True, key="os1_radar_chart")
        
        with col2:
            # Explication algèbre humaine temps réel
            st.markdown("##### 💬 Real-Time Explanation")
            realtime_explanation = explain_features_realtime(st.session_state["features"])
            st.markdown(realtime_explanation)
            
            # Interprétation
            features = st.session_state["features"]
            vol = features.get("volatility", 0.5)
            coh = features.get("coherence", 0.5)
            regime = features.get("regime", "unknown")
            
            st.markdown("**Interpretation:**")
            if vol > 0.3:
                st.warning("⚠️ High volatility detected. Market is unstable.")
            else:
                st.success("✅ Low volatility. Market is stable.")
            
            if coh < 0.3:
                st.error("❌ Low coherence. High risk of X-108 HOLD.")
            elif coh > 0.7:
                st.success("✅ High coherence. Favorable conditions.")
            else:
                st.info("ℹ️ Medium coherence. Proceed with caution.")
            
            st.write(f"**Regime**: {regime}")
        
        # Raw JSON
        with st.expander("📊 View Raw Features JSON"):
            st.json(st.session_state["features"])
