import streamlit as st
import requests
import pandas as pd

# Title of the app
st.title("Taxi Fare Prediction")

# Create the form to collect input parameters
with st.form("my_form"):
    st.write("Enter the details for the ride:")

    # Input for Pickup Date and Time (separate date and time inputs)
    pickup_date = st.date_input("Pickup Date", value=pd.to_datetime("2014-07-06"))
    pickup_time = st.time_input("Pickup Time", value=pd.to_datetime("2014-07-06 19:18:00").time())

    # Combine the date and time into a single string for the API
    pickup_datetime = f"{pickup_date} {pickup_time}"

    # Input for Pickup Longitude and Latitude (ensure it's a float in a valid range)
    pickup_longitude = st.number_input("Pickup Longitude", min_value=-180.0, max_value=180.0, value=-73.950655, step=0.000001)
    pickup_latitude = st.number_input("Pickup Latitude", min_value=-90.0, max_value=90.0, value=40.783282, step=0.000001)

    # Input for Dropoff Longitude and Latitude (ensure it's a float in a valid range)
    dropoff_longitude = st.number_input("Dropoff Longitude", min_value=-180.0, max_value=180.0, value=-73.984365, step=0.000001)
    dropoff_latitude = st.number_input("Dropoff Latitude", min_value=-90.0, max_value=90.0, value=40.769802, step=0.000001)

    # Input for Passenger Count (using slider or selectbox for predefined values)
    passenger_count = st.slider("Passenger Count", min_value=1, max_value=6, value=2)

    # Submit button inside the form
    submitted = st.form_submit_button("Submit")

# Define the API URL (updated to the live API)
api_url = 'https://taxifare.lewagon.ai/predict'

# When the form is submitted, make the API call
if submitted:
    # Build the query parameters for the GET request
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    # Display the parameters being sent
    st.write(f"Sending the following parameters to the API: {params}")

    try:
        # Send a GET request to the API with the parameters
        response = requests.get(api_url, params=params)

        # If the request was successful, display the response
        if response.status_code == 200:
            prediction = response.json().get("prediction", None)
            if prediction:
                st.write(f"The predicted taxi fare is: ${prediction:.2f}")
            else:
                st.write("Error: No prediction returned.")
        else:
            st.write(f"Error: Unable to retrieve prediction. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.write(f"An error occurred: {e}")
