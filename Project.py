#Import the libraries
from flask import Flask,render_template,request,jsonify
import pickle
import requests
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
from werkzeug.utils import secure_filename
import os, sys, glob, re


#For Boston
boston=pickle.load(open('Boston_model.pickle','rb'))
#For Diabetis model
diabetis=pickle.load(open('Diabets.pickle','rb'))
#For Flight prediction
flight=pickle.load(open('Flight.pickle','rb'))
#Heart disease
heart=pickle.load(open('heart_model.pickle','rb'))
#IPL prediction
ipl=pickle.load(open('random_model_1.pickle','rb'))
#Chances of Admission
admin=pickle.load(open('Admission_model.pickle','rb'))
#Human resource analysis
classifier=pickle.load(open('Human_model.pkl','rb'))
#Loan approval prediction
loanapp=pickle.load(open('Load_model_pred.pickle','rb'))
#data science salry
salary=pickle.load(open('Data_scientist_new.pickle','rb'))
#Employee attrition
employee=pickle.load(open('Employee_model.pickle','rb'))
#Cardio vascular disease
cardio=pickle.load(open('Light_cardio.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def front():
    return render_template("frontend.html")

@app.route('/index')
def index():
    return render_template('index.html')


#-----------Boston-----------------


@app.route('/boston')  # route to display the home page
#@cross_origin()
def bostonhouse():
    return render_template("boston.html")


@app.route('/predictboston', methods=['POST'])  # route to show the predictions in a web UI
#@cross_origin()
def bostonpredict():
    if request.method == 'POST':
        #  reading the inputs given by the user
        crim = float(request.form['crim'])
        ZN = float(request.form['zn'])
        INDUS = float(request.form['indus'])
        CHAS = float(request.form['chas'])
        NOX = float(request.form['nox'])
        RM = float(request.form['rm'])
        AGE = float(request.form['age'])
        DIS = float(request.form['dis'])
        RAD = float(request.form['rad'])
        PTRATIO = float(request.form['ptratio'])
        B = float(request.form['b'])
        LSTAT = float(request.form['lstat'])
        prediction =boston.predict([[crim,ZN,INDUS,CHAS,NOX,RM,AGE,DIS,RAD,PTRATIO,B,LSTAT]])
        print('prediction is', prediction)
        # showing the prediction results in a UI
        return render_template('boston.html', prediction_text='Your estimated house price is: {}'.format(prediction[0]))

#------Diabetis prediction----------


@app.route('/diabetic')
def diabetic():
    return render_template('diabetis.html')


@app.route('/predictdiabetic',methods=['POST'])
def predictdiabetic():
    if request.method == 'POST':
        preg=float(request.form['pregnancies'])
        gluco=int(request.form['glucose'])
        blodd=float(request.form['bloodpressure'])
        skin=float(request.form['skinthickness'])
        insulin=float(request.form['insulin'])
        bmi=float(request.form['bmi'])
        diabet=float(request.form['diabetespedigreefunction'])
        age=int(request.form['age'])

        data=np.array([[preg,gluco,blodd,skin,insulin,bmi,diabet,age]])

        prediction=diabetis.predict(data)

        return render_template('diabetis.html',prediction=prediction)

#---------Flight fare prediction------------

@app.route('/flight')
def flightpr():
    return render_template('flight.html')

@app.route('/flightpredict',methods=['POST'])
def flightpredict():
    if request.method == 'POST':
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        Total_stops = int(request.form["stops"])
        # print(Total_stops)

        # Airline
        # AIR ASIA = 0 (not in column)
        airline = request.form['airline']
        if (airline == 'Jet Airways'):
            Jet_Airways = 1
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'IndiGo'):
            Jet_Airways = 0
            IndiGo = 1
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Air India'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 1
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Multiple carriers'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 1
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'SpiceJet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 1
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Vistara'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 1
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'GoAir'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 1
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Multiple carriers Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 1
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Jet Airways Business'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 1
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline == 'Vistara Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 1
            Trujet = 0

        elif (airline == 'Trujet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 1

        else:
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        # print(Jet_Airways,
        #     IndiGo,
        #     Air_India,
        #     Multiple_carriers,
        #     SpiceJet,
        #     Vistara,
        #     GoAir,
        #     Multiple_carriers_Premium_economy,
        #     Jet_Airways_Business,
        #     Vistara_Premium_economy,
        #     Trujet)

        # Source
        # Banglore = 0 (not in column)
        Source = request.form["Source"]
        if (Source == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

        elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        # print(s_Delhi,
        #     s_Kolkata,
        #     s_Mumbai,
        #     s_Chennai)

        # Destination
        # Banglore = 0 (not in column)
        Source = request.form["Destination"]
        if (Source == 'Cochin'):
            d_Cochin = 1
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'Delhi'):
            d_Cochin = 0
            d_Delhi = 1
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'New_Delhi'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'Hyderabad'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif (Source == 'Kolkata'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        # print(
        #     d_Cochin,
        #     d_Delhi,
        #     d_New_Delhi,
        #     d_Hyderabad,
        #     d_Kolkata
        # )

        #     ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
        #    'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
        #    'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
        #    'Airline_Jet Airways', 'Airline_Jet Airways Business',
        #    'Airline_Multiple carriers',
        #    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
        #    'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
        #    'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
        #    'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
        #    'Destination_Kolkata', 'Destination_New Delhi']

        prediction = flight.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi
        ]])

        output = round(prediction[0], 2)

        return render_template('flight.html', prediction_text="Your Flight price is Rs. {}".format(output))


#--------------ipl--------------#


@app.route('/ipl')  # route to display the home page
#@cross_origin()
def iplscore():
    return render_template("ipl.html")


@app.route('/iplpredict', methods=['POST'])  # route to show the predictions in a web UI
#@cross_origin()
def iplpredict():
    temp_array=list()
    if request.method == 'POST':
            #  reading the inputs given by the user
        runs=int(request.form['runs'])
        wickets=int(request.form['wickets'])
        overs=float(request.form['overs'])
        runs_last_5=int(request.form['runs_last_5'])
        wickets_last_5=int(request.form['wickets_last_5'])

        batting_team = request.form['bat_team']
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1, 0, 0, 0, 0, 0, 0, 0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0, 1, 0, 0, 0, 0, 0, 0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0, 0, 1, 0, 0, 0, 0, 0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0, 0, 0, 1, 0, 0, 0, 0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0, 0, 0, 0, 1, 0, 0, 0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0, 0, 0, 0, 0, 1, 0, 0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 1, 0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 1]

        bowling_team = request.form['bowl_team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1, 0, 0, 0, 0, 0, 0, 0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0, 1, 0, 0, 0, 0, 0, 0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0, 0, 1, 0, 0, 0, 0, 0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0, 0, 0, 1, 0, 0, 0, 0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0, 0, 0, 0, 1, 0, 0, 0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0, 0, 0, 0, 0, 1, 0, 0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 1, 0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0, 0, 0, 0, 0, 0, 0, 1]


        # predictions using the loaded model file
        temp_array = temp_array + [overs, runs, wickets, runs_last_5, wickets_last_5]
        data=np.array([temp_array])

        prediction = int(ipl.predict(data)[0])
        prediction_text='The final score predicted range is: '
        print('prediction is', prediction)
        # showing the prediction results in a UI
        return render_template('ipl.html',lower_limit='The final score predicted range is {}'.format(prediction - 10),upper_limit='-{}'.format(prediction + 5))


#------------Heart disease prediction----------


@app.route('/heart')
def heartscore():
    return render_template('heart.html')

@app.route('/heartpredict',methods=['POST'])
def heartpredict():
    if request.method == 'POST':
        age=int(request.form['age'])
        sex=request.form['sex']
        if (sex == 1):
            sex_1 = 1
            sex_0 = 0
        elif (sex == 0):
            sex_1 = 0
            sex_0 = 1
        else:
            sex_1 = 0
            sex_0 = 0
        cp=request.form['cp']
        if (cp == 'cp_0'):
            cp_0 = 1
            cp_1 = 0
            cp_2 = 0
            cp_3 = 0
        elif (cp == 'cp_1'):
            cp_0 = 0
            cp_1 = 1
            cp_2 = 0
            cp_3 = 0
        elif (cp == 'cp_2'):
            cp_0 = 0
            cp_1 = 0
            cp_2 = 1
            cp_3 = 0
        elif (cp == 'cp_3'):
            cp_0 = 0
            cp_1 = 0
            cp_2 = 0
            cp_3 = 1
        else:
            cp_0 = 0
            cp_1 = 0
            cp_2 = 0
            cp_3 = 0
        fbs=request.form['fbs']
        if (fbs == 'fbs_0'):
            fbs_0 = 1
            fbs_1 = 0
        elif (fbs == 'fbs_1'):
            fbs_0 = 0
            fbs_1 = 1
        else:
            fbs_0 = 0
            fbs_1 = 0
        rest=request.form['restecg']

        if (rest == 'restecg_0'):
            restecg_0 = 1
            restecg_1 = 0
            restecg_2 = 0
        elif (rest == 'restecg_1'):
            restecg_0 = 0
            restecg_1 = 1
            restecg_2 = 0
        elif (rest == 'restecg_2'):
            restecg_0 = 0
            restecg_1 = 0
            restecg_2 = 1
        else:
            restecg_0 = 0
            restecg_1 = 0
            restecg_2 = 0
        exang= request.form['exang']
        if (exang == 'exang_0'):
            exang_0 = 1
            exang_1 = 0
        elif (exang == 'exang_1'):
            exang_0 = 0
            exang_1 = 1
        else:
            exang_0 = 0
            exang_1 = 0
        slope=request.form['slope']
        if (slope == 'slope_0'):
            slope_0 = 1
            slope_1 = 0
            slope_2 = 0
        elif (slope == 'slope_1'):
            slope_0 = 0
            slope_1 = 1
            slope_2 = 0
        elif (slope == 'slope_2'):
            slope_0 = 0
            slope_1 = 0
            slope_2 = 1
        else:
            slope_0 = 0
            slope_1 = 0
            slope_2 = 0

        ca=request.form['ca']
        if (ca == 'ca_0'):
            ca_0 = 1
            ca_1 = 0
            ca_2 = 0
            ca_3 = 0
            ca_4 = 0
        elif (ca == 'ca_1'):
            ca_0 = 0
            ca_1 = 1
            ca_2 = 0
            ca_3 = 0
            ca_4 = 0
        elif (ca == 'ca_2'):
            ca_0 = 0
            ca_1 = 0
            ca_2 = 1
            ca_3 = 0
            ca_4 = 0
        elif (ca == 'ca_3'):
            ca_0 = 0
            ca_1 = 0
            ca_2 = 0
            ca_3 = 1
            ca_4 = 0
        elif (ca == 'ca_4'):
            ca_0 = 0
            ca_1 = 0
            ca_2 = 0
            ca_3 = 0
            ca_4 = 1
        else:
            ca_0 = 0
            ca_1 = 0
            ca_2 = 0
            ca_3 = 0
            ca_4 = 0
        thal=request.form['thal']
        if (thal == 'thal_0'):
            thal_0 = 1
            thal_1 = 0
            thal_2 = 0
            thal_3 = 0
        elif (thal == 'thal_1'):
            thal_0 = 0
            thal_1 = 1
            thal_2 = 0
            thal_3 = 0
        elif (thal == 'thal_2'):
            thal_0 = 0
            thal_1 = 0
            thal_2 = 1
            thal_3 = 0
        elif (thal == 'thal_3'):
            thal_0 = 0
            thal_1 = 0
            thal_2 = 0
            thal_3 = 1
        else:
            thal_0 = 0
            thal_1 = 0
            thal_2 = 0
            thal_3 = 0



        trest=int(request.form['trestbps'])
        chol=int(request.form['chol'])
        old=float(request.form['oldpeak'])

        data=np.array([[age,sex_0,sex_1,cp_0,cp_1,cp_2,cp_3,
                        fbs_0,fbs_1,restecg_0,restecg_1,restecg_2,
                        exang_0,exang_1,slope_0,slope_1,slope_2,
                        ca_0,ca_1,ca_2,ca_3,ca_4,thal_0,thal_1,thal_2,thal_3,trest,chol,old]])

        #scaled_data=sc.fit_tranform(data)

        prediction=heart.predict(data)

        return render_template('heart.html',prediction=prediction)


#----------------Admission-------------

@app.route('/admin',methods=['GET'])
def adminscore():
    return render_template("admission.html")

@app.route('/predictadmin',methods=['POST','GET'])
def adminpredict():
    if request.method == 'POST':
        gre_score= int(request.form['gre_score'])
        toefl_score= int(request.form['toefl_score'])
        university_rating= int(request.form['university_rating'])
        sop= float(request.form['sop'])
        lor= float(request.form['lor'])
        cgpa= float(request.form['cgpa'])
        is_research=request.form['research']
        if (is_research=='yes'):
            research=1
        else:
            research=0

        prediction=admin.predict([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]])
        print('prediction is',prediction)

        return render_template("admission.html",prediction='Your chances for admission in to UCLA is {} %'.format(round(100*prediction[0])))

@app.route('/car')
def car():
    return render_template('car.html')

@app.route('/carpredict',methods=['POST'])
def carpage():
    if request.method == 'POST':
        #  reading the inputs given by the user
        present_price = float(request.form['present_price'])
        kms_driven = float(request.form['kms_driven'])
        owner = float(request.form['owner'])
        no_year = float(request.form['no_year'])
        fuel =request.form['fuel_type']
        if (fuel == 'Diesel'):
            Fuel_Type_Diesel = 1
            Fuel_Type_Petrol = 0
        elif (fuel == 'Petrol'):
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 1
        else:
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 1
        sellar=int(request.form['Seller_Type_Individual'])
        transmission_manual=int(request.form['transmission_manual'])

        classifier=pickle.load(open('Reg_model_car.pkl','rb'))

        prediction =classifier.predict([[present_price,kms_driven,owner,no_year,
                                       Fuel_Type_Diesel,
                                       Fuel_Type_Petrol,
                                       sellar,
                                       transmission_manual]])
        print('prediction is', prediction)
        # showing the prediction results in a UI
        return render_template('car.html', prediction_text='Your estimated car price is: {}'.format(prediction[0]))

#--------Human resource analysis--------


@app.route('/human')
def human():
    return render_template('humanresource.html')


@app.route('/humanpredict', methods=['POST'])
def humanpage():
    if request.method == 'POST':
        city = int(request.form['city'])
        index_city = float(request.form['city_developement_index'])
        gender = int(request.form['gender'])
        exp = int(request.form['relevent_experience'])
        univer = int(request.form['enrolled_university'])
        educ_level = int(request.form['education_level'])
        exp_level = float(request.form['experience'])
        size = int(request.form['company_size'])
        new_job = float(request.form['last_new_job'])
        train_hours = float(request.form['training_hours'])

        major = request.form['major_discipline']

        if (major == 'Arts'):
            Arts = 1
            Bussiness_Degree = 0
            Humanities = 0
            STEM = 0
            No_Major = 0

        elif (major == 'Bussiness Degree'):
            Arts = 0
            Bussiness_Degree = 1
            Humanities = 0
            STEM = 0
            No_Major = 0

        elif (major == 'Humanities'):
            Arts = 0
            Bussiness_Degree = 0
            Humanities = 1
            STEM = 0
            No_Major = 0
        elif (major == 'STEM'):
            Arts = 0
            Bussiness_Degree = 0
            Humanities = 0
            STEM = 1
            No_Major = 0
        elif (major == 'No Major'):
            Arts = 0
            Bussiness_Degree = 0
            Humanities = 0
            STEM = 0
            No_Major = 1
        else:
            Arts = 0
            Bussiness_Degree = 0
            Humanities = 0
            STEM = 0
            No_Major = 0

        type = request.form['company_type']

        if (type == 'Early Stage Startup'):
            Early_Stage_Startup = 1
            Funded_Startup = 0
            NGO = 0
            Other = 0
            Public_Sector = 0
            Pvt_Ltd = 0
        elif (type == 'Funded Startup'):
            Early_Stage_Startup = 0
            Funded_Startup = 1
            NGO = 0
            Other = 0
            Public_Sector = 0
            Pvt_Ltd = 0
        elif (type == 'NGO'):
            Early_Stage_Startup = 0
            Funded_Startup = 0
            NGO = 1
            Other = 0
            Public_Sector = 0
            Pvt_Ltd = 0
        elif (type == 'Other'):
            Early_Stage_Startup = 0
            Funded_Startup = 0
            NGO = 0
            Other = 1
            Public_Sector = 0
            Pvt_Ltd = 0
        elif (type == 'Public Sector'):
            Early_Stage_Startup = 0
            Funded_Startup = 0
            NGO = 0
            Other = 0
            Public_Sector = 1
            Pvt_Ltd = 0
        elif (type == 'Pvt Ltd'):
            Early_Stage_Startup = 0
            Funded_Startup = 0
            NGO = 0
            Other = 0
            Public_Sector = 0
            Pvt_Ltd = 1
        else:
            Early_Stage_Startup = 0
            Funded_Startup = 0
            NGO = 0
            Other = 0
            Public_Sector = 0
            Pvt_Ltd = 0

        data = np.array([[city, index_city, gender, exp, univer, educ_level, exp_level,
                          size, new_job, train_hours, Arts, Bussiness_Degree, Humanities, STEM, No_Major,
                          Early_Stage_Startup,
                          Funded_Startup,
                          NGO,
                          Other,
                          Public_Sector,
                          Pvt_Ltd]])
        prediction = classifier.predict(data)

        return render_template('humanresource.html', prediction=prediction)



@app.route('/loan')
def loan():
    return render_template('loan.html')


@app.route('/loanpredict',methods=['POST'])
def loanpage():
    if request.method == 'POST':
        dependents=int(request.form['dependents'])
        loanAmount=np.log(float(request.form['loanAmount']))
        loan_amount_term=int(request.form['loan_amount_term'])
        credit_history	=float(request.form['credit_history'])
        total_income=np.log(float(request.form['total_income']))
        married=request.form['married']
        if (married == 'Married No'):
            Married_No = 1
            Married_Yes = 0
        elif (married == 'Married_Yes'):
            Married_No = 0
            Married_Yes = 1
        else:
            Married_No = 0
            Married_Yes = 0
        gender=request.form['gender']
        if (gender == 'Female'):
            Female = 1
            Male = 0
        elif (gender == 'Male'):
            Female = 0
            Male = 1
        else:
            Female = 0
            Male = 0
        education=request.form['education']
        if (education == 'Graduate'):
            Graduate = 1
            Not_Graduate = 0
        elif (education == 'Not Graduate'):
            Graduate = 0
            Not_Graduate = 1
        else:
            Graduate = 0
            Not_Graduate = 0
        self=request.form['self']
        if(self == 'self No'):
            self_No = 1
            self_Yes = 0
        elif (self == 'self_yes'):
            self_No = 0
            self_Yes = 1
        else:
            self_No = 0
            self_Yes = 0
        property=request.form['property_area']
        if (property == 'Rural'):
            Rural = 1
            Semiurban = 0
            Urban = 0
        elif (property == 'Semiurban'):
            Rural = 0
            Semiurban = 1
            Urban = 0
        elif (property == 'urban'):
            Rural = 0
            Semiurban = 0
            Urban = 1
        else:
            Rural = 0
            Semiurban = 0
            Urban = 0


        data=np.array([[dependents,loanAmount,loan_amount_term,credit_history,total_income,
                        Married_No,Married_Yes,Female,Male,
                        Graduate,Not_Graduate,self_No,self_Yes,
                        Rural,Semiurban,Urban]])




        prediction=loanapp.predict(data)

        return render_template('loan.html',prediction=prediction)



#--------------data science salary-------------

@app.route('/datascience')
def datascience():
    return render_template("datascience.html")


@app.route('/salarypredict', methods=['POST'])  # route to show the predictions in a web UI
#@cross_origin()
def datasciencepred():
    if request.method == 'POST':
        company_founded=float(request.form['company_founded'])
        company_size=int(request.form['company_size'])
        company_rating = float(request.form['company_rating'])
        revenue=float(request.form['revenue'])
        competitors=int(request.form['competitors'])
        Job_seniority=int(request.form['Job_seniority'])
        Job_in_headquarters=int(request.form['Job_in_headquarters'])
        job=request.form['jobs']
        if (job == 'Python_job'):
            Python_job =1
            Excel_job = 0
            Sql_job = 0
            Tableu_job = 0
        elif (job == 'Excel_job'):
            Python_job = 0
            Excel_job = 1
            Sql_job = 0
            Tableu_job = 0
        elif (job == 'Sql_job'):
            Python_job = 0
            Excel_job = 0
            Sql_job = 1
            Tableu_job = 0
        elif (job == 'Tableu_job'):
            Python_job = 0
            Excel_job = 0
            Sql_job = 0
            Tableu_job = 1
        else:
            Python_job = 0
            Excel_job = 0
            Sql_job = 0
            Tableu_job = 0

        ownership=request.form['ownership']
        if(ownership == 'Government'):
            Government = 1
            Hospital = 0
            Nonprofit_Organization = 0
            Other_Organization = 0
            Private = 0
            Public = 0
            Subsidiary_or_Business_Segment = 0
        elif (ownership == 'Hospital'):
            Government = 0
            Hospital = 1
            Nonprofit_Organization = 0
            Other_Organization = 0
            Private = 0
            Public = 0
            Subsidiary_or_Business_Segment = 0
        elif (ownership == 'Nonprofit_Organization'):
            Government = 0
            Hospital = 0
            Nonprofit_Organization = 1
            Other_Organization = 0
            Private = 0
            Public = 0
            Subsidiary_or_Business_Segment = 0
        elif (ownership == 'Other_Organization'):
            Government = 0
            Hospital = 0
            Nonprofit_Organization = 0
            Other_Organization = 1
            Private = 0
            Public = 0
            Subsidiary_or_Business_Segment = 0
        elif (ownership == 'Private'):
            Government = 0
            Hospital = 0
            Nonprofit_Organization = 0
            Other_Organization = 0
            Private = 1
            Public = 0
            Subsidiary_or_Business_Segment = 0
        elif (ownership == 'Public'):
            Government = 0
            Hospital = 0
            Nonprofit_Organization = 0
            Other_Organization = 0
            Private = 0
            Public = 1
            Subsidiary_or_Business_Segment = 0
        elif (ownership == 'Subsidiary_or_Business_Segment'):
            Government = 0
            Hospital = 0
            Nonprofit_Organization = 0
            Other_Organization = 0
            Private = 0
            Public = 0
            Subsidiary_or_Business_Segment = 1
        else:
            Government = 1
            Hospital = 0
            Nonprofit_Organization = 0
            Other_Organization = 0
            Private = 0
            Public = 0
            Subsidiary_or_Business_Segment = 0

        jobtitle=request.form['job_title']
        if (jobtitle == 'Job_title_data analyst'):
            Job_title_data_analyst = 1
            Job_title_data_engineer = 0
            Job_title_data_scientist = 0
            Job_title_director = 0
            Job_title_manager = 0
            Job_title_mle = 0
            Job_title_other = 0

        elif (jobtitle == 'Job_title_data_engineer'):
            Job_title_data_analyst = 0
            Job_title_data_engineer = 1
            Job_title_data_scientist = 0
            Job_title_director = 0
            Job_title_manager = 0
            Job_title_mle = 0
            Job_title_other = 0
        elif (jobtitle == 'Job_title_data_scientist'):
            Job_title_data_analyst = 0
            Job_title_data_engineer = 0
            Job_title_data_scientist = 1
            Job_title_director = 0
            Job_title_manager = 0
            Job_title_mle = 0
            Job_title_other = 0
        elif (jobtitle == 'Job_title_director'):
            Job_title_data_analyst = 0
            Job_title_data_engineer = 0
            Job_title_data_scientist = 0
            Job_title_director = 1
            Job_title_manager = 0
            Job_title_mle = 0
            Job_title_other = 0
        elif (jobtitle == 'Job_title_manager'):
            Job_title_data_analyst = 0
            Job_title_data_engineer = 0
            Job_title_data_scientist = 0
            Job_title_director = 0
            Job_title_manager = 1
            Job_title_mle = 0
            Job_title_other = 0
        elif (jobtitle == 'Job_title_mle'):
            Job_title_data_analyst = 0
            Job_title_data_engineer = 0
            Job_title_data_scientist = 0
            Job_title_director = 0
            Job_title_manager = 0
            Job_title_mle = 1
            Job_title_other = 0
        elif (jobtitle == 'Job_title_other'):
            Job_title_data_analyst = 0
            Job_title_data_engineer = 0
            Job_title_data_scientist = 0
            Job_title_director = 0
            Job_title_manager = 0
            Job_title_mle = 0
            Job_title_other = 1
        else:
            Job_title_data_analyst = 0
            Job_title_data_engineer = 0
            Job_title_data_scientist = 0
            Job_title_director = 0
            Job_title_manager = 0
            Job_title_mle = 0
            Job_title_other = 0

        sector= request.form['sector']
        if(sector == 'sector_Aerospace & Defense'):
            sector_Aerospace_Defense = 1
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 0
        elif (sector == 'sector_Biotech & Pharmaceuticals'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 1
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 0
        elif (sector == 'sector_Business Services'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 1
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 0
        elif (sector == 'sector_Education'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 1
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 0
        elif (sector == 'sector_Finance'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 1
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 0
        elif (sector == 'sector_Health Care'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 1
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 0
        elif (sector == 'sector_Information Technology'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 1
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 0

        elif (sector == 'sector_Insurance'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 1
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 0
        elif (sector == 'sector_Manufacturing'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 1
            sector_Others = 0
            sector_Retail = 0
        elif (sector == 'sector_Others'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 1
            sector_Retail = 0
        elif (sector == 'sector_Retail'):
            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 1
        else:

            sector_Aerospace_Defense = 0
            sector_Biotech_Pharmaceuticals = 0
            sector_Business_Services = 0
            sector_Education = 0
            sector_Finance = 0
            sector_Health_Care = 0
            sector_Information_Technology = 0
            sector_Insurance = 0
            sector_Manufacturing = 0
            sector_Others = 0
            sector_Retail = 0


        prediction =salary.predict([[company_founded,company_size,company_rating,revenue,
                                     competitors,Job_seniority,Job_in_headquarters,Python_job,Excel_job,Sql_job,Tableu_job,
                                     Government,Hospital,Nonprofit_Organization,Other_Organization,Private,Public,Subsidiary_or_Business_Segment,
                                     Job_title_data_analyst,Job_title_data_engineer,Job_title_data_scientist,Job_title_director,
                                     Job_title_manager,Job_title_mle,Job_title_other,
                                     sector_Aerospace_Defense,sector_Biotech_Pharmaceuticals,sector_Business_Services,sector_Education,
                                     sector_Finance,sector_Health_Care,sector_Information_Technology,sector_Insurance,
                                     sector_Manufacturing,sector_Others,sector_Retail]])
        print('prediction is', prediction)
        # showing the prediction results in a UI
        return render_template('datascience.html', prediction_text='The predicted data science salary is: {} $'.format(prediction[0]))


#-------------employee attrition------------

@app.route('/employee')
def hr():
    return render_template('hr.html')

@app.route('/employeepredict',methods=['POST'])
def hrpage():
    if request.method == 'POST':
        age=int(request.form['Age'])
        daily=int(request.form['DailyRate'])
        distance=int(request.form['DistanceFromHome'])
        Education=int(request.form['Education'])
        EnvironmentSatisfaction=int(request.form['EnvironmentSatisfaction'])
        HourlyRate=int(request.form['HourlyRate'])
        JobInvolvement=int(request.form['JobInvolvement'])
        JobLevel=int(request.form['JobLevel'])
        JobSatisfaction=int(request.form['JobSatisfaction'])
        MonthlyIncome=float(request.form['MonthlyIncome'])
        MonthlyRate=int(request.form['MonthlyRate'])
        NumCompaniesWorked=int(request.form['NumCompaniesWorked'])
        PerformanceRating=int(request.form['PerformanceRating'])
        RelationshipSatisfaction = int(request.form['RelationshipSatisfaction'])
        StockOptionLevel = int(request.form['StockOptionLevel'])
        TotalWorkingYears = int(request.form['TotalWorkingYears'])
        bussines = request.form['BusinessTravel']
        if (bussines == 'BusinessTravel_Travel_Frequently'):
            BusinessTravel_Travel_Frequently = 1
            BusinessTravel_Travel_Rarely = 0
        elif (bussines == 'BusinessTravel_Travel_Rarely'):
            BusinessTravel_Travel_Frequently = 0
            BusinessTravel_Travel_Rarely = 1
        else:
            BusinessTravel_Travel_Frequently = 0
            BusinessTravel_Travel_Rarely = 0

        depatment = request.form['Department']
        if (depatment == 'Department_Research & Development'):
            Department_Research_Development = 1
            Department_Sales = 0
        elif (depatment == 'Department_Sales'):
            Department_Research_Development = 0
            Department_Sales = 1
        else:
            Department_Research_Development = 0
            Department_Sales = 0


        educfield= request.form['EducationField']

        if (educfield == 'EducationField_Life Sciences'):
            EducationField_Life_Sciences = 1
            EducationField_Marketing = 0
            EducationField_Medical = 0
            EducationField_Other = 0
            EducationField_Technical_Degree = 0

        elif (educfield == 'EducationField_Marketing'):
            EducationField_Life_Sciences = 0
            EducationField_Marketing = 1
            EducationField_Medical = 0
            EducationField_Other = 0
            EducationField_Technical_Degree = 0

        elif (educfield == 'EducationField_Medical'):
            EducationField_Life_Sciences = 0
            EducationField_Marketing = 0
            EducationField_Medical = 1
            EducationField_Other = 0
            EducationField_Technical_Degree = 0
        elif (educfield == 'EducationField_Other'):
            EducationField_Life_Sciences = 0
            EducationField_Marketing = 0
            EducationField_Medical = 0
            EducationField_Other = 1
            EducationField_Technical_Degree = 0
        elif (educfield == 'EducationField_Technical_Degree'):
            EducationField_Life_Sciences = 0
            EducationField_Marketing = 0
            EducationField_Medical = 0
            EducationField_Other = 0
            EducationField_Technical_Degree = 1
        else:
            EducationField_Life_Sciences = 0
            EducationField_Marketing = 0
            EducationField_Medical = 0
            EducationField_Other = 0
            EducationField_Technical_Degree = 0

        gender = int(request.form['Gender_Male'])
        jobrole = request.form['JobRole']
        if (jobrole == 'JobRole_Human Resources'):
            JobRole_Human_Resources = 1
            JobRole_Laboratory_Technician = 0
            JobRole_Manager = 0
            JobRole_Manufacturing_Director = 0
            JobRole_Research_Director = 0
            JobRole_Research_Scientist = 0
            JobRole_Sales_Executive = 0
            JobRole_Sales_Representative = 0

        elif (jobrole == 'JobRole_Laboratory_Technician'):
            JobRole_Human_Resources = 0
            JobRole_Laboratory_Technician = 1
            JobRole_Manager = 0
            JobRole_Manufacturing_Director = 0
            JobRole_Research_Director = 0
            JobRole_Research_Scientist = 0
            JobRole_Sales_Executive = 0
            JobRole_Sales_Representative = 0
        elif (jobrole == 'JobRole_Manager'):
            JobRole_Human_Resources = 0
            JobRole_Laboratory_Technician = 0
            JobRole_Manager = 1
            JobRole_Manufacturing_Director = 0
            JobRole_Research_Director = 0
            JobRole_Research_Scientist = 0
            JobRole_Sales_Executive = 0
            JobRole_Sales_Representative = 0
        elif (jobrole =='JobRole_Manufacturing_Director'):
            JobRole_Human_Resources = 0
            JobRole_Laboratory_Technician = 0
            JobRole_Manager = 0
            JobRole_Manufacturing_Director = 1
            JobRole_Research_Director = 0
            JobRole_Research_Scientist = 0
            JobRole_Sales_Executive = 0
            JobRole_Sales_Representative = 0
        elif (jobrole == 'JobRole_Research_Director'):
            JobRole_Human_Resources = 0
            JobRole_Laboratory_Technician = 0
            JobRole_Manager = 0
            JobRole_Manufacturing_Director = 0
            JobRole_Research_Director = 1
            JobRole_Research_Scientist = 0
            JobRole_Sales_Executive = 0
            JobRole_Sales_Representative = 0
        elif (jobrole == 'JobRole_Research_Scientist'):
            JobRole_Human_Resources = 0
            JobRole_Laboratory_Technician = 0
            JobRole_Manager = 0
            JobRole_Manufacturing_Director = 0
            JobRole_Research_Director = 0
            JobRole_Research_Scientist = 1
            JobRole_Sales_Executive = 0
            JobRole_Sales_Representative = 0
        elif (jobrole == 'JobRole_Sales_Executive'):
            JobRole_Human_Resources = 0
            JobRole_Laboratory_Technician = 0
            JobRole_Manager = 0
            JobRole_Manufacturing_Director = 0
            JobRole_Research_Director = 0
            JobRole_Research_Scientist = 0
            JobRole_Sales_Executive = 1
            JobRole_Sales_Representative = 0
        elif (jobrole == 'JobRole_Sales_Representative'):
            JobRole_Human_Resources = 0
            JobRole_Laboratory_Technician = 0
            JobRole_Manager = 0
            JobRole_Manufacturing_Director = 0
            JobRole_Research_Director = 0
            JobRole_Research_Scientist = 0
            JobRole_Sales_Executive = 0
            JobRole_Sales_Representative = 1
        else:
            JobRole_Human_Resources = 0
            JobRole_Laboratory_Technician = 0
            JobRole_Manager = 0
            JobRole_Manufacturing_Director = 0
            JobRole_Research_Director = 0
            JobRole_Research_Scientist = 0
            JobRole_Sales_Executive = 0
            JobRole_Sales_Representative = 0

        MaritalStatus = request.form['MaritalStatus']

        if (MaritalStatus == 'MaritalStatus_Married'):
            MaritalStatus_Married = 1
            MaritalStatus_Single = 0
        elif (MaritalStatus == 'MaritalStatus_Single'):
            MaritalStatus_Married = 0
            MaritalStatus_Single = 1
        else:
            MaritalStatus_Married = 0
            MaritalStatus_Single = 0

        overt=int(request.form['OverTime_Yes'])


        data=np.array([[
            age,daily,distance,Education,EnvironmentSatisfaction,HourlyRate,
            JobInvolvement,JobLevel,JobSatisfaction,
            MonthlyIncome,MonthlyRate,NumCompaniesWorked,PerformanceRating,
            RelationshipSatisfaction,StockOptionLevel,TotalWorkingYears,
            BusinessTravel_Travel_Frequently,BusinessTravel_Travel_Rarely,
            Department_Research_Development,Department_Sales,
            EducationField_Life_Sciences,EducationField_Marketing,EducationField_Medical,
            EducationField_Other,EducationField_Technical_Degree,gender,JobRole_Human_Resources,
            JobRole_Laboratory_Technician,JobRole_Manager,JobRole_Manufacturing_Director,
            JobRole_Research_Director,JobRole_Research_Scientist,JobRole_Sales_Executive,
            JobRole_Sales_Representative,MaritalStatus_Married,MaritalStatus_Single,
            overt

        ]])



        scaled_data=sc.fit_transform(data)

        prediction=employee.predict(scaled_data)

        return render_template('hr.html',prediction=prediction)



#---------------cardio vascular disease--------------

@app.route('/cardio')
def cardiomodel():
    return render_template('cardio.html')


@app.route('/cardiopredict',methods=['POST'])
def cardiopred():
    if request.method == 'POST':
        ap_hi=np.log(float(request.form['ap_hi']))
        ap_lo=np.log(float(request.form['ap_lo']))
        cholesterol=int(request.form['cholesterol'])
        gluc=int(request.form['gluc'])
        smoke=int(request.form['smoke'])
        alco=int(request.form['alco'])
        active=int(request.form['active'])
        age=int(request.form['age_data'])
        bmi = float(request.form['bmi'])
        male=int(request.form['male'])

        data=np.array([[ap_hi,ap_lo,cholesterol,gluc,smoke,alco,active,age,
                        bmi,male]])

        scaled_data=sc.fit_transform(data)

        prediction=cardio.predict(scaled_data)

        return render_template('cardio.html',prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)