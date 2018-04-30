# -*- coding: utf-8 -*-

from Schema import *
from clean_tools import *
from Plots import *
# Import dataset
from sklearn.decomposition import PCA

# Variables
plot_info=True

drugs = pd.read_table("./Data/CIS_bdpm.txt", names=DRUGS_COLUMNS, encoding="windows-1252")
drugs = drugs.set_index("CIS")
drugs_cleaner = DrugsCleaner()
drugs_cleaner.clean(drugs)

forms = pd.read_table("./Data/CIS_CIP_bdpm.txt", names=FORMS_COLUMNS, encoding="windows-1252", sep="\t", index_col=False)
forms = forms.set_index("CIP7")
forms_cleaner = FormsCleaner()
forms_cleaner.clean(forms)

smr_file = "./Data/CIS_HAS_SMR_bdpm.txt"
smr = pd.read_table(smr_file, names=SMR_COLUMNS, encoding="windows-1252", sep="\t")
smr = simple_smr(smr)

asmr_file = "./Data/CIS_HAS_ASMR_bdpm.txt"
asmr = pd.read_table(asmr_file, names=ASMR_COLUMNS, encoding="windows-1252", sep="\t")
asmr = simple_asmr(asmr)

# TODO : Un médicament n'ayant pas de taux de remboursement (non-remboursé) ne devrait pas avoir d'honoraire de dispensation ?

# Jointure sur les médicaments et leurs présentations
forms_drugs = forms.merge(drugs, left_on="CIS", right_index=True, suffixes=("_left", "_right"))
forms_drugs = forms_drugs[DRUGS_FORMS_REORDERED_COLUMNS]

# Delete rows without price
forms_drugs = forms_drugs[pd.notnull(forms_drugs["price"])]

# # Clean price format
# clean_prices(forms_drugs, "price")
#
# # Clean reinbursement_rates
# clean_reinbursement_rates(forms_drugs, "reinbursement_rate")
#
# # Use correct types
# use_categorical_types(forms_drugs, print_galenic=False, print_route=False)
# use_date_types(forms_drugs)

#with pd.option_context("display.max_seq_items", 30000):
#    print(forms_drugs['galenic_form'].cat.categories)

# Joint with SMR and ASMR
df_smr = forms_drugs.merge(smr, how="left")
df_full = df_smr.merge(asmr, how="left")

# Make a subset to make operations faster
partfd = df_full[:1000]

if plot_info:
    plots_things_about_reinbursement_rate(partfd)
    # plots_things_about_price(partfd)


#Transforme l'etat de commercialisation en des variables string puis binaires
forms_drugs['commercialisation_status_right']=forms_drugs['commercialisation_status_right'].astype(str)
forms_drugs.loc[forms_drugs['commercialisation_status_right']=="Commercialisée","commercialisation_status_right"]=1
forms_drugs.loc[forms_drugs['commercialisation_status_right']=='Non commercialisée',"commercialisation_status_right"]=0

#Transforme le type de procédure en des variables string puis binaires (nationales ou non)
forms_drugs['clearance_type']=forms_drugs['clearance_type'].astype(str)
forms_drugs.loc[forms_drugs['clearance_type']=="Procédure nationale","clearance_type"]=1
forms_drugs.loc[forms_drugs['clearance_type']!="Procédure nationale","clearance_type"]=0

#Transforme le statut administratif en des variables string puis binaires (actives ou non)
forms_drugs['clearance_status']=forms_drugs['clearance_status'].astype(str)
forms_drugs.loc[forms_drugs['clearance_status']=="Autorisation active","clearance_status"]=1
forms_drugs.loc[forms_drugs['clearance_status']!="Autorisation active","clearance_status"]=0

#Transforme les agrément des collectivités en des variables string puis binaires (agrément ou non)
forms_drugs['collectivities_aggreement']=forms_drugs['collectivities_aggreement'].astype(str)
forms_drugs.loc[forms_drugs['collectivities_aggreement']=="oui","collectivities_aggreement"]=1
forms_drugs.loc[forms_drugs['collectivities_aggreement']=="non","collectivities_aggreement"]=0

#Transforme le statut administratif de la présentation en des variables string puis binaires (agrément ou non)
forms_drugs['administrative_status']=forms_drugs['administrative_status'].astype(str)
forms_drugs.loc[forms_drugs['administrative_status']=="Présentation abrogée","administrative_status"]=0
forms_drugs.loc[forms_drugs['administrative_status']=="Présentation active","administrative_status"]=1

forms_drugs['enhanced_monitoring']=forms_drugs['enhanced_monitoring'].astype(str)
forms_drugs.loc[forms_drugs['enhanced_monitoring']=="Non","enhanced_monitoring"]=0
forms_drugs.loc[forms_drugs['enhanced_monitoring']=="Oui","enhanced_monitoring"]=1

X = forms_drugs[['commercialisation_status_right','clearance_type','clearance_status','collectivities_aggreement','administrative_status','enhanced_monitoring']].values
#print(X)
pca = PCA()
pca.fit(X)
#print(pca.explained_variance_ratio_)
#print(pca.singular_values_)