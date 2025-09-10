# app.py
import streamlit as st
import joblib
import numpy as np

# Load the trained model with absolute path
try:
    model = joblib.load(r'C:\Users\Kshitij Gaikwad\OneDrive\Documents\Green Skill Internship\energy_consumption_model.pkl')
    st.write("Model loaded successfully!")
    print("Model loaded, type:", type(model))  # Debug
except Exception as e:
    st.error(f"Error loading model: {e}")
    print(f"Model load error: {e}")  # Debug
    st.stop()

# Set page title and layout
st.title("Energy Consumption Predictor")
st.write("Enter the details below to predict daily energy consumption (kWh).")

# Input fields with validation
day_of_week = st.number_input("Day of Week (0-6, where 0 is Monday, 6 is Sunday)", min_value=0, max_value=6, value=0, help="Enter a number between 0 and 6")
month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=1, help="Enter a number between 1 and 12")
voltage = st.number_input("Voltage (e.g., 230)", min_value=0.0, value=230.0, step=0.1, help="Typical voltage value")
sub_metering_1 = st.number_input("Sub-metering 1 (kWh)", min_value=0.0, value=100.0, step=0.1, help="Kitchen appliance energy")
global_intensity = st.number_input("Global Intensity", min_value=0.0, value=20.0, step=0.1, help="Average current intensity")
sub_metering_2 = st.number_input("Sub-metering 2 (kWh)", min_value=0.0, value=50.0, step=0.1, help="Laundry appliance energy")

if st.button("Predict"):
    # Enhanced validation
    if any(x < 0 for x in [day_of_week, month, voltage, sub_metering_1, global_intensity, sub_metering_2]):
        st.error("Please enter non-negative values.")
    elif month > 12 or day_of_week > 6:
        st.error("Invalid month or day of week value.")
    else:
        try:
            # Scale sub-meter inputs to approximate daily totals (e.g., multiply by 10-20)
            scaled_sub_metering_1 = sub_metering_1 * 10  # Adjust based on training data range
            scaled_sub_metering_2 = sub_metering_2 * 10  # Adjust based on training data range
            input_data = np.array([[day_of_week, month, voltage, scaled_sub_metering_1, global_intensity, scaled_sub_metering_2]])
            print("Input data shape:", input_data.shape)  # Debug
            print("Input data:", input_data)  # Debug
            prediction = model.predict(input_data)[0]
            st.success(f"Predicted Daily Energy Consumption: {max(0, prediction):.2f} kWh")  # Clamp to non-negative
        except Exception as e:
            st.error(f"Prediction error: {e}")
            print(f"Debug: Error details = {e}")  # Debug

# Optional: Add info and styling
st.write("Note: Values should reflect typical household data for accurate predictions.")
st.markdown("<style>body {background-color: #f0f0f0;}</style>", unsafe_allow_html=True)