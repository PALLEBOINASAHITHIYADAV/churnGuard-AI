import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.data_agent import DataAgent
from src.model_agent import ModelAgent
from src.alert_agent import AlertAgent

st.set_page_config(page_title="ChurnGuard AI", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .alert-card {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f44336;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🔍 ChurnGuard AI - Early Warning System</h1>', unsafe_allow_html=True)
st.markdown("**Powered by Multi-Agent AI** | Detect churn risks before they happen!")

with st.sidebar:
    st.header("📤 Upload Data")
    uploaded_file = st.file_uploader("Upload customer CSV", type="csv", help="Required columns: customer_id, tenure, monthly_charges, total_charges, churn. Optional: complaints, usage_hours.")
    st.info("💡 Supports standard Telco datasets with automatic column mapping.")

    st.header("📧 Email Configuration (Optional)")
    smtp_server = st.text_input("SMTP Server (e.g., smtp.gmail.com)", placeholder="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=587, min_value=1, max_value=65535)
    smtp_username = st.text_input("Email Username", value="sahithisuresh14@gmail.com", placeholder="your-email@gmail.com")
    smtp_password = st.text_input("Email Password/App Password", type="password", placeholder="your-app-password")
    recipient_email = st.text_input("Recipient Email", value="sahithisuresh14@gmail.com", placeholder="account-manager@company.com")

    if st.button("🚀 Process Data & Send Alerts"):
        if uploaded_file:
            st.session_state.process = True
            st.session_state.email_config = {
                'smtp_server': smtp_server,
                'smtp_port': smtp_port,
                'smtp_username': smtp_username,
                'smtp_password': smtp_password,
                'recipient_email': recipient_email
            }
        else:
            st.error("Please upload a CSV file.")

if 'process' in st.session_state and st.session_state.process:
    # Save uploaded file temporarily
    with open("temp_upload.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        # Initialize agents
        data_agent = DataAgent("temp_upload.csv")
        model_agent = ModelAgent()
        email_config = st.session_state.get('email_config', {})
        alert_agent = AlertAgent(
            smtp_server=email_config.get('smtp_server'),
            smtp_port=email_config.get('smtp_port'),
            smtp_username=email_config.get('smtp_username'),
            smtp_password=email_config.get('smtp_password'),
            recipient_email=email_config.get('recipient_email')
        )

        # Data Agent: Load and preprocess
        data_agent.load_data()
        data_agent.preprocess()

        # Model Agent: Train and predict
        X_train, y_train = data_agent.get_train_data()
        X_test, y_test = data_agent.get_test_data()
        model_agent.train(X_train, y_train)
        accuracy = model_agent.evaluate(X_test, y_test)

        # Predict on full data
        full_df = data_agent.get_full_data()
        X_full = full_df.drop(['customer_id', 'churn'], axis=1)
        X_full_scaled = data_agent.scaler.transform(X_full)
        churn_probs = model_agent.predict_proba(X_full_scaled)

        # Alert Agent: Identify at-risk and send emails
        at_risk = alert_agent.identify_at_risk(full_df, churn_probs, top_n=5)
        alerts = alert_agent.simulate_alert_emails(at_risk)

        # Send real emails if configured
        if smtp_username and smtp_password and recipient_email:
            alert_agent_instance = AlertAgent(
                smtp_server=smtp_server,
                smtp_port=int(smtp_port),
                smtp_username=smtp_username,
                smtp_password=smtp_password,
                recipient_email=recipient_email
            )
            alert_agent_instance.send_alert_emails(at_risk)

        # Layout
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("📊 Model Insights")
            st.metric("Model Accuracy", f"{accuracy:.2%}")
            churn_dist = full_df['churn'].value_counts()
            fig, ax = plt.subplots()
            ax.pie(churn_dist, labels=['No Churn', 'Churn'], autopct='%1.1f%%', colors=['#4CAF50', '#f44336'])
            ax.set_title("Churn Distribution")
            st.pyplot(fig)

        with col2:
            st.subheader("⚠️ Top 5 At-Risk Customers")
            st.dataframe(at_risk.style.highlight_max(axis=0, color='red'))

            # Bar chart for top risks
            fig, ax = plt.subplots()
            ax.bar(at_risk['customer_id'].astype(str), at_risk['churn_probability'], color='#f44336')
            ax.set_title("Churn Probabilities for Top Risks")
            ax.set_ylabel("Probability")
            st.pyplot(fig)

        st.subheader("📧 Simulated Alert Emails")
        tabs = st.tabs([f"Alert {i+1}" for i in range(len(alerts))])
        for i, (tab, alert) in enumerate(zip(tabs, alerts)):
            with tab:
                st.markdown(f'<div class="alert-card">{alert.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}. Please ensure your CSV has the required columns: customer_id, tenure, monthly_charges, total_charges, churn. Optional: complaints, usage_hours. The system can handle standard Telco Churn datasets by mapping columns automatically.")
