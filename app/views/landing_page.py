"""Landing page with Guided vs Expert mode selection."""
import streamlit as st
from pathlib import Path

def render():
    """Affiche la landing page avec choix du mode."""
    
    # CSS personnalisé
    st.markdown("""
    <style>
    .landing-container {
        text-align: center;
        padding: 40px 20px;
    }
    .landing-title {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .landing-subtitle {
        font-size: 20px;
        color: #666;
        margin-bottom: 50px;
    }
    .mode-card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    .mode-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    .mode-icon {
        font-size: 64px;
        margin-bottom: 20px;
    }
    .mode-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #333;
    }
    .mode-description {
        font-size: 16px;
        color: #666;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .mode-features {
        text-align: left;
        margin: 20px 0;
    }
    .mode-features li {
        margin: 8px 0;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="landing-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="landing-title">🏛️ OBSIDIA UNIFIED INTERFACE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="landing-subtitle">Système de gouvernance transparent pour IA autonome</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Choix du mode
    st.markdown("## 🎯 Choisissez votre parcours")
    st.markdown("Sélectionnez le mode qui correspond le mieux à votre niveau d'expertise.")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">🎓</div>
            <div class="mode-title">Mode Guidé</div>
            <div class="mode-description">
                Parfait pour <strong>découvrir</strong> et <strong>comprendre</strong> 
                le fonctionnement du système étape par étape.
            </div>
            <div class="mode-features">
                <strong>Inclut :</strong>
                <ul>
                    <li>✅ Workflow pas-à-pas</li>
                    <li>✅ Explications détaillées</li>
                    <li>✅ Scénarios prédéfinis</li>
                    <li>✅ Assistance contextuelle</li>
                    <li>✅ Validation automatique</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Démarrer en Mode Guidé", type="primary", use_container_width=True):
            st.session_state["app_mode"] = "guided"
            st.session_state["guided_step"] = 1
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">⚡</div>
            <div class="mode-title">Mode Expert</div>
            <div class="mode-description">
                Accès <strong>complet</strong> à toutes les fonctionnalités 
                sans restrictions ni guidage.
            </div>
            <div class="mode-features">
                <strong>Inclut :</strong>
                <ul>
                    <li>✅ Accès direct OS0-OS6</li>
                    <li>✅ Configuration avancée</li>
                    <li>✅ Scénarios personnalisés</li>
                    <li>✅ Stress testing</li>
                    <li>✅ Exports complets</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ Démarrer en Mode Expert", use_container_width=True):
            st.session_state["app_mode"] = "expert"
            st.rerun()
    
    st.markdown("---")
    
    # Section informative
    with st.expander("📚 En savoir plus sur Obsidia"):
        st.markdown("""
        ### Qu'est-ce qu'Obsidia ?
        
        **Obsidia Unified Interface** est un système de gouvernance pour agents autonomes 
        basé sur des **lois fondamentales non-négociables** (X-108, Gate Priority, etc.).
        
        #### 🎯 Objectifs
        - **Transparence** : Chaque décision est expliquée et traçable
        - **Sécurité** : Verrous temporels et gates de validation
        - **Auditabilité** : Tous les artefacts sont exportables
        - **Reproductibilité** : Seed + Run ID pour tests déterministes
        
        #### 🏗️ Architecture
        - **OS0** : Lois fondamentales (invariants)
        - **OS1** : Exploration des données (sans risque)
        - **OS2** : Simulation Monte Carlo (projection)
        - **OS3** : Gouvernance (gates + X-108 + ROI)
        - **OS4** : Rapports et exports (audit)
        - **OS5** : Démo automatisée (scénarios)
        - **OS6** : Tests de stress (avancé)
        
        #### 🔒 Principes Clés
        1. **BLOCK > HOLD > ALLOW** : Priorité stricte des décisions
        2. **X-108 Temporal Lock** : Délai obligatoire (τ) avant action irréversible
        3. **Exploration ≠ Action** : Séparation des rôles
        4. **Non-Anticipation** : Impossible d'agir avant τ
        """)
    
    with st.expander("🎓 Mode Guidé vs ⚡ Mode Expert : Quelle différence ?"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎓 Mode Guidé
            
            **Pour qui ?**
            - Nouveaux utilisateurs
            - Démonstrations
            - Formation
            - Validation de concepts
            
            **Fonctionnement :**
            - Workflow linéaire OS1→OS2→OS3→OS4
            - Explications à chaque étape
            - Validation automatique des prérequis
            - Scénarios prédéfinis
            - Assistance contextuelle
            
            **Avantages :**
            - Apprentissage rapide
            - Pas d'erreurs de navigation
            - Compréhension profonde
            """)
        
        with col2:
            st.markdown("""
            ### ⚡ Mode Expert
            
            **Pour qui ?**
            - Utilisateurs expérimentés
            - Développeurs
            - Auditeurs
            - Chercheurs
            
            **Fonctionnement :**
            - Navigation libre entre tous les OS
            - Configuration avancée
            - Création de scénarios custom
            - Tests de stress
            - Exports techniques
            
            **Avantages :**
            - Flexibilité maximale
            - Accès complet
            - Personnalisation
            """)
    
    # Footer
    st.markdown("---")
    st.caption("Obsidia Unified Interface v1.0.0 • Build: obsi-unified-mvp")
