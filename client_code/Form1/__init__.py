from ._anvil_designer import Form1Template
from anvil import *
from datetime import datetime
import pandas as pd

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Set greeting message based on the current time
        self.set_greeting()

        # Bind the button click event to the submit method
        self.submit_button.set_event_handler('click', self.submit_form)

    def set_greeting(self):
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Good morning"
        elif 12 <= current_hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        self.greeting_label.text = f"Hello, {greeting}!"

    def submit_form(self, **event_args):
        # Get the user inputs
        user_name = self.name_input.text
        user_pincode = self.pincode_input.text.strip()
        land_size = self.land_size_input.text.strip()

        # Validate inputs
        if not user_name or not user_pincode or not land_size:
            alert("Please fill in all fields.")
            return

        try:
            land_size = float(land_size)
        except ValueError:
            alert("Please enter a valid number for land size.")
            return

        # Call the function to fetch weather and crop predictions
        self.get_predictions(user_pincode, land_size)

    def get_predictions(self, user_pincode, land_size):
        # Fetch location details based on pincode (replace with your actual data fetching logic)
        if user_pincode in pin_data['Pincode'].astype(str).values:
            row = pin_data[pin_data['Pincode'] == int(user_pincode)].iloc[0]
            place_name = row['Placename']
            district = row['District']
            state_name = row['StateName']

            # Display the formatted output
            self.output_label.text = f"Weather for the pincode {user_pincode}:\nPlace Name: {place_name}\nDistrict: {district}\nState Name: {state_name}"

            # Fetch weather data (this should be replaced with your actual API call)
            weather_data = fetch_weather_data(row['Latitude'], row['Longitude'], datetime.today().strftime('%Y-%m-%d'), 'YOUR_API_KEY')

            if weather_data is None:
                alert("Error fetching weather data.")
                return

            # Analyze and display weather data in a table
            analyzed_weather = analyze_weather(weather_data)
            weather_df = pd.DataFrame({
                'Parameter': ['Temperature