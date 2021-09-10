import streamlit as st
import pandas as pd
import joblib
import math
import random

import altair as alt

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


#Loading Our final trained RF model 
model= open("hr_model.sav", "rb")
rf_clf=joblib.load(model)



st.set_page_config(layout="wide", )
st.title("HR Analysis: Employee Attrition Prediction")

st.sidebar.subheader("Choose Company")
Company = st.sidebar.selectbox("Companies", ("Paytm AI", "Amazon AI", "Google Brain", "SeAsia Infotech"))

st.sidebar.subheader("Choose Department")
Department = st.sidebar.selectbox("Department", ("Sales", "Accounts", "HR", "Technical", "IT", "Support"))

col1, col2, col3 = st.columns(3)


with col1:
    
    ## Employee Name
    emp_name = st.text_input('Employee Name of:  ' + Company + "  and Department:  " + Department + ' \n' )
    ## Employee ID
    emp_id = st.text_input('Employee ID')

    ## Experiance in months
    ## Employee ID
    
    st.subheader("Select Experiance in Months")
    months = st.slider('Months',  min_value=1, max_value=100, step=1)

    if months <= 12:
        salary = round(random.uniform(10000, 15000))
            
    elif months >=13 and months <=25:
        salary = round(random.uniform(15000, 20000))
            
    elif months >=26 and months <=35:
        salary = round(random.uniform(20000, 30000))
            
    elif months >=36 and months <=45:
        salary = round(random.uniform(40000, 40000))  
            
    elif months >=46 and months <=55:
        salary = round(random.uniform(40000, 50000))
            
    elif months >=56 and months <=65:
        salary = round(random.uniform(50000, 60000))   
            
    elif months >=66 and months <=75:
        salary = round(random.uniform(60000, 70000))
            
    elif months >=76 and months <=85:
        salary = round(random.uniform(70000, 80000))     
            
    elif months >=86 and months <=100:
        salary = round(random.uniform(80000, 90000))
            
    else:
        print("Enter months between 1 - 100")

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
#salary = st.sidebar.slider('Salary',  min_value=0.0, max_value=2.0, step=1.0)

with col2:
    st.subheader("You choose these values")
    st.markdown(f"**satisfaction_level:** {satisfaction_level:}")
    st.markdown(f"**last_evaluation:** {last_evaluation:}")
    st.markdown(f"**number_project:** {number_project:}")
    st.markdown(f"**average_montly_hours:** {average_montly_hours:}")
    st.markdown(f"**time_spend_company:** {time_spend_company:}")
    st.markdown(f"**Work_accident:** {Work_accident:}")
    st.markdown(f"**promotion_last_5years:** {promotion_last_5years:}")
    st.markdown(f"**sales:** {sales:}")


df1 = pd.DataFrame({'features': ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours', 
                                       'time_spend_company', 'Work_accident', 'promotion_last_5years', 'sales'],
                     'values': [satisfaction_level, last_evaluation, number_project, average_montly_hours,
                                  time_spend_company, Work_accident, promotion_last_5years, sales]})

st.set_option('deprecation.showPyplotGlobalUse', False)

perfor_meter = ((average_montly_hours + time_spend_company) // 2)
perfor_meter = int(perfor_meter)



df1['performance'] = df1['values'].cumsum()

df2 = pd.DataFrame({'Performance': ['perfor_meter'],
                     'Performance Meter': [perfor_meter]})


with col3:
    st.subheader("Choose Monthly Hours and Company Time Spend for Performance")

if st.button("Submit"):
    features = [[satisfaction_level, last_evaluation, number_project, average_montly_hours, time_spend_company, 
             Work_accident, promotion_last_5years, sales, 2]]
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

        with col3:
            st.subheader("Choose Monthly Hours and Company Time Spend for Performance")
            chart = alt.Chart(df2).mark_bar().encode(
            alt.X("Performance", bin=False),
            y='Performance Meter').properties(width=100)
            st.altair_chart(chart)
        
        #df1.plot(x="features", y=["performance"])
        #st.pyplot()   
        
        st.write("Performance Update: Employee Working status is good but need  \n to increase the paysacle and number of projects")        
        st.markdown(f"**The Employee Salary is or expected:** {salary:}")

    else:
        st.success(
        "Hello: " + emp_name + '  \n'
        "ID: "+ emp_id +'  \n'
        'Employee will leave the company.' + '  \n'
        )
        
        with col3:
            #st.subheader("Choose Monthly Hours and Company Time Spend for Performance")
            chart = alt.Chart(df2).mark_bar().encode(
            alt.X("Performance", bin=False),
            y='Performance Meter').properties(width=100)
            st.altair_chart(chart)

        #df1.plot(x="features", y=["performance"])
        #st.pyplot() 
        
        st.write("Performance Update: Increase the number of the projects of the Employee")
        st.markdown(f"**The Employee Salary is or expected:** {salary:}")
       
