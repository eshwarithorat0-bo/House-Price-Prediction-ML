import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load the housing dataset
data = pd.read_csv("house_data.csv")

# 2. Display dataset information
print("Dataset loaded successfully!")
print("Columns:", data.columns.tolist())
print(data.head())

# 3. Select numeric columns
numeric_data = data.select_dtypes(include="number").dropna()

# 4. Check whether the dataset has enough columns
if numeric_data.shape[1] < 2:
    raise ValueError(
        "Dataset needs at least one numeric feature "
        "and one numeric house-price column."
    )

# 5. Use the last numeric column as the target price
X = numeric_data.iloc[:, :-1]
y = numeric_data.iloc[:, -1]

# 6. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# 8. Evaluate the model
predictions = model.predict(X_test)

print("\nModel training completed!")
print("Mean Absolute Error:", mean_absolute_error(y_test, predictions))
print("R2 Score:", r2_score(y_test, predictions))

# 9. Save the trained model and feature names
with open("house_price_model.pkl", "wb") as file:
    pickle.dump(
        {"model": model, "features": X.columns.tolist()},
        file
    )

print("\nModel saved as house_price_model.pkl")