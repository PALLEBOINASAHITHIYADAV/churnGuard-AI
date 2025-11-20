# ChurnGuard AI - Early Warning System

## Overview
ChurnGuard AI is a multi-agent AI system designed to predict customer churn and send automated email alerts to prevent customer loss. This system helps B2B SaaS companies retain customers by identifying at-risk clients before they churn.

## Features
- **Multi-Agent Architecture**: Data preprocessing, ML prediction, and alert notification agents
- **Machine Learning**: Logistic Regression model for churn prediction with ~81% accuracy
- **Email Alerts**: Automated SMTP email notifications for account managers
- **Web Interface**: Streamlit-based dashboard with data visualizations
- **Data Processing**: Handles standard Telco/SaaS customer datasets with automatic column mapping

## Architecture
- **DataAgent**: Loads, preprocesses, and prepares customer data
- **ModelAgent**: Trains ML model and predicts churn probabilities
- **AlertAgent**: Identifies at-risk customers and sends email alerts

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
streamlit run app.py
```

## Input Schema
- Customer data CSV with columns: customer_id, tenure, monthly_charges, total_charges, churn
- Optional: complaints, usage_hours
- Email configuration for SMTP alerts

## Output Schema
- Model accuracy score
- List of top at-risk customers with churn probabilities
- Email alert status
- Churn distribution statistics
- Simulated alert previews

## API Endpoints
- POST /predict: Predict churn for customer data
- GET /customers/{id}: Get customer information
- POST /alerts/send: Send churn alert emails
- PUT /customers/{id}/status: Update customer status
- DELETE /customers/{id}: Remove customer record

## Environment Variables
- SMTP_SERVER: Email server configuration
- SMTP_PORT: Email port (default: 587)
- DEFAULT_RECIPIENT: Default alert recipient
- MODEL_ACCURACY_THRESHOLD: Minimum acceptable model accuracy
- TOP_RISK_COUNT: Number of top-risk customers to alert

## License
MIT License

## Author
BLACKBOXAI
