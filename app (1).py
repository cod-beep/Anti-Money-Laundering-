import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("aml_model.pkl")

st.title("Anti-Money Laundering (AML) Detection System")

st.write("Enter transaction details to predict whether it is laundering or not.")

# User Inputs
amount = st.number_input("Transaction Amount", min_value=0.0, value=1000.0)

payment_type = st.selectbox(
    "Payment Type",
    ["cash", "cheque", "card", "online", "transfer"]
)

payment_currency = st.selectbox(
    "Payment Currency",
    ["USD", "EUR", "INR", "GBP", "Other"]
)

received_currency = st.selectbox(
    "Received Currency",
    ["USD", "EUR", "INR", "GBP", "Other"]
)

sender_location = st.selectbox(
    "Sender Bank Location",
    ["Local", "Foreign"]
)

receiver_location = st.selectbox(
    "Receiver Bank Location",
    ["Local", "Foreign"]
)

laundering_type = st.selectbox(
    "Laundering Type",
    ["Unknown", "Structuring", "Smurfing", "Shell_Company"]
)

# Feature Engineering (same logic as training)
if amount <= 1000:
    amount_risk = 0
elif amount <= 10000:
    amount_risk = 1
elif amount <= 50000:
    amount_risk = 2
else:
    amount_risk = 3

if payment_type.lower() in ["cash", "cheque"]:
    payment_risk = 1
else:
    payment_risk = 0

# Encode remaining categorical features manually
encoding_map = {
    "USD": 0, "EUR": 1, "INR": 2, "GBP": 3, "Other": 4,
    "Local": 0, "Foreign": 1,
    "Unknown": 0, "Structuring": 1, "Smurfing": 2, "Shell_Company": 3
}

input_data = pd.DataFrame([[
    encoding_map[payment_currency],
    encoding_map[received_currency],
    encoding_map[sender_location],
    encoding_map[receiver_location],
    encoding_map[laundering_type],
    amount_risk,
    payment_risk
]], columns=[
    "Payment_currency",
    "Received_currency",
    "Sender_bank_location",
    "Receiver_bank_location",
    "Laundering_type",
    "Amount_Risk",
    "Payment_Risk"
])

# Prediction
if st.button("Predict"):
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("⚠️ Suspicious Transaction: Possible Money Laundering")
    else:
        st.success("✅ Normal Transaction: No Money Laundering Detected")
