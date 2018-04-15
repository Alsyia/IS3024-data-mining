import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
from pandas.api.types import CategoricalDtype
import dateutil as du
from Schema import *
from CleanTools import *
from Plots import *
# Import dataset
from sklearn.decomposition import PCA

# Variables
plot_info=False

data_file = "./Data/CIS_bdpm.txt"

drugs = pd.read_table(data_file, names=DRUGS_COLUMNS, encoding="latin-1")
drugs = drugs.set_index("CIS")

forms = pd.read_table("./Data/CIS_CIP_bdpm.txt", names=FORMS_COLUMNS, encoding="latin-1", sep="\t", index_col=False)
forms = forms.set_index("CIP7")

# TODO : Un médicament n'ayant pas de taux de remboursement (non-remboursé) ne devrait pas avoir d'honoraire de dispensation ?

# Jointure sur les médicaments et leurs présentations
forms_drugs = forms.join(drugs, on="CIS", lsuffix="_left", rsuffix="_right")
forms_drugs = forms_drugs[DRUGS_FORMS_REORDERED_COLUMNS]

# Delete rows without price
forms_drugs = forms_drugs[pd.notnull(forms_drugs["price"])]

# Clean price format
clean_prices(forms_drugs, "price")

# Clean reinbursement_rates
clean_reinbursement_rates(forms_drugs, "reinbursement_rate")

# Use correct types
use_categorical_types(forms_drugs)
use_date_types(forms_drugs)

#with pd.option_context("display.max_seq_items", 30000):
#    print(forms_drugs['galenic_form'].cat.categories)

# Make a subset to make operations faster
partfd = forms_drugs[:1000]

if plot_info:
    plots_things_about_reinbursement_rate(partfd)
    plots_things_about_price(partfd)

pca = PCA()
forms_drugs['commercialisation_status_right']=forms_drugs['commercialisation_status_right'].astype(str)
forms_drugs.loc[forms_drugs['commercialisation_status_right']=="Commercialisée","commercialisation_status_right"]=1
forms_drugs.loc[forms_drugs['commercialisation_status_right']=='Non commercialisée',"commercialisation_status_right"]=0

forms_drugs['clearance_type']=forms_drugs['clearance_type'].astype(str)
forms_drugs.loc[forms_drugs['clearance_type']=="Procédure nationale","clearance_type"]=1
forms_drugs.loc[forms_drugs['clearance_type']!="Procédure nationale","clearance_type"]=0

forms_drugs['clearance_status']=forms_drugs['clearance_status'].astype(str)
forms_drugs.loc[forms_drugs['clearance_status']=="Autorisation active","clearance_status"]=1
forms_drugs.loc[forms_drugs['clearance_status']!="Autorisation active","clearance_status"]=0

forms_drugs['collectivities_aggreement']=forms_drugs['collectivities_aggreement'].astype(str)
forms_drugs.loc[forms_drugs['collectivities_aggreement']=="oui","collectivities_aggreement"]=1
forms_drugs.loc[forms_drugs['collectivities_aggreement']=="non","collectivities_aggreement"]=0

forms_drugs['administrative_status']=forms_drugs['administrative_status'].astype(str)
forms_drugs.loc[forms_drugs['administrative_status']=="Présentation abrogée","administrative_status"]=0
forms_drugs.loc[forms_drugs['administrative_status']=="Présentation active","administrative_status"]=1

forms_drugs['enhanced_monitoring']=forms_drugs['enhanced_monitoring'].astype(str)
forms_drugs.loc[forms_drugs['enhanced_monitoring']=="Non","enhanced_monitoring"]=0
forms_drugs.loc[forms_drugs['enhanced_monitoring']=="Oui","enhanced_monitoring"]=1

X = forms_drugs[['commercialisation_status_right','clearance_type','clearance_status','collectivities_aggreement','administrative_status','enhanced_monitoring']].values
print(X)
pca.fit(X)
print(pca.explained_variance_ratio_)
print(pca.singular_values_)