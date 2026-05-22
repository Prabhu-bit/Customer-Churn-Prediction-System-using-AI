"""Customer Churn Streamlit App - stable runtime + human-style visuals."""

import hashlib
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import requests
import streamlit as st
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score, roc_curve

# Ensure project root imports work no matter where streamlit is launched from.
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from reduced_model_utils import prepare_reduced_model_input
from evaluation_utils import evaluate_bundle

st.set_page_config(page_title="Customer Churn Predictor", page_icon="🛡️", layout="wide")

def apply_theme_css() -> None:
    css = """
    <style>
    .stApp { background:#f8fafc; color:#0f172a; }
    .stApp, .stApp * { color:#0f172a; }
    section[data-testid="stSidebar"] { background:#ffffff; border-right:1px solid #e2e8f0; }
    section[data-testid="stSidebar"] * { color:#0f172a; }
    .stButton > button {
        background:#dbeafe;
        color:#0f172a;
        border:1px solid #93c5fd;
        border-radius:10px;
        padding:0.6rem 1rem;
        box-shadow:none;
    }
    .stButton > button:hover {
        background:#bfdbfe;
        color:#0f172a;
        border:1px solid #60a5fa;
    }
    .stButton > button:focus {
        box-shadow:0 0 0 0.15rem rgba(96,165,250,.25);
        outline:none;
    }
    .stSelectbox div[data-baseweb="select"],
    .stMultiSelect div[data-baseweb="select"],
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stSlider [data-baseweb="slider"] { color:#0f172a; }
    div[data-baseweb="select"] > div,
    .stSelectbox [role="combobox"],
    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea {
        background:#ffffff;
        border-color:#cbd5e1;
    }
    div[data-baseweb="select"] > div:hover,
    .stTextInput input:hover,
    .stNumberInput input:hover,
    .stTextArea textarea:hover {
        border-color:#93c5fd;
    }
    .metric-card { background:linear-gradient(135deg,#0284c7,#0ea5e9); color:#fff; border-radius:12px; padding:12px; text-align:center; }
    .risk-low { background:#dcfce7; border:2px solid #22c55e; color:#14532d; border-radius:12px; padding:18px; text-align:center; font-size:22px; font-weight:700; }
    .risk-medium { background:#ffedd5; border:2px solid #f97316; color:#7c2d12; border-radius:12px; padding:18px; text-align:center; font-size:22px; font-weight:700; }
    .risk-high { background:#fee2e2; border:2px solid #ef4444; color:#7f1d1d; border-radius:12px; padding:18px; text-align:center; font-size:22px; font-weight:700; }
    hr { border-color:#e2e8f0; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


apply_theme_css()

AUTH_DB_PATH = ROOT_DIR / "user_auth.db"


def _clean_username(username: str) -> str:
    return username.strip()


def _password_hash(password: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()


def _get_auth_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(AUTH_DB_PATH)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    return connection


def create_user_account(username: str, password: str) -> tuple[bool, str]:
    username = _clean_username(username)
    if not username or not password:
        return False, "Please enter both username and password."

    with _get_auth_connection() as connection:
        existing_user = connection.execute(
            "SELECT username FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if existing_user:
            return False, "Username already exists. Please sign in instead."

        salt = os.urandom(16).hex()
        connection.execute(
            "INSERT INTO users (username, password_hash, salt, created_at) VALUES (?, ?, ?, ?)",
            (username, _password_hash(password, salt), salt, datetime.utcnow().isoformat()),
        )
        connection.commit()

    return True, "Account created successfully. Please sign in."


def verify_user_account(username: str, password: str) -> tuple[bool, str]:
    username = _clean_username(username)
    if not username or not password:
        return False, "Please enter both username and password."

    with _get_auth_connection() as connection:
        row = connection.execute(
            "SELECT password_hash, salt FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if row is None:
        return False, "Wrong username or password."

    password_hash, salt = row
    if _password_hash(password, salt) != password_hash:
        return False, "Wrong username or password."

    return True, "Login successful."


def initialize_auth_state() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Sign in"


def show_auth_toast(message: str, level: str) -> None:
    icon_map = {"success": "✅", "error": "❌", "info": "ℹ️"}
    st.toast(message, icon=icon_map.get(level, "ℹ️"))


def show_login_screen() -> None:
    st.title("Secure Login")
    st.caption("Sign in to access the dashboard. New users can create an account.")

    _, form_col, _ = st.columns([1, 1.25, 1])
    with form_col:
        with st.form("auth_form", clear_on_submit=False):
            auth_mode = st.radio("Action", ["Sign in", "Create account"], horizontal=True, key="auth_mode")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", placeholder="Enter your password", type="password")
            submitted = st.form_submit_button("Continue", use_container_width=True)

    if submitted:
        if auth_mode == "Create account":
            success, message = create_user_account(username, password)
        else:
            success, message = verify_user_account(username, password)

        if success and auth_mode == "Sign in":
            show_auth_toast(message, "success")
            st.session_state.authenticated = True
            st.session_state.username = _clean_username(username)
            st.rerun()

        if success and auth_mode == "Create account":
            show_auth_toast(message, "success")
            st.session_state.auth_mode = "Sign in"
        else:
            show_auth_toast(message, "error")


def render_authenticated_sidebar() -> None:
    st.sidebar.title("Customer Churn")
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Signed in as:** {st.session_state.username}")
    if st.sidebar.button("Log out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        show_auth_toast("Logged out successfully.", "info")
        st.rerun()
    st.sidebar.markdown("---")


@st.cache_resource
def load_assets():
    model_path = ROOT_DIR / "07_Models_Trained" / "final_optimized_churn_model_reduced.pkl"
    metadata_path = ROOT_DIR / "07_Models_Trained" / "model_metadata.json"
    test_path = ROOT_DIR / "05_Data_Splits" / "test_split.csv"

    bundle = joblib.load(model_path)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    test_df = pd.read_csv(test_path)
    return bundle, metadata, test_df


@st.cache_data
def evaluate(_bundle, test_df):
    return evaluate_bundle(_bundle, test_df)


def format_metric_value(value, decimals=3):
    return "N/A" if pd.isna(value) else f"{value:.{decimals}f}"


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")


def _build_retention_email_fallback(tenure: int, contract: str, charges: float, churn_score: float, risk_level: str) -> str:
    if risk_level == "high":
        return (
            "Subject: A personal check-in about your account\n\n"
            "Hi there,\n\n"
            f"I noticed your {contract} plan and wanted to reach out directly because you have been with us for {tenure} months. "
            f"With your current bill at ${charges:.2f} per month, I would like to review a few stronger retention options with you before any final decision is made. "
            "If you are open to a quick conversation, reply with a suitable time and I will handle the rest personally.\n\n"
            "Kind regards,\n"
            "Your Customer Care Team"
        )

    return (
        "Subject: A quick plan review for your account\n\n"
        "Hi there,\n\n"
        f"Thanks for staying with us for {tenure} months on the {contract} plan. "
        f"At ${charges:.2f} per month, your account may benefit from a brief review, and I would be glad to go over a couple of practical options that could make the service a better fit. "
        "If you'd like, reply and I can help you look at a lower-cost or more useful plan.\n\n"
        "Warm regards,\n"
        "Your Customer Care Team"
    )


def call_llm_retention_api(tenure, contract, charges, churn_score, risk_level):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _build_retention_email_fallback(tenure, contract, charges, churn_score, risk_level)

    if risk_level == "high":
        style_guidance = (
            "Use a more urgent but still respectful tone. Make the message feel like a personal escalation from a real account manager. "
            "Focus on keeping the customer, offering a direct review call, and making the next step easy."
        )
    else:
        style_guidance = (
            "Use a softer, friendly tone. Make the message feel like a genuine check-in from a helpful support representative. "
            "Focus on a practical plan review, billing help, or a small adjustment that improves value."
        )

    prompt = f"""
Write a natural, human-sounding retention email that reads like it was written by an experienced account manager, not an AI tool.

Customer profile:
- Contract type: {contract}
- Account tenure: {tenure} months
- Monthly charges: ${charges:.2f}
- Churn risk score: {churn_score * 100:.1f}%
- Risk bucket: {risk_level}

Requirements:
- {style_guidance}
- Keep the subject line different for medium and high risk.
- Refer to the customer's contract, tenure, and price in a natural way.
- Avoid generic AI phrases such as "we value your business", "our system has flagged", or "retention offer".
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
            message = choices[0].get("message", {})
            content = message.get("content", "").strip()
            if content:
                return content
    except Exception:
        pass

    return _build_retention_email_fallback(tenure, contract, charges, churn_score, risk_level)


initialize_auth_state()

if not st.session_state.authenticated:
    show_login_screen()
    st.stop()

bundle, metadata, test_df = load_assets()
model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]
metrics, cm, fpr, tpr, y_prob = evaluate(bundle, test_df)

render_authenticated_sidebar()

page = st.sidebar.radio("Navigate", ["Home", "Make Prediction", "Analytics", "Model & Diagrams"])

if page == "Home":
    st.title("Customer Churn Prediction System")
    st.markdown("## About this project")
    st.write("This project predicts customer churn using a reduced 12-feature MLPClassifier. The Streamlit UI provides a simple prediction interface and visual analytics. The documentation contains full evaluation details and corrected visual assets.")
    st.info("LLM support is built into the Make Prediction tab. After prediction, the app can generate a human-style retention email that changes with the customer's risk level.")
    st.caption("High-risk customers get a more direct retention note, while medium-risk customers get a softer review-style message.")
    st.markdown("## About the model")
    st.write("- Model type: MLPClassifier (scikit-learn)\n- Feature set: 12 selected features (reduced pipeline)\n- The trained model bundle is stored in the project's models folder.\n- In-app predictions use the shared preprocessing utility to ensure consistent inputs.")
    st.markdown("---")

elif page == "Make Prediction":
    st.title("Make Prediction")
    col1, col2, col3 = st.columns(3)

    with col1:
        tenure = st.slider("Tenure (months)", 0, 72, 24)
        monthly = st.slider("Monthly Charges", 0.0, 150.0, 70.0)
        total = st.number_input("Total Charges", 0.0, 15000.0, 1700.0)

    with col2:
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
        internet = st.selectbox("Internet Service", ["No", "DSL", "Fiber optic"])

    with col3:
        tech = st.selectbox("Tech Support", ["No", "Yes"])
        security = st.selectbox("Online Security", ["No", "Yes"])
        backup = st.selectbox("Online Backup", ["No", "Yes"])

    col4, col5, col6 = st.columns(3)
    with col4:
        paperless = st.selectbox("Paperless Billing", ["No", "Yes"])
    with col5:
        gender = st.selectbox("Gender", ["Female", "Male"])
    with col6:
        multiple = st.selectbox("Multiple Lines", ["No", "Yes"])

    if st.button("Predict Churn", use_container_width=True):
        payload = {
            "TotalCharges": total,
            "MonthlyCharges": monthly,
            "tenure": tenure,
            "Contract": contract,
            "PaymentMethod": payment,
            "TechSupport": tech,
            "OnlineSecurity": security,
            "PaperlessBilling": paperless,
            "InternetService": internet,
            "gender": gender,
            "OnlineBackup": backup,
            "MultipleLines": multiple,
        }
        input_df = prepare_reduced_model_input(payload, features)
        scaled = scaler.transform(input_df)
        pred = model.predict(scaled)[0]
        prob = model.predict_proba(scaled)[0]
        yes_idx = list(model.classes_).index("Yes") if "Yes" in model.classes_ else 1
        churn_prob = float(prob[yes_idx])

        if churn_prob >= 0.70:
            css = "risk-high"
            risk_label = "HIGH RISK"
        elif churn_prob >= 0.35:
            css = "risk-medium"
            risk_label = "MEDIUM RISK"
        else:
            css = "risk-low"
            risk_label = "LOW RISK"

        st.markdown("---")
        st.markdown(f"<div class='{css}' style='font-size:24px;padding:18px'>{risk_label}<br/>{churn_prob*100:.1f}%</div>", unsafe_allow_html=True)
        st.write(f"Predicted class: {'Churn' if str(pred) == 'Yes' else 'No Churn'}")

        st.markdown("---")
        st.subheader("📬 Automated Retention Email")

        if churn_prob >= 0.35:
            risk_level = "high" if churn_prob >= 0.7 else "medium"
            with st.spinner("Generating personalized retention email..."):
                email_campaign = call_llm_retention_api(
                    tenure=tenure,
                    contract=contract,
                    charges=monthly,
                    churn_score=churn_prob,
                    risk_level=risk_level,
                )

            st.text_area(
                "Email draft",
                value=email_campaign,
                height=240,
                label_visibility="collapsed",
                key="retention_email_template",
            )
        else:
            st.info("This customer is low risk, so no automated retention email was generated.")

elif page == "Analytics":
    st.title("Analytics")
    st.markdown("### Model Evaluation")
    
    for image in [
        ROOT_DIR / "03_Visualizations_Charts" / "human_01_model_metrics.png",
        ROOT_DIR / "03_Visualizations_Charts" / "human_02_confusion_matrix.png",
        ROOT_DIR / "03_Visualizations_Charts" / "human_03_roc_curve.png",
    ]:
        if image.exists():
            st.image(str(image), use_container_width=True)

else:
    st.title("Model Visualizations")
    st.caption("Feature and model charts (diagrams removed from this view)")

    st.subheader("Feature / Model Charts")
    for image in [
        ROOT_DIR / "03_Visualizations_Charts" / "human_05_feature_selection_impact.png",
        ROOT_DIR / "03_Visualizations_Charts" / "human_06_permutation_importance.png",
        ROOT_DIR / "03_Visualizations_Charts" / "human_07_class_distribution.png",
    ]:
        if image.exists():
            st.image(str(image), use_container_width=True)

st.markdown("---")
st.caption("Customer Churn Dashboard | Reduced 12-feature model | Updated visuals")
