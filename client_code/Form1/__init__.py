from ._anvil_designer import Form1Template
from anvil import *
import anvil.http

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Bind the button click event to the submit method
        self.submit_button.set_event_handler('click', self.submit_form)

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

        # Call the function to fetch crop predictions
        self.get_predictions(user_pincode, land_size)

    def get_predictions(self, user_pincode, land_size):
        # Prepare the request payload
        payload = {
            "pincode": user_pincode,
            "land_size": land_size
        }

        try:
            # Make a POST request to your Flask API
            response = anvil.http.request(
                "https://your-service-name.onrender.com/predict",  # Replace with your actual API URL
                method="POST",
                json=payload
            )

            # Handle the response
            if 'predicted_crop' in response:
                self.output_section.clear()  # Clear previous output
                self.output_section.add_component(Label(text=f"Predicted Crop: {response['predicted_crop']}"))
                self.output_section.add_component(Label(text=f"Estimated Production: {response['estimated_production']} kgs"))
            else:
                self.output_section.clear()
                self.output_section.add_component(Label(text=f"Error: {response['error']}"))

        except Exception as e:
            alert(f"An error occurred: {str(e)}")