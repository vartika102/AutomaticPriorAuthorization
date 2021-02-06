from django.db import models

# Create your models here.

class Patient(models.Model):
    p_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    weight = models.IntegerField()
    height = models.IntegerField()

class Patient1():
    p_id: str
    name: str
    age: int
    gender: int
    weight: int
    height: float
    HPlan_Basic : int
    HPlan_Platinum : int
    HPlan_Gold : int
    addictive : int
    pre_treat : str
    pre_drug : str
    pre_drug_cost : int
    pre_treat_cost : int
    pre_med_cost : int
    alter_med_cost : int
    doc_exp : int
    prev_med_imp : int
    side_effects : int
    strength : float
    insurance_amount : int
    dosage : int
    len_of_therapy : int
    therapy_initiated : int
    reauth : int
    result : str
    amt_paid_insurance: float
    amt_out_of_pocket: float
    plan: str
    coins: str
    max_coins: int
    output: float