from collections import defaultdict
from sklearn import preprocessing
import pandas as pd

def binary_labels_encode(df):

    mapping = defaultdict(preprocessing.LabelEncoder)
    # Only binary columns without null values shall go here
    columns = ["commercialisation_status_right",
               "collectivities_aggreement",
               "administrative_status"
               ]

    for column in columns:
        df[column] = mapping[column].fit_transform(df[column])

    return mapping

def multivalues_labels_encode(df, features):

    columns = ["galenic_form_simplified",
                          #"owners",
                          "commercialisation_status_left",
                          # "route_of_administration",
                          "clearance_status",
                          "clearance_type",
                          "bdm_status",
                          "enhanced_monitoring"]

    return pd.get_dummies(df, columns=columns)
