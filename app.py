
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import re
import os
from datetime import datetime
from text_preprocessing import normalize_text


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Sentinel AI | Scam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #18264a 0%, transparent 40%),
        radial-gradient(ellipse at 90% 15%, #242044 0%, transparent 35%),
        #080d1b;
    color: #edf3ff;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.hero {
    text-align: center;
    padding: 45px 20px 35px;
    border: 1px solid rgba(125, 155, 255, 0.18);
    border-radius: 28px;
    background: linear-gradient(
        135deg,
        rgba(28, 43, 78, 0.82),
        rgba(24, 18, 48, 0.80)
    );
    box-shadow: 0 15px 60px rgba(0, 0, 0, 0.22);
    margin-bottom: 28px;
}

.shield {
    font-size: 62px;
    filter: drop-shadow(0 0 18px rgba(68, 220, 255, 0.55));
    margin-bottom: 8px;
}

.hero h1 {
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 0;
    color: #ffffff;
}

.gradient-text {
    background: linear-gradient(90deg, #50e6ff, #a89aff, #f0a7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #b5c3e4;
    font-size: 16px;
    line-height: 1.8;
    max-width: 680px;
    margin: 16px auto 0;
}

.status-pill {
    display: inline-block;
    margin-top: 22px;
    padding: 8px 16px;
    border-radius: 30px;
    color: #78f5c5;
    background: rgba(45, 220, 155, 0.09);
    border: 1px solid rgba(45, 220, 155, 0.25);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.section-heading {
    font-size: 23px;
    font-weight: 750;
    color: #f3f6ff;
    margin: 15px 0 7px;
}

.section-description {
    color: #99a9cb;
    font-size: 14px;
    margin-bottom: 20px;
}

.metric-card {
    background: linear-gradient(
        145deg,
        rgba(27, 39, 69, 0.92),
        rgba(17, 25, 46, 0.92)
    );
    border: 1px solid rgba(133, 159, 230, 0.18);
    border-radius: 18px;
    padding: 22px;
    min-height: 130px;
    margin-bottom: 12px;
}

.metric-label {
    font-size: 12px;
    color: #9daed0;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    font-size: 27px;
    color: #ffffff;
    font-weight: 800;
    margin-top: 12px;
}

.metric-note {
    color: #7de9cb;
    font-size: 12px;
    margin-top: 5px;
}

.scan-panel {
    background: rgba(17, 26, 48, 0.88);
    border: 1px solid rgba(132, 159, 226, 0.22);
    border-radius: 24px;
    padding: 28px;
    margin: 15px 0 25px;
}

.stTextArea textarea {
    background: #0b1326 !important;
    color: #f1f5ff !important;
    border: 1px solid #35466d !important;
    border-radius: 14px !important;
    font-size: 15px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #6c91ff !important;
    box-shadow: 0 0 0 2px rgba(108, 145, 255, 0.15) !important;
}

.stButton > button {
    width: 100%;
    border: none;
    border-radius: 12px;
    min-height: 48px;
    font-size: 15px;
    font-weight: 750;
    color: #071126;
    background: linear-gradient(90deg, #55e6f7, #a99aff);
    transition: 0.2s ease;
}

.stButton > button:hover {
    box-shadow: 0 0 25px rgba(91, 188, 255, 0.25);
    transform: translateY(-1px);
    color: #071126;
}

.result-card {
    border-radius: 20px;
    padding: 25px;
    margin-top: 20px;
    margin-bottom: 20px;
}

.result-safe {
    background: linear-gradient(
        135deg,
        rgba(20, 103, 82, 0.30),
        rgba(13, 45, 54, 0.70)
    );
    border: 1px solid rgba(64, 233, 177, 0.45);
}

.result-danger {
    background: linear-gradient(
        135deg,
        rgba(136, 42, 68, 0.36),
        rgba(55, 22, 48, 0.75)
    );
    border: 1px solid rgba(255, 99, 143, 0.48);
}

.result-title {
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 10px;
}

.result-description {
    color: #d1d9ed;
    line-height: 1.7;
    font-size: 14px;
}

.info-card {
    background: rgba(22, 32, 57, 0.78);
    border: 1px solid rgba(125, 151, 215, 0.16);
    border-radius: 16px;
    padding: 20px;
    min-height: 130px;
    margin-bottom: 12px;
}

.info-card h4 {
    color: #eaf0ff;
    margin-top: 0;
    font-size: 16px;
}

.info-card p {
    color: #a8b7d5;
    line-height: 1.7;
    font-size: 13px;
}

.footer {
    text-align: center;
    color: #7889ac;
    font-size: 12px;
    line-height: 1.9;
    padding-top: 30px;
    border-top: 1px solid rgba(125, 151, 215, 0.13);
    margin-top: 35px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

@media (max-width: 700px) {
    .hero {
        padding: 30px 15px;
    }

    .scan-panel {
        padding: 17px;
    }

    .metric-value {
        font-size: 23px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD MODEL ----------------

MODEL_PATH = "models/multilingual_scam_detector.pkl"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception:
    model = None


# ---------------- ANALYSIS RULES ----------------

SCAM_INDICATORS = {
    "otp": "OTP or security code mentioned",
    "password": "Password-related content",
    "prize": "Prize or reward claim",
    "inaam": "Prize or reward claim",
    "lottery": "Lottery-related content",
    "claim": "Reward claim language",
    "payment": "Payment-related language",
    "fee": "Fee or charges mentioned",
    "transfer": "Money transfer language",
    "blocked": "Account-blocking warning",
    "verify": "Verification request",
    "verification": "Verification request",
    "urgent": "Urgency-related language",
    "congratulations": "Possible reward claim",
    "link": "Link-related language",
    "pin": "PIN or security code mentioned",
    "passcode": "Passcode mentioned"
}

PROTECTIVE_PHRASES = [
    "never share",
    "do not share",
    "dont share",
    "never disclose",
    "do not disclose",
    "never send",
    "do not send",
    "keep your password private",
    "kabhi share na karein",
    "kabhi share na karen",
    "kisi ko na batayein",
    "kisi ko mat batayein",
    "share na karein",
    "share na karen",
    "mat share karein"
]

REQUEST_WORDS = {
    "send", "share", "provide", "enter", "reply", "give",
    "tell", "submit", "confirm", "provide", "bhejein",
    "batayein", "likhein", "darj"
}


def analyze_indicators(message):
    normalized = normalize_text(message)
    words = set(normalized.split())
    indicators = []

    protective = any(
        phrase in normalized
        for phrase in PROTECTIVE_PHRASES
    )

    credentials = {
        "otp", "password", "pin", "passcode"
    } & words

    request_present = bool(REQUEST_WORDS & words)

    if credentials:
        if protective:
            indicators.append(
                "Safety advice: message discourages sharing credentials."
            )
        elif request_present:
            indicators.append(
                "Possible request for a password, OTP, PIN, or security code."
            )
        else:
            indicators.append(
                "Credential-related words detected; review the context."
            )

    for word, explanation in SCAM_INDICATORS.items():
        if word in words:
            if word in {"otp", "password", "pin", "passcode"}:
                continue
            indicators.append(explanation)

    if not indicators:
        indicators.append(
            "No predefined indicators detected. This does not guarantee safety."
        )

    return indicators



# ---------------- MODEL EXPLANATION (XAI) ----------------

def explain_prediction(normalized_message, top_n=6):
    import numpy as np

    features = model.named_steps["features"]
    classifier = model.named_steps["classifier"]

    feature_names = features.get_feature_names_out()
    weights = classifier.coef_[0]
    transformed = features.transform([normalized_message])
    contributions = transformed.multiply(weights).toarray()[0]

    def get_features(indices, positive):
        results = []
        for i in indices:
            value = contributions[i]
            if positive and value <= 0:
                break
            if not positive and value >= 0:
                break

            name = feature_names[i]
            if not name.startswith("word_tfidf__"):
                continue

            name = name.replace("word_tfidf__", "")
            results.append((name, float(value)))
            if len(results) >= top_n:
                break
        return results

    positive_indices = np.argsort(contributions)[::-1]
    negative_indices = np.argsort(contributions)

    return (
        get_features(positive_indices, True),
        get_features(negative_indices, False)
    )


# ---------------- HERO ----------------

st.markdown("""
<div class="hero">
    <div class="shield"></div>
    <h1>Sentinel <span class="gradient-text">AI</span></h1>
    <p>
        Your intelligent first line of defense against scam and phishing messages.
        Analyze suspicious texts, understand warning signs, and make safer decisions
        with multilingual message detection.
    </p>
    <div class="status-pill"> MULTILINGUAL SECURITY ANALYSIS</div>
</div>
""", unsafe_allow_html=True)


# ---------------- MODEL STATUS ----------------

if model is None:
    st.error(
        "The trained model could not be loaded. "
        "Please check models/multilingual_scam_detector.pkl."
    )
    st.stop()



# ---------------- METRICS ----------------

metrics_path = "results/dashboard_model_metrics.csv"

try:
    evaluation_df = pd.read_csv(metrics_path)
    svm_row = evaluation_df[evaluation_df["Model"] == "Linear SVM"]

    if not svm_row.empty:
        svm_accuracy = f"{float(svm_row.iloc[0]['Accuracy (%)']):.2f}%"
        accuracy_note = "Held-out test set"
    else:
        svm_accuracy = "N/A"
        accuracy_note = "Run dashboard_evaluation.py"

except (FileNotFoundError, pd.errors.EmptyDataError, KeyError, ValueError):
    evaluation_df = pd.DataFrame()
    svm_accuracy = "N/A"
    accuracy_note = "Run dashboard_evaluation.py"


c1, c2, c3, c4 = st.columns(4)

metrics = [
    (c1, "TEST ACCURACY", svm_accuracy, accuracy_note),
    (c2, "LANGUAGE INPUT", "Multilingual", "English + Roman Urdu"),
    (c3, "MODEL", "Linear SVM", "Word + character TF-IDF"),
    (c4, "ANALYSIS", "Instant", "Local model prediction")
]

for col, label, value, note in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)





# ---------------- MODEL PERFORMANCE DASHBOARD ----------------

st.markdown("---")
st.markdown(
    '<div class="section-heading">Model Performance Dashboard</div>',
    unsafe_allow_html=True
)

if not evaluation_df.empty:
    st.markdown("#### Model Comparison")

    display_columns = [
        "Model",
        "Accuracy (%)",
        "Precision (scam)",
        "Recall (scam)",
        "F1-score (scam)"
    ]

    available_columns = [
        col for col in display_columns if col in evaluation_df.columns
    ]

    st.dataframe(
        evaluation_df[available_columns].round(2),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("#### Accuracy Comparison")

    chart_df = evaluation_df[["Model", "Accuracy (%)"]].copy()
    chart_df = chart_df.set_index("Model")

    st.bar_chart(chart_df, y="Accuracy (%)")

    st.caption(
        "Results are calculated on a held-out test dataset. "
        "Run dashboard_evaluation.py to update the evaluation results."
    )

else:
    st.warning(
        "Evaluation results are unavailable. "
        "Please run dashboard_evaluation.py first."
    )


# ---------------- MESSAGE SCANNER ----------------

st.markdown('<div class="section-heading"> Message Security Scanner</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="section-description">
Paste a suspicious SMS, message, or notification below to analyze it.
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("#### Analyze a message")

    message = st.text_area(
        "Message to analyze",
        placeholder=(
            "Example: Your account will be blocked. "
            "Send your OTP immediately to restore access."
        ),
        height=150,
        max_chars=5000,
        label_visibility="collapsed"
    )

    left, right = st.columns([3, 1])

    with left:
        st.caption(
            " Avoid entering real passwords, OTPs, account numbers, "
            "or other private information."
        )

    with right:
        scan_clicked = st.button(
            " Scan Message",
            use_container_width=True
        )


# ---------------- SCAN RESULT ----------------

if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

if scan_clicked:
    if not message.strip():
        st.warning("Please enter a message before scanning.")
    else:
        try:
            normalized_message = normalize_text(message)
            prediction = model.predict([normalized_message])[0]
            indicators = analyze_indicators(message)

            is_scam = str(prediction).lower() == "scam"

            st.markdown("---")
            st.markdown(
                '<div class="section-heading"> Scan Results</div>',
                unsafe_allow_html=True
            )

            if is_scam:
                st.markdown("""
                <div class="result-card result-danger">
                    <div class="result-title">
                         SCAM / SUSPICIOUS MESSAGE
                    </div>
                    <div class="result-description">
                        The machine learning model classified this message
                        as suspicious. Do not share sensitive information
                        or follow payment instructions without independently
                        verifying the sender.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown("""
                <div class="result-card result-safe">
                    <div class="result-title">
                         CLASSIFIED AS NORMAL
                    </div>
                    <div class="result-description">
                        The machine learning model classified this message
                        as normal. This is not a guarantee of safety.
                        Remain careful with unexpected links and requests
                        for personal information.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            result_left, result_right = st.columns(2)

            with result_left:
                st.markdown("####  Message indicators")
                for item in indicators:
                    st.markdown(f"- {item}")

            with result_right:
                st.markdown("####  Recommended action")

                if is_scam:
                    st.warning(
                        "Verify the sender through an official channel. "
                        "Do not share your OTP, password, PIN, or banking details."
                    )
                else:
                    st.info(
                        "Check the sender and context. Avoid unexpected links "
                        "and never disclose confidential information."
                    )

            with st.expander("Why did AI make this prediction?"):
                st.write(
                    "These are word features that contributed to the model's "
                    "decision score. They are not proof that a message is fraudulent."
                )

                supporting, opposing = explain_prediction(normalized_message)

                col_scam, col_normal = st.columns(2)

                with col_scam:
                    st.markdown("**Features supporting SCAM**")
                    if supporting:
                        for word, score in supporting:
                            st.write(f"`{word}`: +{score:.4f}")
                    else:
                        st.write("No positive word contributions found.")

                with col_normal:
                    st.markdown("**Features supporting NORMAL**")
                    if opposing:
                        for word, score in opposing:
                            st.write(f"`{word}`: {score:.4f}")
                    else:
                        st.write("No negative word contributions found.")

            with st.expander("View normalized text"):
                st.code(normalized_message)

            st.caption(
                "Indicators are heuristic keyword/context checks, not a direct "
                "explanation of the ML model's internal reasoning."
            )

            st.session_state.scan_history.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "message": message[:100],
                "prediction": "SCAM / SUSPICIOUS" if is_scam else "NORMAL"
            })

            st.session_state.scan_history = (
                st.session_state.scan_history[:5]
            )

        except Exception as error:
            st.error(
                "The message could not be analyzed. "
                "Please check the model and preprocessing files."
            )
            with st.expander("Technical details"):
                st.code(str(error))


# ---------------- SAMPLE MESSAGES ----------------

st.markdown("---")
st.markdown(
    '<div class="section-heading"> Try a sample message</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="section-description">
Use an example to understand how the scanner works.
</div>
""", unsafe_allow_html=True)

sample1, sample2 = st.columns(2)

with sample1:
    st.markdown("""
    <div class="info-card">
        <h4> Suspicious example</h4>
        <p>
        Your account will be blocked. Send your OTP immediately
        to restore access.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Try suspicious example"):
        st.session_state.sample_message = (
            "Your account will be blocked. "
            "Send your OTP immediately to restore access."
        )
        st.rerun()

with sample2:
    st.markdown("""
    <div class="info-card">
        <h4> Normal example</h4>
        <p>
        Your account is safe. Never share your password with anyone.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Try normal example"):
        st.session_state.sample_message = (
            "Your account is safe. Never share your password with anyone."
        )
        st.rerun()


# Keep selected sample available in session state
if "sample_message" in st.session_state:
    st.info(
        "Sample selected. Copy the example into the scanner above, "
        "then click Scan Message."
    )
    st.code(st.session_state.sample_message)


# ---------------- RECENT SCANS ----------------

if st.session_state.scan_history:
    st.markdown("---")
    st.markdown(
        '<div class="section-heading"> Recent Scans</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Recent scans are stored only in this active Streamlit session."
    )

    for item in st.session_state.scan_history:
        with st.container(border=True):
            st.caption(item["time"])
            st.write(item["message"])
            st.write(f"**Result:** {item['prediction']}")


# ---------------- ABOUT ----------------

st.markdown("---")
st.markdown(
    '<div class="section-heading"> Built for Safer Digital Communication</div>',
    unsafe_allow_html=True
)

a, b, c = st.columns(3)

with a:
    st.markdown("""
    <div class="info-card">
        <h4> Machine Learning</h4>
        <p>
        Linear SVM with word and character TF-IDF features
        for text classification.
        </p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="info-card">
        <h4> Multilingual Input</h4>
        <p>
        Designed to analyze English, Roman Urdu, and mixed-language
        messages represented in the training data.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="info-card">
        <h4> Privacy Awareness</h4>
        <p>
        The app runs its prediction locally using the loaded model.
        Avoid entering real confidential information.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    <strong>Sentinel AI</strong> · Scam & Phishing Detector<br>
    Machine Learning Project · English + Roman Urdu<br><br>
    This tool is an aid, not a guarantee. Always verify suspicious messages
    through trusted official channels.
</div>
""", unsafe_allow_html=True)

