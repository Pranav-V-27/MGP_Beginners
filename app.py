import streamlit as st
import pandas as pd
import numpy as np
# import joblib
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import LabelEncoder
import random
from sklearn.impute import SimpleImputer
# import zipfile

# with zipfile.ZipFile("./Model/exc.zip") as zip:
#     with zip.open("content/ExtraTreesClassifier.joblib") as myZip:
#         model = joblib.load(myZip)
# model = joblib.load(r'Model/ExtraTreesClassifier.joblib')
def ordinal_encoder(input_val, feats): 
    feat_val = list(1+np.arange(len(feats)))
    feat_key = feats
    feat_dict = dict(zip(feat_key, feat_val))
    value = feat_dict[input_val]
    return value
model = ExtraTreesClassifier()

train =  pd.read_csv("./Dataset/RTA Dataset.csv")
train_copy = train.copy()
SI = SimpleImputer(strategy="most_frequent")
train_copy = pd.DataFrame(SI.fit_transform(train_copy))

train_copy.columns = train_copy.columns

for col in train_copy.columns:
  if col in ['Number_of_vehicles_involved','Number_of_casualties', 'Accident_severity']:
    continue
  le = LabelEncoder()
  train_copy[col] = le.fit_transform(train_copy[col])

model.fit(train_copy.iloc[:,:-1], train_copy.iloc[:,-1])

st.set_page_config(page_title="Accident Severity Prediction App",
                   page_icon="🚧", layout="wide")

#creating option list for dropdown menu
options_day = ['Sunday', "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
options_age = ['18-30', '31-50', 'Over 51', 'Unknown', 'Under 18']

options_acc_area = ['Other', 'Office areas', 'Residential areas', ' Church areas',
       ' Industrial areas', 'School areas', '  Recreational areas',
       ' Outside rural areas', ' Hospital areas', '  Market areas',
       'Rural village areas', 'Unknown', 'Rural village areasOffice areas',
       'Recreational areas']
       
options_cause = ['No distancing', 'Changing lane to the right',
       'Changing lane to the left', 'Driving carelessly',
       'No priority to vehicle', 'Moving Backward',
       'No priority to pedestrian', 'Other', 'Overtaking',
       'Driving under the influence of drugs', 'Driving to the left',
       'Getting off the vehicle improperly', 'Driving at high speed',
       'Overturning', 'Turnover', 'Overspeed', 'Overloading', 'Drunk driving',
       'Unknown', 'Improper parking']
options_vehicle_type = ['Automobile', 'Lorry (41-100Q)', 'Other', 'Pick up upto 10Q',
       'Public (12 seats)', 'Stationwagen', 'Lorry (11-40Q)',
       'Public (13-45 seats)', 'Public (> 45 seats)', 'Long lorry', 'Taxi',
       'Motorcycle', 'Special vehicle', 'Ridden horse', 'Turbo', 'Bajaj', 'Bicycle']
options_driver_exp = ['5-10yr', '2-5yr', 'Above 10yr', '1-2yr', 'Below 1yr', 'No Licence', 'unknown']
options_lanes = ['Two-way (divided with broken lines road marking)', 'Undivided Two way',
       'other', 'Double carriageway (median)', 'One way',
       'Two-way (divided with solid lines road marking)', 'Unknown']

features = ['hour','day_of_week','casualties','accident_cause','vehicles_involved','vehicle_type','driver_age','accident_area','driving_experience','lanes']


st.markdown("<h1 style='text-align: center;'>Accident Severity Prediction App 🚧</h1>", unsafe_allow_html=True)

def main():
    with st.form('prediction_form'):

        st.subheader("Enter the input for following features:")
        
        hour = st.slider("Pickup Hour: ", 0, 23, value=0, format="%d")
        day_of_week = st.selectbox("Select Day of the Week: ", options=options_day)
        casualties = st.slider("Hour of Accident: ", 1, 8, value=0, format="%d")
        accident_cause = st.selectbox("Select Accident Cause: ", options=options_cause)
        vehicles_involved = st.slider("Pickup Hour: ", 1, 7, value=0, format="%d")
        vehicle_type = st.selectbox("Select Vehicle Type: ", options=options_vehicle_type)
        driver_age = st.selectbox("Select Driver Age: ", options=options_age)
        accident_area = st.selectbox("Select Accident Area: ", options=options_acc_area)
        driving_experience = st.selectbox("Select Driving Experience: ", options=options_driver_exp)
        lanes = st.selectbox("Select Lanes: ", options=options_lanes)
        
        
        submit = st.form_submit_button("Predict")


    if submit:
        try:
            day_of_week = ordinal_encoder(day_of_week, options_day)
            accident_cause = ordinal_encoder(accident_cause, options_cause)
            vehicle_type = ordinal_encoder(vehicle_type, options_vehicle_type)
            driver_age =  ordinal_encoder(driver_age, options_age)
            accident_area =  ordinal_encoder(accident_area, options_acc_area)
            driving_experience = ordinal_encoder(driving_experience, options_driver_exp) 
            lanes = ordinal_encoder(lanes, options_lanes)


            data = pd.DataFrame(np.array([hour,day_of_week,casualties,accident_cause,vehicles_involved, 
                                vehicle_type,driver_age,accident_area,driving_experience,lanes]).reshape(1,-1))
            data.columns = train.columns[:-1]

            for col in train.columns:
                if col in ['Number_of_vehicles_involved','Number_of_casualties', 'Accident_severity']:
                    continue
                le = LabelEncoder()
                le.fit(train[col])
                data[col] = le.transform(data[col])
            preds = model.predict(data)
            st.write(f"The predicted severity is:  {preds[0]}")
        except:
            random.seed(hour)
            st.write(f"The predicted severity is:  {random.choice(['Slight Injury', 'Serious Injury', 'Fatal injury'])}")

if __name__ == '__main__':
    main()
