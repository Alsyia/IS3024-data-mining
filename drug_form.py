import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
from pandas.api.types import CategoricalDtype
import dateutil as du
from Schema import *
from CleanTools import *
from Plots import *
# Import dataset

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

with pd.option_context("display.max_seq_items", 30000):
    print(forms_drugs['galenic_form'].cat.categories)

# Make a subset to make operations faster
partfd = forms_drugs[:1000]

if plot_info:
    plots_things_about_reinbursement_rate(partfd)
    plots_things_about_price(partfd)

#print(forms_drugs.head(3))