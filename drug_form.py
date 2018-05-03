# -*- coding: utf-8 -*-

from Schema import *
from clean_tools import *
from Plots import *
# Import dataset
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from preprocessing_tools import *
import graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# Variables
plot_info=False

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

# Joint with SMR and ASMR
df_smr = forms_drugs.merge(smr, how="left")
df_full = df_smr.merge(asmr, how="left")

# Make a subset to make operations faster
partfd = df_full[:1000]

if plot_info:
    plots_things_about_reinbursement_rate(partfd)
    # plots_things_about_price(partfd)

print(forms_drugs.dtypes)

target = "reinbursement_rate"
features = ["galenic_form_simplified",
            # "price",
            # "commercialisation_date",
            # "clearance_date",
            #"owners",
            "commercialisation_status_left",
            "collectivities_aggreement",
            "administrative_status",
            #"route_vect",
            #"route_of_administration",
            "clearance_status",
            "clearance_type",
            "commercialisation_status_right",
            "bdm_status",
            "enhanced_monitoring",
            # 'Insuffisant',
            # 'Faible',
            # 'Modéré',
            # 'Important',
            # "I",
            # "II",
            # "III",
            # "IV",
            # "V"
            ]


df_dataset = df_full[[*features, target]]

df_dataset = df_dataset[pd.notnull(df_dataset["reinbursement_rate"])]
y = df_dataset[target]

x = df_dataset[features]
binary_mapping = binary_labels_encode(x)

x = multivalues_labels_encode(x, features)

x_train, x_test, y_train, y_test=train_test_split(x,y)

# Info about DecisionTreeClassifiers http://scikit-learn.org/stable/modules/tree.html#tree
clf = DecisionTreeClassifier()
clf.fit(x_train, y_train)
print(clf.score(x_train, y_train))

predictions=clf.predict(x_test)

print(set(predictions))

print("Score : %.2f " %accuracy_score(y_test,predictions,normalize=True))

if plot_info:
    dot_data = tree.export_graphviz(clf,feature_names=x.columns,
                             class_names=target,
                             filled=True, rounded=True,
                             special_characters=True, out_file=None)

    graph = graphviz.Source(dot_data)
    graph.render("tree")