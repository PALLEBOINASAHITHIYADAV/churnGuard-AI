from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

class ModelAgent:
    def __init__(self):
        self.model = LogisticRegression(random_state=42)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        print("Model trained.")

    def predict_proba(self, X):
        return self.model.predict_proba(X)[:, 1]  # probability of churn (class 1)

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.2f}")
        return accuracy
