import streamlit as st
import pandas as pd
import joblib
import math

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


#Loading Our final trained RF model 
model= open("hr_model.sav", "rb")
rf_clf=joblib.load(model)


st.title("HR Analytics App")
## Employee Name
emp_name = st.text_input('Employee Name')
## Employee ID
emp_id = st.text_input('Employee ID')


st.sidebar.title("Features")


#Intializing

satisfaction_level = st.sidebar.slider('Satisfaction Level',  min_value=0.09, max_value=1.0, step=0.01)
last_evaluation = st.sidebar.slider('Last Evaluation',  min_value=0.36, max_value=1.0, step=0.01)
number_project = st.sidebar.slider('Number of Project	',  min_value=2.0, max_value=6.0, step=1.0)
average_montly_hours = st.sidebar.slider('Average Montly Hours',  min_value=96.0, max_value=310.0, step=1.0)
time_spend_company = st.sidebar.slider('Time Spend Company',  min_value=2.0, max_value=10.0, step=1.0)
Work_accident = st.sidebar.slider('Work Accident',  min_value=0.0, max_value=1.0, step=1.0)
promotion_last_5years = st.sidebar.slider('Promotion Last 5years',  min_value=0.0, max_value=1.0, step=1.0)
sales = st.sidebar.slider('Sales',  min_value=0.0, max_value=9.0, step=1.0)
salary = st.sidebar.slider('Salary',  min_value=0.0, max_value=2.0, step=1.0)

#satisfaction_level = math.ceil(satisfaction_level)
#last_evaluation = math.ceil(last_evaluation)
#number_project = math.ceil(number_project)
#average_montly_hours = math.ceil(average_montly_hours)
#time_spend_company = math.ceil(time_spend_company)
#Work_accident = math.ceil(Work_accident)
#promotion_last_5years = math.ceil(promotion_last_5years)
#sales = math.ceil(sales)
#salary = math.ceil(salary)

df1 = pd.DataFrame({'features': ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 
                                       'time_spend_company', 'Work_accident', 'promotion_last_5years', 'sales', 'salary'],
                     'values': [satisfaction_level, last_evaluation, number_project, average_montly_hours,
                                  time_spend_company, Work_accident, promotion_last_5years, sales, salary]})

#st.dataframe(df1)
st.set_option('deprecation.showPyplotGlobalUse', False)

df1['performance'] = df1['values'].cumsum()

#df1.plot(x="features", y=["performance"])
#st.pyplot()




if st.button("Submit"):
    features = [[satisfaction_level, last_evaluation, number_project, average_montly_hours, time_spend_company, 
             Work_accident, promotion_last_5years, sales, salary]]
    print(features)
    prediction = rf_clf.predict(features)

    lc = [str(i) for i in prediction]
    ans = int("".join(lc))
    if ans == 0:

        st.error(
        "Hello: " + emp_name +"  \n "
        "ID: "+ emp_id +'  \n'
        'Employee Will not leave the company.' + '  \n'
        ) 

        df1.plot(x="features", y=["performance"])
        st.pyplot()   
        if(satisfaction_level >= 0.5 and number_project >= 3.0):
            st.write("Performance Update: Employee Working status is good but need  \n to increase the paysacle and number of projects")        
    else:
        st.success(
        "Hello: " + emp_name + '  \n'
        "ID: "+ emp_id +'  \n'
        'Employee will leave the company.' + '  \n'
        )
        df1.plot(x="features", y=["performance"])
        st.pyplot() 
        if(satisfaction_level <= 0.09 and number_project <= 3.0):
            st.write("Performance Update: Increase the number of the projects of the Employee")
       
