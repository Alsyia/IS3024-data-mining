import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
from pandas.api.types import CategoricalDtype
import dateutil as du
from Schema import *

# Import dataset

data_file = "./Data/CIS_bdpm.txt"

drugs = pd.read_table(data_file, names=DRUGS_COLUMNS, encoding="latin-1")
drugs = drugs.set_index("CIS")

forms = pd.read_table("./Data/CIS_CIP_bdpm.txt", names=FORMS_COLUMNS, encoding="latin-1", sep="\t", index_col=False)
forms = forms.set_index("CIP7")

# TODO : Un médicament n'ayant pas de taux de remboursement (non-remboursé) ne devrait pas avoir d'honoraire de dispensation ?

# Jointure sur les médicaments et leurs présentations
forms_drugs = forms.join(drugs, on="CIS", lsuffix="_left", rsuffix="_right")
forms_drugs = forms_drugs[DRUGS_FORMS_REORDERED_COLUMNS]


# Clean all prices cause they have weird format (eg: 47,522,55, I assumed it means 47 522.55)
def clean_price(price):
    if type(price) == str:
        comma_pos = price.rfind(",")
        if comma_pos != -1:
            price = price[:comma_pos] + "." + price[comma_pos + 1:]
    return price


# Filter rows where there is no price
forms_drugs = forms_drugs[pd.notnull(forms_drugs['price'])]
forms_drugs['price'] = forms_drugs['price'].apply(clean_price)
forms_drugs['price'] = forms_drugs['price'].str.replace(",", "").astype(float)

# Merge reinbursement rates like "15 %" and "15%"
forms_drugs["reinbursement_rate"] = forms_drugs["reinbursement_rate"].str.replace(" ", "")
reinbursement_rates = CategoricalDtype(categories=["15%", "30%", "65%", "100%"], ordered=True)
forms_drugs["reinbursement_rate"] = forms_drugs["reinbursement_rate"].astype(reinbursement_rates)

# with pd.option_context("display.max_rows", 30000):
#     display(forms_drugs['price'])

# Transform all categorical fields into categorical datatype
for column in ["administrative_status",
               "galenic_form",
               "route_of_administration",
               "owners",
               "commercialisation_status_left",
               "commercialisation_status_right",
               "collectivities_aggreement",
               "administrative_status",
               "clearance_status",
               "clearance_type",
               "bdm_status",
               "enhanced_monitoring"]:
    forms_drugs[column] = forms_drugs[column].astype('category')
    # TODO: Decommentt this, analyze categories, and fix them when needed
    # For example, we sometimes have two or three different categories because there is a typo...
    print(f"Column {column} has values: {forms_drugs[column].cat.categories}")

with pd.option_context("display.max_seq_items", 30000):
    print(forms_drugs['galenic_form'].cat.categories)

# Transform all date fields into date datatype
for column in ["commercialisation_date",
               "clearance_date"]:
    forms_drugs[column] = forms_drugs[column].apply(du.parser.parse)
    print(forms_drugs[column])
# Make a subset to make operations faster
partfd = forms_drugs[:1000]

# Price distribution plot
# Display prices distribution
# sb.distplot(partfd["price"])
# plt.show()

# Price vs galenic form plot (not very useful, some outliers for comprimés/gelules/injections
# p = sb.stripplot(x="galenic_form", y="price", data=partfd)
# # TODO: Reduce font size
# p.set_xticklabels(p.get_xticklabels(), rotation=45)
# plt.show()

# partfd_codes = partfd.copy()
# partfd_codes["reinbursement_rate"] = partfd_codes["reinbursement_rate"].cat.codes
# # Reinbursement rate vs galenic form
# p = sb.stripplot(x="galenic_form", y="reinbursement_rate", data=partfd_codes, jitter=True)
# plt.show()

# Price vs reinbursement rate
# p = sb.stripplot(x="reinbursement_rate", y="price", data=partfd, jitter=True)
# plt.show()

# Price vs owner
# p = sb.boxplot(x="owners", y="price", data=partfd)
# p.set_xticklabels(p.get_xticklabels(), rotation=45)
# plt.show()

# Price vs commercialisation date
forms_drugs[['commercialisation_date','price']].set_index('commercialisation_date').plot()
plt.show()