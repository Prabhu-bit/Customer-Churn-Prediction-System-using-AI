"""
Customer Churn Prediction - Fixed Streamlit Frontend with REDUCED FEATURES
Uses only 12 most important features for faster, cleaner predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import sys
import requests

# Configure Streamlit page
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px;
    }
    .prediction-high-risk {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
    }
    .prediction-stable {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# LOAD MODELS AND DATA - USING REDUCED FEATURES
# ============================================================================

@st.cache_resource
def load_model_and_features():
    """Load trained model and feature order from new folder structure"""
    try:
        # Get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        
        # Paths for reduced model
        model_path = os.path.join(parent_dir, "07_Models_Trained", "final_optimized_churn_model_reduced.pkl")
        metadata_path = os.path.join(parent_dir, "07_Models_Trained", "model_metadata.json")
        training_data_path = os.path.join(parent_dir, "05_Data_Splits", "training_split.csv")
        
        # Load model metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        feature_columns = metadata['features']
        
        # Load model
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            st.success(f"✓ Model loaded successfully ({len(feature_columns)} features)")
        else:
            st.error(f"Model file not found at: {model_path}")
            return None, None, None
        
        # Load training data for encoding reference
        if os.path.exists(training_data_path):
            training_data = pd.read_csv(training_data_path)
        else:
            st.error(f"Training data not found at: {training_data_path}")
            training_data = None
        
        return model, feature_columns, training_data
    
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None, None

@st.cache_data
def load_original_data():
    """Load original dataset info"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        data_path = os.path.join(parent_dir, "04_Data_Raw", "customer_churn.csv")
        
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            return df
        else:
            st.warning(f"Original data not found at: {data_path}")
            return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")


def _build_retention_email_fallback(tenure, contract, charges, churn_score):
    if churn_score >= 0.7:
        return (
            "Subject: Let us help you keep your current plan working for you\n\n"
            "Hi there,\n\n"
            f"I was reviewing your {contract} plan, and since you have been with us for {tenure} months, I wanted to reach out personally before you make any changes. "
            f"Your current monthly charge is ${charges:.2f}, and I would like to look at a better-fit offer with you if the service or price is not matching what you need right now. "
            "If you are open to it, reply with the best time to talk and I will help sort through the available options.\n\n"
            "Best,\n"
            "Your Customer Success Team"
        )

    return (
        "Subject: A quick note about your current service\n\n"
        "Hi there,\n\n"
        f"Thanks for being with us for {tenure} months on the {contract} plan. "
        f"At ${charges:.2f} per month, your account looks like it may benefit from a quick review, and I would be happy to help you compare options that better fit how you use the service. "
        "If you'd like, reply and I can walk you through a few simple ways to lower the bill or improve the plan.\n\n"
        "Warm regards,\n"
        "Your Customer Success Team"
    )


def call_llm_retention_api(tenure, contract, charges, churn_score):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _build_retention_email_fallback(tenure, contract, charges, churn_score)

    prompt = f"""
Write a natural, human-sounding retention email that reads like it was written by an experienced account manager, not an AI tool.

Customer profile:
- Contract type: {contract}
- Account tenure: {tenure} months
- Monthly charges: ${charges:.2f}
- Churn risk score: {churn_score * 100:.1f}%

Requirements:
- Make the wording feel fresh and customer-specific.
- Vary the opening, middle, and closing depending on whether the customer is medium or high risk.
- Refer to the customer's contract, tenure, and price in a natural way.
- Avoid generic AI phrases such as "we value your business", "our system has flagged", or "retention offer".
- Use a calm human tone, like a real support or account representative.
- Offer a realistic next step, such as a plan review, billing check, or account consultation.
- Do not use placeholders.
- Return only the email body with a subject line.
""".strip()

    payload = {
        "model": OPENAI_MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a senior customer retention specialist for a telecom enterprise."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = requests.post(OPENAI_CHAT_COMPLETIONS_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        response_json = response.json()
        choices = response_json.get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content", "").strip()
            if content:
                return content
    except Exception:
        pass

    return _build_retention_email_fallback(tenure, contract, charges, churn_score)

# Load models and data
model, feature_columns, training_data = load_model_and_features()
df = load_original_data()

# ============================================================================
# SIDEBAR - NAVIGATION
# ============================================================================

st.sidebar.title("🎯 Churn Prediction System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Home", "🔮 Make Prediction", "📊 Analytics", "ℹ️ About Model"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **How to use:**\n\n"
    "1. Go to 'Make Prediction'\n"
    "2. Fill in customer details\n"
    "3. Get instant churn prediction\n"
    "4. View confidence scores"
)

# ============================================================================
# PAGE 1: HOME
# ============================================================================

if page == "🏠 Home":
    st.title("🎯 Customer Churn Prediction System")
    st.markdown("### AI-Powered Predictive Analytics (Optimized Model)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h3>📊 Accuracy</h3>
            <h2>76%</h2>
            <p>Model Performance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h3>⚡ Features</h3>
            <h2>12</h2>
            <p>Optimized Features</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h3>🚀 Speed</h3>
            <h2>Fast</h2>
            <p>Instant Predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 System Overview")
        st.write("""
        This optimized machine learning system predicts customer churn probability 
        using the 12 most important features.
        
        **Key Features:**
        - ✅ Faster predictions with reduced features
        - ✅ Maintains high accuracy (76%)
        - ✅ Real-time predictions with proper feature engineering
        - ✅ Different results for different inputs
        - ✅ Confidence scores
        - ✅ Feature importance analysis
        - ✅ Interactive dashboard
        - ✅ REST API support
        """)
    
    with col2:
        st.subheader("🚀 Quick Stats")
        st.metric("Dataset Size", "7,043 records", "Training Data")
        st.metric("Features Used", "12", "Most important only")
        st.metric("Churn Rate", "26.7%", "Target class")
    
    st.markdown("---")
    st.subheader("📊 Model Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if model is not None:
            st.success("✓ Model Loaded")
        else:
            st.error("✗ Model Not Loaded")
    
    with col2:
        if feature_columns is not None:
            st.success(f"✓ {len(feature_columns)} Features Ready")
        else:
            st.error("✗ Features Not Ready")
    
    with col3:
        if df is not None:
            st.success("✓ Data Available")
        else:
            st.warning("⚠ Data Limited")
    
    st.markdown("---")
    st.subheader("📊 Top 12 Features Used")
    features_df = pd.DataFrame({"Feature": feature_columns})
    st.dataframe(features_df, use_container_width=True)

# ============================================================================
# PAGE 2: MAKE PREDICTION - SIMPLIFIED FOR 12 FEATURES
# ============================================================================

elif page == "🔮 Make Prediction":
    st.title("🔮 Customer Churn Prediction")
    st.markdown("### Enter customer details to get churn prediction")
    
    if model is None or feature_columns is None:
        st.error("❌ Model or features not loaded properly. Check paths and files.")
    else:
        st.success(f"✅ Model Ready | {len(feature_columns)} Features Loaded")
        
        # Create tabs for different input methods
        tab1, tab2 = st.tabs(["📝 Manual Input", "📤 CSV Upload"])
        
        with tab1:
            st.subheader("Customer Information")
            
            # Numeric features
            col1, col2, col3 = st.columns(3)
            
            with col1:
                tenure = st.slider("Tenure (months)", 0, 72, 24)
            
            with col2:
                monthly_charges = st.slider("Monthly Charges ($)", 0.0, 150.0, 65.0)
            
            with col3:
                total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 1500.0)
            
            # Categorical features
            col1, col2, col3 = st.columns(3)
            
            with col1:
                internet_service = st.selectbox("Internet Service", 
                    ["No", "DSL", "Fiber optic"])
                contract = st.selectbox("Contract Type", 
                    ["Month-to-month", "One year", "Two year"])
                gender = st.selectbox("Gender", ["Male", "Female"])
            
            with col2:
                online_security = st.selectbox("Online Security", 
                    ["No", "Yes", "No internet service"])
                tech_support = st.selectbox("Tech Support", 
                    ["No", "Yes", "No internet service"])
                paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"])
            
            with col3:
                online_backup = st.selectbox("Online Backup", 
                    ["No", "Yes", "No internet service"])
                payment_method = st.selectbox("Payment Method",
                    ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
                multiple_lines = st.selectbox("Multiple Lines", 
                    ["No", "Yes", "No phone service"])
            
            # Prediction button
            if st.button("🎯 Predict Churn", key="predict_btn", use_container_width=True):
                try:
                    # Create input DataFrame with 12 features
                    input_dict = {}
                    
                    # Map user inputs to feature names
                    for feat in feature_columns:
                        if feat == 'tenure':
                            input_dict[feat] = tenure
                        elif feat == 'MonthlyCharges':
                            input_dict[feat] = monthly_charges
                        elif feat == 'TotalCharges':
                            input_dict[feat] = total_charges
                        elif feat == 'Contract':
                            input_dict[feat] = contract
                        elif feat == 'InternetService':
                            input_dict[feat] = internet_service
                        elif feat == 'OnlineSecurity':
                            input_dict[feat] = online_security
                        elif feat == 'TechSupport':
                            input_dict[feat] = tech_support
                        elif feat == 'OnlineBackup':
                            input_dict[feat] = online_backup
                        elif feat == 'PaperlessBilling':
                            input_dict[feat] = paperless_billing
                        elif feat == 'PaymentMethod':
                            input_dict[feat] = payment_method
                        elif feat == 'gender':
                            input_dict[feat] = gender
                        elif feat == 'MultipleLines':
                            input_dict[feat] = multiple_lines
                    
                    # Create DataFrame
                    input_df = pd.DataFrame([input_dict])
                    
                    # Verify we have all 12 features
                    if len(input_df.columns) != len(feature_columns):
                        st.error(f"Feature count mismatch! Expected {len(feature_columns)}, got {len(input_df.columns)}")
                    else:
                        # Make prediction
                        prediction = model.predict(input_df)[0]
                        probability = model.predict_proba(input_df)[0]
                        
                        churn_prob = probability[1]
                        no_churn_prob = probability[0]

                        if churn_prob >= 0.70:
                            risk_level = "HIGH RISK"
                            risk_css = "prediction-high-risk"
                            risk_feedback = f"⚠️ This customer has a HIGH RISK of churning ({churn_prob*100:.1f}%)"
                        elif churn_prob >= 0.35:
                            risk_level = "MEDIUM RISK"
                            risk_css = "info-box"
                            risk_feedback = f"⚠️ This customer has a MEDIUM RISK of churning ({churn_prob*100:.1f}%)"
                        else:
                            risk_level = "LOW RISK"
                            risk_css = "prediction-stable"
                            risk_feedback = f"✅ This customer has a LOW RISK of churning ({churn_prob*100:.1f}%)"
                        
                        # Display results
                        st.markdown("---")
                        st.subheader("🎯 Prediction Results")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if churn_prob >= 0.70:
                                st.markdown(f"""
                                <div class="prediction-high-risk">
                                ⚠️ HIGH RISK<br/>
                                <br/>
                                {churn_prob*100:.1f}% Churn Probability
                                </div>
                                """, unsafe_allow_html=True)
                                st.warning(risk_feedback)
                            elif churn_prob >= 0.35:
                                st.markdown(f"""
                                <div class="info-box">
                                🟡 MEDIUM RISK<br/>
                                <br/>
                                {churn_prob*100:.1f}% Churn Probability
                                </div>
                                """, unsafe_allow_html=True)
                                st.info(risk_feedback)
                            else:
                                st.markdown(f"""
                                <div class="prediction-stable">
                                ✅ LOW RISK<br/>
                                <br/>
                                {churn_prob*100:.1f}% Churn Probability
                                </div>
                                """, unsafe_allow_html=True)
                                st.success(risk_feedback)
                        
                        with col2:
                            # Show probabilities
                            st.metric("Churn Probability", f"{churn_prob*100:.2f}%")
                            st.metric("Retention Probability", f"{no_churn_prob*100:.2f}%")
                        
                        # Feature importance for this prediction
                        st.markdown("---")
                        st.subheader("📊 Customer Profile")
                        
                        profile_data = pd.DataFrame({
                            "Feature": feature_columns,
                            "Value": [input_dict.get(feat, "N/A") for feat in feature_columns]
                        })
                        st.dataframe(profile_data, use_container_width=True)

                        st.markdown("---")
                        st.subheader("📬 Automated Retention Email")

                        if churn_prob >= 0.35:
                            with st.spinner("Generating personalized retention email..."):
                                email_campaign = call_llm_retention_api(
                                    tenure=tenure,
                                    contract=contract,
                                    charges=monthly_charges,
                                    churn_score=churn_prob,
                                )

                            st.text_area(
                                label="Email draft",
                                value=email_campaign,
                                height=240,
                                label_visibility="collapsed",
                                key="retention_email_template",
                            )
                        else:
                            st.info("This customer is low risk, so no automated retention email was generated.")
                
                except Exception as e:
                    st.error(f"❌ Error during prediction: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())

# ============================================================================
# PAGE 3: ANALYTICS
# ============================================================================

elif page == "📊 Analytics":
    st.title("📊 Analytics & Model Performance")
    
    if df is not None:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Customers", len(df))
        
        with col2:
            churn_count = (df['Churn'] == 'Yes').sum() if 'Churn' in df.columns else 0
            st.metric("Churned", churn_count)
        
        with col3:
            churn_rate = (churn_count / len(df) * 100) if len(df) > 0 else 0
            st.metric("Churn Rate", f"{churn_rate:.2f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Model Improvements")
            st.write("""
            **Optimization Benefits:**
            - ✅ Reduced features: 30 → 12
            - ✅ Faster predictions
            - ✅ Maintained accuracy: 76%
            - ✅ Easier to interpret
            - ✅ Better performance
            - ✅ Reduced overfitting risk
            """)
        
        with col2:
            st.subheader("Model Metrics")
            st.write("""
            **Performance on Test Set:**
            - Accuracy: 76%
            - ROC-AUC: 0.7768
            - Precision: 56.56%
            - Recall: 48.40%
            """)
    else:
        st.warning("Data not available")

# ============================================================================
# PAGE 4: ABOUT MODEL
# ============================================================================

elif page == "ℹ️ About Model":
    st.title("ℹ️ About the Model")
    
    st.subheader("🔧 Model Architecture")
    st.write("""
    - **Algorithm**: Multi-Layer Perceptron (MLPClassifier)
    - **Hidden Layers**: 32 → 16 → 8 neurons
    - **Activation**: ReLU
    - **Solver**: Adam Optimizer
    - **Input Features**: 12 (most important only)
    """)
    
    st.subheader("📊 Training Data")
    st.write(f"""
    - **Total Records**: 7,043
    - **Training Set**: 4,278 (60%)
    - **Validation Set**: 1,426 (20%)
    - **Test Set**: 705 (10%)
    - **Holdout Set**: 634 (10%)
    """)
    
    st.subheader("🎯 Top 12 Features")
    if feature_columns:
        for i, feat in enumerate(feature_columns, 1):
            st.write(f"{i}. {feat}")
    
    st.subheader("📈 Why These Features?")
    st.write("""
    These 12 features were selected using feature importance analysis:
    - Account tenure and charges are strong predictors
    - Service types indicate customer engagement
    - Support options show customer care investment
    - Contract type reflects customer commitment
    - Payment method affects satisfaction
    """)
    
    st.subheader("✅ Model Validation")
    st.write("""
    - Model trained on 60% of data
    - Validated on 20% of data
    - Tested on 10% of data
    - Holdout set (10%) used for final verification
    - All sets maintain same churn rate (~26.7%)
    """)

st.markdown("---")
st.caption("🎯 Customer Churn Prediction System | Powered by ML | Optimized with 12 Features")
