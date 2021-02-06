from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Patient, Patient1
import joblib
import pickle
import numpy as np
import csv
from django.contrib import messages
import tensorflow as tf

# Create your views here.

def index(request):
    return render(request, 'index.html')

def model2(vals):
    mean = [0.5205205205205206, 0.3613613613613614, 0.11811811811811812, 0.26226226226226224, 60389.53353353353, 50349.4629258517, 8.87987987987988, 0.42542542542542544, 2.234234234234234, 17.585585585585587, 0.38238238238238237]
    stddev = [0.49982895804858146, 0.4806355892856062, 0.3229095899297498, 0.44008480610037787, 29778.824937258923, 29381.88064042248, 4.963149331640322, 0.4946549922085418, 0.9544690731566037, 10.376211445433865, 0.4862126442213651]
    #vals = [0,1,0,0,75381,47663.0,5,1,1,30,0]
    Norm_vals = []
    for i in range(0,11):
        new_val = (vals[i]-mean[i])/stddev[i]
        Norm_vals.append(new_val)
    return(Norm_vals)

def calc(request):

    patient = Patient1()
    patient.p_id = request.POST['p_id']
    with open('Patient_DB.csv', 'r') as file:
        reader = csv.reader(file)
        flag =0
        for row in reader:
            if patient.p_id == row[0]:
                flag =1
                patient.name = row[1]
                patient.insurance_amount = int(row[4])
                patient.reauth = int(row[3])
                patient.plan = row[2]
                if row[2] == 'basic':
                    patient.HPlan_Basic = 1
                    patient.HPlan_Gold = 0
                    patient.HPlan_Platinum = 0
                elif row[2] == 'gold':
                    patient.HPlan_Basic = 0
                    patient.HPlan_Gold = 1
                    patient.HPlan_Platinum = 0
                else:
                    patient.HPlan_Basic = 0
                    patient.HPlan_Gold = 0
                    patient.HPlan_Platinum = 1
                break
        if flag == 0 :
            messages.info(request, 'Please Enter Registered Patient ID...If not Registered Please Register')
            return redirect('/')

            #patient_db.append(row)
    #print(patient_db)
    if patient.name != request.POST['name']:
        messages.info(request, 'Entered Patient Name does not belong to entered Patient ID')
        return redirect('/')
    patient.age = int(request.POST['age'])
    patient.gender = int(request.POST['gender'])
    patient.height = float(request.POST['height'])
    patient.weight = float(request.POST['weight'])
    patient.doc_exp = int(request.POST['doc_exp'])
    patient.prev_med_imp = int(request.POST['prev_med_imp'])
    patient.side_effects = int(request.POST['side_effects'])
    patient.strength = float(request.POST['strength'])
    patient.dosage = int(request.POST['dosage'])
    patient.len_of_therapy = int(request.POST['len_of_therapy'])
    patient.therapy_initiated = int(request.POST['therapy_initiated'])

    patient.pre_drug = request.POST['pre_drug']
    patient.pre_drug_cost = int(request.POST['pre_drug_cost'])
    patient.pre_treat = request.POST['pre_treat']
    patient.pre_treat_cost = int(request.POST['pre_treat_cost'])
    alter = 0
    patient.addictive = 0
    with open('drugs.csv', 'r') as file:
        reader = csv.reader(file)
        for r in reader:
            if r[0] == patient.pre_drug :
                #if patient.pre_treat_cost <= r[2] :
                #patient.alter_med_cost = r[1]
                alter = r[3]
                if r[4] == 'YES':
                    patient.addictive = 0
                else :
                    patient.addictive = 1



    with open('treatments.csv', 'r') as file:
        reader = csv.reader(file)
        for r in reader:
            if r[0] == patient.pre_treat :
                #if patient.pre_treat_cost <= r[2] :
                patient.alter_med_cost = r[1] + alter



    patient.pre_med_cost = patient.pre_treat_cost + patient.pre_drug_cost
    #patient.alter_med_cost = patient.pre_med_cost
    
     
    l = [patient.HPlan_Basic, patient.HPlan_Gold, patient.HPlan_Platinum, patient.age, patient.height,
    patient.gender, patient.weight, patient.addictive, patient.pre_med_cost, patient.alter_med_cost,
    patient.doc_exp, patient.prev_med_imp, patient.side_effects, patient.insurance_amount,
    patient.strength, patient.dosage, patient.len_of_therapy, patient.therapy_initiated,patient.reauth]
    
    #print(l)

    model_ = joblib.load('finalised.sav')
    #
    #a2 = np.array([l])
    #ans = model_.predict(a2)
    #print(ans)
    #model_ = joblib.load('Prior_Auth.sav')
    #new_model = tf.keras.models.load_model('saved_model.pb')

    vals = [0,1,0,0,75381,47663.0,5,1,1,30,0]
    norm_vals = model2(vals)
    print(norm_vals)
    
    patient.output = 0.5
    ans = patient.output

    if int(ans) >= 0.8 :
        patient.result = "Rejected" 
    else :
        with open('Plans.csv', 'r') as file:
            reader = csv.reader(file)
            for r in reader:
                if r[0] == patient.plan:
                    patient.coins = str(float(r[1])*100)+'%'
                    patient.max_coins = '$'+r[2]
                    patient.amt_out_of_pocket = float(r[1])*patient.pre_med_cost
                    if patient.amt_out_of_pocket > float(r[2]):
                        patient.amt_out_of_pocket = float(r[2])
                    patient.amt_paid_insurance = patient.pre_med_cost - patient.amt_out_of_pocket
                    if patient.insurance_amount < patient.amt_paid_insurance :
                        patient.result = "Partially Accepted"
                    else:
                        patient.result = "Accepted"

    #print("Gender :",patient.gender)

    #patient = Patient(name=name, gender=gender, age=12, height=12, weight=30)
    #patient.save()
    print('user created')
    #return redirect('/')
    return render(request, "result.html", {'patient':patient})
    
    
    
    #model_ = joblib.load('dt.sav')
    '''patient = Patient1()
    patient.p_id = request.POST['p_id']
    with open('Patient_DB.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if patient.p_id == row[0]:
                patient.name = row[1]
                patient.insurance_amount = int(row[4])
                patient.reauth = int(row[3])
                if row[2] == 'basic':
                    patient.HPlan_Basic = 1
                    patient.HPlan_Gold = 0
                    patient.HPlan_Platinum = 0
                elif row[2] == 'gold':
                    patient.HPlan_Basic = 0
                    patient.HPlan_Gold = 1
                    patient.HPlan_Platinum = 0
                else:
                    patient.HPlan_Basic = 0
                    patient.HPlan_Gold = 0
                    patient.HPlan_Platinum = 1
                break
            #patient_db.append(row)
    #print(patient_db)
    if patient.name != request.POST['name']:
        messages.info(request, 'Wrong Name')
        return redirect('/')
    patient.age = int(request.POST['age'])
    patient.gender = int(request.POST['gender'])
    patient.height = float(request.POST['height'])
    patient.weight = float(request.POST['weight'])
    patient.doc_exp = int(request.POST['doc_exp'])
    patient.prev_med_imp = int(request.POST['prev_med_imp'])
    patient.side_effects = int(request.POST['side_effects'])
    patient.strength = float(request.POST['strength'])
    patient.dosage = int(request.POST['dosage'])
    patient.len_of_therapy = int(request.POST['len_of_therapy'])
    patient.therapy_initiated = int(request.POST['therapy_initiated'])

    patient.pre_drug = request.POST['pre_drug']
    patient.pre_drug_cost = int(request.POST['pre_drug_cost'])
    patient.pre_treat = request.POST['pre_treat']
    patient.pre_treat_cost = int(request.POST['pre_treat_cost'])

    patient.pre_med_cost = patient.pre_treat_cost + patient.pre_drug_cost
    #patient.alter_med_cost = patient.alter_drug_cost + patient.alter_treat_cost
    #patient.addictive = 0
     
    l = [patient.HPlan_Basic, patient.HPlan_Gold, patient.HPlan_Platinum, patient.age, patient.height,
    patient.gender, patient.weight, patient.addictive, patient.pre_med_cost, patient.alter_med_cost,
    patient.doc_exp, patient.prev_med_imp, patient.side_effects, patient.insurance_amount,
    patient.strength, patient.dosage, patient.len_of_therapy, patient.therapy_initiated,patient.reauth]
    
    print(l)
    #model_ = joblib.load('finalised.sav')
    #inp=([[0,0,1,37.0,5.2,2,45,0,10456,23456,9,1,0,98231,200,3,10,0,1]])
    #a2 = np.array(inp)
    #ans = model_.predict(a2)
    #print(ans)
    ans = 1
    #ans = cls.predict([lis])
    #patient = Patient()
    #name = request.POST['name']
    #patient.age = request.POST['age']
    #gender = request.POST['gender']
    #patient = Patient(name=name, gender=gender, age=12, height=12, weight=30)
    #patient.save()
    print('user created')
    #return redirect('/')
    return render(request, "result.html", {'patient':patient})'''

def home(request):
    return render(request, 'home.html', {'name':'Jinny'})

def add(request):
    value1 = int(request.POST['num1'])
    value2 = int(request.POST['num2'])
    return render(request, "result.html", {'result':value1+value2})