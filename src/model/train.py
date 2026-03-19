import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def train_win_predictor():
    print("Loading processed data...")
    try:
        df = pd.read_csv('data/processed/model_data.csv')
    except Exception as e:
        print("Data not found. Please run the data pipeline first.")
        return

    # Use comprehensive new features
    X = df.drop(['target', 'team1', 'team2', 'venue'], axis=1)
    y = df['target']
    
    feature_names = X.columns.tolist()
    
    if len(df) < 10:
        print("Not enough data to train. Generating mock model instead.")
        X_train, X_test, y_train, y_test = X, X, y, y
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    from sklearn.model_selection import GridSearchCV
    
    # We will use Logistic Regression to get well-calibrated probabilities
    # and GridSearchCV to identify the optimal regularization to maximize accuracy
    base_model = LogisticRegression(max_iter=2000, random_state=42)
    
    param_grid = {
        'C': [0.01, 0.1, 1.0, 10.0],
        'solver': ['lbfgs', 'liblinear']
    }
    
    print("Running Hyperparameter Grid Search for max accuracy...")
    grid_search = GridSearchCV(base_model, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    
    model = grid_search.best_estimator_
    print(f"Best Hyperparameters: {grid_search.best_params_}")
    
    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Win Probability Model Accuracy: {acc * 100:.2f}%")
    
    # Save the model and feature names
    os.makedirs('models/saved_models', exist_ok=True)
    joblib.dump({'model': model, 'features': feature_names}, 'models/saved_models/win_model.pkl')
    print("Model saved to models/saved_models/win_model.pkl")

if __name__ == '__main__':
    print("Training ML Models...")
    train_win_predictor()
