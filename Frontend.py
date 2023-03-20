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
    df = pd.DataFrame(data, ["age", "sex", "bmi", "children", "smoker"]).T
    # returning the processed data
    return df


# check the formats of the input data
def check_data(data):
    # checking age, bmi, children
    check_1 = 0.0
    for i in data:
        if type(i) != type(check_1):
            # invalid data format
            return False

    if data[2] < 0 or data[1] < 0 or data[0] < 0:
        return False
    elif data[1] > 200 or data[1] < 13:
        return False
    elif data[0] < 18:
        return False

    # all data are in valid format
    return True


# entry point for our webpage
def main():
    # sidebar
    with st.sidebar:
        st.title("About:")
        st.markdown(
        "- Predicting the cost of the Health Insurance Policy that should be applied by a Person, based on their Characteristics.\n"
        "- Early Health Insurance Amount Prediction can help in better contemplation of the amount needed, where a person can ensure that the amount, he/she is going to opt is justified.\n"
        "- Also, it can provide an idea about gaining extra benefits from the Health Insurance."
        )
        st.title("Other Projects:")
        st.markdown("📰 [Fake News Detector](https://fake-news-detector-k19.streamlit.app/)")

        
    # setting the title
    st.title('US Health Insurance Cost Predictor')

    try:
        # getting age from the user
        age = st.text_input('Age')
        st.info("Acceptable Age: 18 - 64",icon="ℹ️")
        temp_age = float(age) 
        age = temp_age
        if temp_age < 18 or temp_age > 64:
            raise Exception
        
    except:
        if age != "":
            st.warning("Enter a Valid Age",icon="❌")

    # getting gender from the user
    inp_gender = st.radio("Gender", ('Male', 'Female'))
    if inp_gender == 'Male':
        gender = 1.0
    else:
        gender = 0.0

    # calculating the BMI with height and weight
    bmi = None
    bool_height_weight = True
    try:
        verify = True
        height = st.text_input('Height (in Cm) ')
        weight = st.text_input('Weight (in Kg) ')
        st.info("Acceptable BMI: 13.0 - 200.0",icon="ℹ️")
        temp_h = float(height)
        temp_w = float(weight)
        if temp_h < 50 or temp_h > 250:
            bool_height_weight = False
            st.warning("Enter a Valid height",icon="❌")
       
        
        if temp_w < 15 or temp_w > 600:
            bool_height_weight = False
            verify = False
            st.warning("Enter a Valid weight",icon="❌")

        elif bool_height_weight:
            bmi = float(float(float(weight) / (float(height) * float(height)))*10000)
            st.info(f"Your BMI: {bmi:.2f}",icon="ℹ️")
            temp_b = bmi
            if bmi < 14 and verify:
                st.warning(f"BMI is too Low.",icon="❌")
            elif bmi > 54 and verify:
                st.warning(f"BMI is too High.",icon="❌")
        
    except:
        if height != "" and weight != "":
            st.warning("Enter a Valid Height and Weight",icon="❌")

    # getting number of children that the person have
    children = None
    try:
        children = float(st.text_input('Number Of Children')+".0")
        if children < 0 or children > 15:
            raise Exception
    except:
        st.warning("Enter a Valid Number of Children",icon="❌")

    # getting input whether the person is a smoker or not
    inp_smoker = st.radio('Are you a Smoker ? ', ('Yes', 'No'))
    if inp_smoker == 'Yes':
        smoker = 1.0
    else:
        smoker = 0.0

    # getting input for region where the person lives
    inp_region = st.radio('Region (In US)', ('Southeast', 'Southwest', 'Northwest', 'Northeast'))

    # showing the results
    try:
        result = ""
        
        if st.button('submit'):   
            if children < 0 or children > 15:
                raise Exception       
            validated = check_data([age, bmi, children])
            if validated and bool_height_weight:
                # small animation until the webpage is loaded
                st.balloons()
                
                processed_data = convert_into_dataframe([age, gender, bmi, children, smoker])
                result = make_prediction(processed_data)
                min_res = round((result - 2500), -3) if result > 3000 else round(result, -3)
                max_res = round((result + 2500), -3) 
                st.success(f"Predicted Range: \${min_res:.0f} to \${max_res:.0f}")

            else:
                raise Exception

        st.info(
                "Premiums are determined by Health Insurance Companies "
                "private statistical procedures and complicated models, "
                "which are kept concealed from the public. "
                "The goal of this predictor is to see if machine learning algorithms "
                "can be used to anticipate the pricing "
                "of yearly health insurance premiums on the basis of person's "
                "characteristics.", icon="ℹ️")
    except:
        st.error('Invalid Input. Try again!!!', icon="⚠️")
        


if __name__ == '__main__':
    # calling main function
    main()

