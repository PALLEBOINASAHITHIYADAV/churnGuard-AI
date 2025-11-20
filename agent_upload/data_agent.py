import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

class DataAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()

    def load_data(self):
        self.df = pd.read_csv(self.data_path)
        print("Data loaded successfully.")

    def preprocess(self):
        # Column mapping for common datasets (e.g., Telco Customer Churn)
        column_mapping = {
            'customerID': 'customer_id',
            'CustomerID': 'customer_id',
            'MonthlyCharges': 'monthly_charges',
            'TotalCharges': 'total_charges',
            'SeniorCitizen': 'senior_citizen',  # optional
            'Partner': 'partner',  # optional
            'Dependents': 'dependents',  # optional
            'PhoneService': 'phone_service',  # optional
            'MultipleLines': 'multiple_lines',  # optional
            'InternetService': 'internet_service',  # optional
            'OnlineSecurity': 'online_security',  # optional
            'OnlineBackup': 'online_backup',  # optional
            'DeviceProtection': 'device_protection',  # optional
            'TechSupport': 'tech_support',  # optional
            'StreamingTV': 'streaming_tv',  # optional
            'StreamingMovies': 'streaming_movies',  # optional
            'Contract': 'contract',  # optional
            'PaperlessBilling': 'paperless_billing',  # optional
            'PaymentMethod': 'payment_method',  # optional
            'Churn': 'churn',
            'Churn?': 'churn'
        }

        # Rename columns if they match
        self.df.rename(columns=column_mapping, inplace=True)

        # Check for required columns
        required_cols = ['customer_id', 'tenure', 'monthly_charges', 'total_charges', 'churn']
        optional_cols = ['complaints', 'usage_hours']
        missing_required = [col for col in required_cols if col not in self.df.columns]
        if missing_required:
            raise ValueError(f"Missing required columns: {missing_required}. Please ensure your CSV has columns: {required_cols}. Optional: {optional_cols}")

        # Add missing optional columns with defaults if not present
        if 'complaints' not in self.df.columns:
            self.df['complaints'] = 0  # default no complaints
        if 'usage_hours' not in self.df.columns:
            self.df['usage_hours'] = self.df['tenure'] * 10  # dummy usage based on tenure

        # Handle missing values (simple fill with mean for numerical)
        numerical_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        self.df[numerical_cols] = self.df[numerical_cols].fillna(self.df[numerical_cols].mean())

        # Convert TotalCharges to numeric if it's string (common in Telco dataset)
        if 'total_charges' in self.df.columns and self.df['total_charges'].dtype == 'object':
            self.df['total_charges'] = pd.to_numeric(self.df['total_charges'], errors='coerce').fillna(0)

        # Encode categorical columns to numerical
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col == 'churn':
                self.df[col] = self.df[col].map({'Yes': 1, 'No': 0})
            elif col == 'customer_id':
                continue  # keep as is for identification
            else:
                # Label encode other categoricals
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col].astype(str))

        # Feature engineering: add derived features if needed
        self.df['charges_per_tenure'] = self.df['total_charges'] / (self.df['tenure'] + 1)  # avoid div by zero

        # Split features and target
        X = self.df.drop(['customer_id', 'churn'], axis=1)
        y = self.df['churn']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

        print("Data preprocessed and split.")

    def get_train_data(self):
        return self.X_train, self.y_train

    def get_test_data(self):
        return self.X_test, self.y_test

    def get_full_data(self):
        return self.df
