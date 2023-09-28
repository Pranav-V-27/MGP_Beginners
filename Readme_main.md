# Road Traffic Accidents Severity Prediction app

This is an app that predicts the severity of an accident based on various input features.

## Input Features

The app takes in the following input features:
- Pickup Hour
- Day of the Week
- Hour of Accident
- Accident Cause
- Number of Vehicles Involved
- Vehicle Type
- Driver Age
- Accident Area
- Driving Experience
- Lanes

## How It Works

The user inputs the values for the various features, and the app uses an ExtraTreesClassifier model to predict the severity of the accident. The predicted severity is then displayed to the user.

## Dependencies

The app requires the following dependencies:
- streamlit
- pandas
- numpy
- joblib
- scikit-learn

## How to Run

To run the app, execute the `app.py` file in a Python environment that has the required dependencies installed.

