# importing the required libraries
import numpy as np
import pandas as pd
import streamlit as st
import xgboost as xgb

# loading the saved model
model = xgb.XGBRFRegressor()
model.load_model("predictor.json")

# function to make prediction with our model
def make_prediction(feature):
    prediction = model.predict(feature)
    # convert and return the result
    return np.asarray(prediction)[0]


# function to preprocess data
def convert_into_dataframe(data):
    # turning into a dataframe
    df = pd.DataFrame(data, ["age", "gender", "bmi", "children", "smoker", "region"]).T
    # returning the processed data
    return df


# check the formats of the input data
def check_data(data):
    # checking age, bmi, children
    for i in data:
        check_1 = 0.0
        if type(i) != type(check_1):
            # invalid data format
            return False
    # all data are in valid format
    return True


# entry point for our webpage
def main():
    # setting the title
    st.title('US Health Insurance Predictor')

    age = None
    try:
        # getting age from the user
        age = float(st.text_input('Age')+".0")
        if age < 18 or age > 150:
            st.warning("Enter a Valid Age",icon="❌")
    except:
        pass

    # getting gender from the user
    inp_gender = st.radio("Gender", ('Male', 'Female'))
    # converting the gender input into 0 or 1
    if inp_gender == 'Female':
        gender = 0.0
    else:
        gender = 1.0

    # calculating the BMI with height and weight
    bmi = None
    try:
        verify = True
        height = st.text_input('Height (in CM) ')
        temp_h = float(height)
        if temp_h < 50 or temp_h > 250:
            st.warning("Enter a Valid height",icon="❌")
       
        weight = st.text_input('Weight (in Kg) ')
        temp_w = float(weight)
        if temp_w < 15 or temp_w > 600:
            verify = False
            st.warning("Enter a Valid weight",icon="❌")
      
        bmi = float(float(float(weight) / (float(height) * float(height)))*10000)
        temp_b = bmi
        if bmi < 13 and verify:
            st.warning(f"BMI is too Low.   BMI: {round(temp_b, 0)}",icon="❌")
        elif bmi > 200 and verify:
            st.warning(f"BMI is too High.   BMI: {round(temp_b, 0)}",icon="❌")
        
    except:
        pass

    # getting number of children that the person have
    children = None
    try:
        children = float(st.text_input('Number Of Children'))
        if children < 0 or children > 15:
            st.warning("Enter a Valid Number of Children",icon="❌")
    except:
        pass

    # getting input whether the person is a smoker or not
    inp_smoker = st.radio('Are you a Smoker ? ', ('Yes', 'No'))
    if inp_smoker == 'Yes':
        smoker = 1.0
    else:
        smoker = 0.0

    # getting input for region where the person lives
    inp_region = st.radio('Region (In US)', ('Southeast', 'Southwest', 'Northwest', 'Northeast'))
    if inp_region == 'Southeast':
        region = 3.0
    elif inp_region == 'Southwest':
        region = 4.0
    elif inp_region == 'Northwest':
        region = 2.0
    else:
        region = 1.0

    # showing the results
    try:
        result = ""
        if st.button('submit'):
            # small animation until the webpage is loaded
            st.balloons()
            validated = check_data([age, bmi, children])
            if validated:
                processed_data = convert_into_dataframe([age, gender, bmi, children, smoker, region])
                result = make_prediction(processed_data)
                st.success(f"Predicted Cost: ${result:.0f}")

            else:
                st.error('Invalid Input. Kindly Reload the Webpage and try again!!!', icon="⚠️")

        st.info(
                "Premiums are determined by Health Insurance Companies "
                "private statistical procedures and complicated models, "
                "which are kept concealed from the public. "
                "The goal of this predictor is to see if machine learning algorithms "
                "can be used to anticipate the pricing "
                "of yearly health insurance premiums on the basis of person's "
                "characteristics.", icon="ℹ️")
    except:
        pass


if __name__ == '__main__':
    # calling main function
    main()

