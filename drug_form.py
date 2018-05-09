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
from sklearn.metrics import confusion_matrix

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

# Jointure sur les médicaments et leurs présentations
forms_drugs = forms.merge(drugs, left_on="CIS", right_index=True, suffixes=("_left", "_right"))

#print(forms_drugs["commercialisation_date"])

# We fill missing price values
# We can use a price average
#forms_drugs["price"]=forms_drugs["price"].fillna(forms_drugs["price"].mean())
# Or we can user an interpolation
forms_drugs['price']=forms_drugs['price'].interpolate()

#print(forms_drugs['price'].head(50))
forms_drugs = forms_drugs[DRUGS_FORMS_REORDERED_COLUMNS]

# Joint with SMR and ASMR
df_smr = forms_drugs.merge(smr, how="left")
df_full = df_smr.merge(asmr, how="left")
df_full['ASMR_score']=df_full['ASMR_score'].interpolate()
df_full['SMR_score']=df_full['SMR_score'].interpolate()
df_full['ASMR_score']=df_full['ASMR_score'].fillna(0)
df_full['SMR_score']=df_full['SMR_score'].fillna(0)

if plot_info:
    # Make a subset to make operations faster
    partfd = df_full[:1000]
    #plots_things_about_reinbursement_rate(partfd)
    #plots_things_about_price(partfd)
    #print(forms_drugs.dtypes)
    print("Length of Form drugs is %i" %len(forms_drugs))
    print("Length of ASMR file is %i" %len(asmr))
    print("Length of SMR file  is %i" %len(smr))

print(df_full["A"])

target = "reinbursement_rate"
features = ["galenic_form_simplified",
            #"price",
            # "commercialisation_date",
            # "clearance_date",
            #"owners",
            'SMR_score',
            'ASMR_score',
            "collectivities_aggreement",
            "administrative_status",
            "clearance_status",
            "clearance_type",
            "bdm_status",
            "enhanced_monitoring",
            "I",
            "A",
            "P"]

df_dataset = df_full[[*features, target]]

df_dataset = df_dataset[pd.notnull(df_dataset["reinbursement_rate"])]
y = df_dataset[target]

x = df_dataset[features]
binary_mapping = binary_labels_encode(x)

x = multivalues_labels_encode(x, features)

x_train, x_test, y_train, y_test=train_test_split(x,y,test_size=0.25,shuffle=True)

clf = DecisionTreeClassifier(criterion = "gini",max_depth=6,min_samples_leaf=10,min_samples_split=10)
clf.fit(x_train, y_train)

predictions=clf.predict(x_test)

print(set(predictions))
print("Score : %.2f " %accuracy_score(y_test,predictions,normalize=True))

print("Confusion matrix")
print(confusion_matrix(y_test, predictions))

if plot_info:
    dot_data = tree.export_graphviz(clf,feature_names=x.columns,
                             filled=True, rounded=True,
                             class_names=['ZONE 1','ZONE 2','ZONE 3','ZONE 4'],
                             special_characters=True, out_file=None,leaves_parallel=True)

    graph = graphviz.Source(dot_data)
    graph.render("tree")