# -*- coding: utf-8 -*-
"""water.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qfOiVqEvkCdzfSz-lVmQZtArpJ8WW6-Y
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict
import joblib

df = pd.read_csv("https://raw.githubusercontent.com/PonakalaNeelima/Project/refs/heads/master/output.csv")

df.head()

df.info()

target_counts = df['is_safe'].value_counts()

print("Number of 0s:", target_counts[0])
print("Number of 1s:", target_counts[1])

# Number of samples to add
n_samples = 6000

# Generate synthetic data for the specified features
synthetic_data = {
    'ph': np.random.uniform(6.5, 8.5, n_samples),  # Safe pH range
    'hardness': np.random.uniform(0, 300, n_samples),  # Adjust as needed
    'turbidity': np.random.uniform(0, 5, n_samples),  # Safe turbidity range
    'arsenic': np.random.uniform(0, 0.01, n_samples),  # Safe arsenic levels
    'chloramine': np.random.uniform(0, 4, n_samples),  # Safe chloramine levels
    'bacteria': np.random.randint(0, 2, n_samples),  # Binary: presence or absence
    'lead': np.random.uniform(0, 0.015, n_samples),  # Safe lead levels
    'nitrates': np.random.uniform(0, 10, n_samples),  # Safe nitrate levels
    'mercury': np.random.uniform(0, 0.002, n_samples),  # Safe mercury levels
    'is_safe': np.ones(n_samples, dtype=int)  # All marked as safe
}

# Create a DataFrame for the synthetic data
synthetic_df = pd.DataFrame(synthetic_data)

# Append synthetic data directly to the original dataset
df = pd.concat([df, synthetic_df], ignore_index=True)

# Save the updated dataset
df.to_csv("output.csv", index=False)

target_counts = df['is_safe'].value_counts()

print("Number of 0s:", target_counts[0])
print("Number of 1s:", target_counts[1])

corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)

features = ['ph','hardness','turbidity','arsenic','chloramine','bacteria','lead',
            'nitrates','mercury', 'is_safe']
plt.figure(figsize=(20, 15))  # Adjust the figure size as needed
for i, feature in enumerate(features):
    plt.subplot(4, 5, i + 1)  # Create a 4x5 grid for 20 plots
    sns.histplot(df[feature], kde=True, bins=30)
    plt.title(feature)
    plt.xlabel('')
    plt.ylabel('Frequency')

plt.tight_layout()  # Adjust spacing to prevent overlap
plt.show()

# Split into features and target
X = df.drop('is_safe', axis=1)
y = df['is_safe']

# Standard scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Show the shapes of the resulting arrays
print("Training features shape:", X_train.shape)
print("Testing features shape:", X_test.shape)
print("Training target shape:", y_train.shape)
print("Testing target shape:", y_test.shape)
joblib.dump(scaler, 'scaler.joblib')

#checking if splits are correct
print(f"Train size: {round(len(X_train) / len(X) * 100)}% \n\
Test size: {round(len(X_test) / len(X) * 100)}%")

# Instnatiating the models
logistic_regression = LogisticRegression()
svm = SVC(probability=True)
tree = DecisionTreeClassifier()
forest=RandomForestClassifier()

# Training the models
base_models = [logistic_regression, svm, tree, forest]

for model in base_models:
    model.fit(X_train, y_train)

# Making predictions with each model
log_reg_preds = logistic_regression.predict(X_test)
svm_preds = svm.predict(X_test)
tree_preds = tree.predict(X_test)
forest_preds = forest.predict(X_test)

#checking if splits are correct
print(f"Train size: {round(len(X_train) / len(X) * 100)}% \n\
Test size: {round(len(X_test) / len(X) * 100)}%")

# Instnatiating the models
logistic_regression = LogisticRegression()
svm = SVC(probability=True)
tree = DecisionTreeClassifier()
forest=RandomForestClassifier()

# Training the models
base_models = [logistic_regression, svm, tree, forest]

for model in base_models:
    model.fit(X_train, y_train)

# Making predictions with each model
log_reg_preds = logistic_regression.predict(X_test)
svm_preds = svm.predict(X_test)
tree_preds = tree.predict(X_test)
forest_preds = forest.predict(X_test)

model_preds = {
    "Logistic Regression": log_reg_preds,
    "Support Vector Machine": svm_preds,
    "Decision Tree": tree_preds,
    "Random Forest": forest_preds
}

for model, preds in model_preds.items():
    print(f"{model} :\nClassification_report\n{classification_report(y_test, preds)}", sep="\n")
    print(f"The accuracy of the model is {accuracy_score(y_test,preds)*100}% ",sep="\n")

test_sample1 = np.array([8.099124189298397, 224.23625939355776, 3.0559337496641685,
                         0.04, 4.24, 0.05, 0.078, 14.16, 0.006]).reshape(1, -1)
log_reg_preds1 = logistic_regression.predict(test_sample1)
svm_preds1 = svm.predict(test_sample1)
tree_preds1 = tree.predict(test_sample1)
forest_preds1 = forest.predict(test_sample1)

print(log_reg_preds1)
print(svm_preds1)
print(tree_preds1)
print(forest_preds1)

def create_stack_dataset(base_models, X, y, n_splits=5):
    stack_X = []
    kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    for model in base_models:
        # Get out-of-fold predictions for each base model
        oof_predictions = cross_val_predict(model, X, y, cv=kf, method='predict_proba')
        stack_X.append(oof_predictions[:, 1])  # Use the probability of class 1 (safe water)

    # Stack the predictions from all models
    stack_X = np.column_stack(stack_X)
    return stack_X
# Generate new dataset for stacking (using predictions from cross-validation)
X_stack = create_stack_dataset(base_models, X_train, y_train, n_splits=5)

# Train a meta-model on the new stacked dataset
meta_model = LogisticRegression()
meta_model.fit(X_stack, y_train)

# Get the predictions for the test set by using the trained base models
base_model_preds_test = [model.predict_proba(X_test)[:, 1] for model in base_models]

# Create a new dataset for the meta-model's prediction
X_test_stack = np.column_stack(base_model_preds_test)

# Get the final predictions from the meta-model
y_stack_pred = meta_model.predict(X_test_stack)

# Evaluate the meta-model
print(f"Accuracy of Stacked Model: {accuracy_score(y_test, y_stack_pred)*100:.2f}%")
print("\nClassification Report for Stacked Model:")
print(classification_report(y_test, y_stack_pred))

import joblib
joblib.dump(meta_model, 'Stacked_Model.joblib')
joblib.dump(logistic_regression, 'LogisticRegression.joblib')
joblib.dump(svm, 'SVM.joblib')
joblib.dump(tree, 'DecisionTree.joblib')
joblib.dump(forest, 'RandomForest.joblib')

