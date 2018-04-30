# -*- coding: utf-8 -*-

import dateutil as du
from pandas.api.types import CategoricalDtype
import numpy as np
from functools import partial
import inspect

import pandas as pd

# with pd.option_context("display.max_rows", 30000):
#     display(forms_drugs['price'])


class FormsCleaner:

    def __init__(self):
        super().__init__()

    def clean(self, df):

        methods = [FormsCleaner.clean_null_prices,
                   FormsCleaner.clean_prices_format,
                   FormsCleaner.clean_reinbursement_rates,
                   FormsCleaner.clean_categorical_types,
                   FormsCleaner.clean_dates]

        for method in methods:
            method(df)

    @staticmethod
    def clean_null_prices(df):
        df = df[pd.notnull(df["price"])]

    @staticmethod
    def clean_prices_format(df, col_name="price"):
        # Clean all prices cause they have weird format (eg: 47,522,55, I assumed it means 47 522.55)
        def clean_price(price):
            if type(price) == str:
                comma_pos = price.rfind(",")
                if comma_pos != -1:
                    price = price[:comma_pos] + "." + price[comma_pos + 1:]
            return price

        df[col_name] = df[col_name].apply(clean_price)
        df[col_name] = df[col_name].str.replace(",", "").astype(float)

    @staticmethod
    def clean_reinbursement_rates(df, col_name="reinbursement_rate"):
        """Make reinbursement_rate a categorical value and merge rates like 15 % and 15%"""

        df[col_name] = df[col_name].str.replace(" ", "")
        reinbursement_rates = CategoricalDtype(categories=["15%", "30%", "65%", "100%"], ordered=True)
        df[col_name] = df[col_name].astype(reinbursement_rates)

    @staticmethod
    def clean_categorical_types(df):

        # Transform all categorical fields into categorical datatype
        for column in ["administrative_status",
                       "commercialisation_status",
                       "collectivities_aggreement"]:
            df[column] = df[column].astype('category')

    @staticmethod
    def clean_dates(df):

        partial_parser = partial(du.parser.parse, dayfirst=True)
        for column in ["commercialisation_date"]:
            df[column] = df[column].apply(partial_parser)


class DrugsCleaner:

    def __init__(self):
        super().__init__()

    def clean(self, df):

        methods = [DrugsCleaner.clean_galenic_forms,
                   DrugsCleaner.clean_categorical_types,
                   DrugsCleaner.clean_routes,
                   DrugsCleaner.clean_dates]

        for method in methods:
            method(df)

    @staticmethod
    def clean_galenic_forms(df, print_galenic=False):

        df.loc[df['galenic_form'] == 'capsule molle ou', 'galenic_form'] = 'capsule molle'
        df["galenic_form_simplified"] = df["galenic_form"]

        def merge_galenic_forms(base_form, new_form=None):

            if new_form is None:
                new_form = base_form

            df.loc[df['galenic_form'].str.contains(base_form), "galenic_form_simplified"] = new_form
        merge_galenic_forms("émulsion")
        merge_galenic_forms("comprimé")
        merge_galenic_forms("ovule")
        merge_galenic_forms("capsule")
        merge_galenic_forms("collyre")
        merge_galenic_forms("granules")
        merge_galenic_forms("granulés", "granules")
        merge_galenic_forms("suppositoire")
        merge_galenic_forms("lotion")
        merge_galenic_forms("lyophilisat")
        merge_galenic_forms("implant")
        merge_galenic_forms("pâte")
        merge_galenic_forms("pilule")
        merge_galenic_forms("pommade")
        merge_galenic_forms("pansement")
        merge_galenic_forms("vernis")
        merge_galenic_forms("microgranule", "granules")
        merge_galenic_forms("gélule")
        merge_galenic_forms("mousse")
        merge_galenic_forms("poudre")
        merge_galenic_forms("suspension")
        merge_galenic_forms("solution")
        # ?
        merge_galenic_forms("crème", "autre")
        merge_galenic_forms("dispositif", "autre")
        merge_galenic_forms("emplâtre", "autre")
        merge_galenic_forms("film", "autre")
        merge_galenic_forms("gel", "autre")

        df["galenic_form_simplified"] = df["galenic_form_simplified"].astype('str')

        if print_galenic:
            print("\nForme pharmaceutiques disponibles après nettoyage")
            for form in sorted(df['galenic_form_simplified'].unique()):
                print(form)

    @staticmethod
    def clean_categorical_types(df):

        # Transform all categorical fields into categorical datatype
        for column in ["galenic_form",
                       "route_of_administration",
                       "owners",
                       "commercialisation_status",
                       "clearance_status",
                       "clearance_type",
                       "bdm_status",
                       "enhanced_monitoring"]:
            df[column] = df[column].astype('category')

    @staticmethod
    def clean_routes(df, print_route=False):
        # We build a vectorized representation of route of administration
        all_routes = []
        for elem in df["route_of_administration"].cat.categories:
            elem_sp = elem.split(";")
            for route in elem_sp:
                if route not in all_routes:
                    all_routes.append(route)

        if print_route:
            print("\nVoie d'administration disponible après nettoyage")
            for administration in sorted(all_routes):
                print(administration)

        # print("Length of the route admin vector is %i" % len(all_routes))

        def f_vectorize(elem__list):
            all_vect = []
            for elem in elem__list:
                vect = [0] * len(all_routes)
                for i in range(0, len(all_routes)):
                    if all_routes[i] in elem.split(";"):
                        vect[i] = 1
                all_vect.append(vect)
            return all_vect

        df['route_vect'] = f_vectorize(df['route_of_administration'])

    @staticmethod
    def clean_dates(df):

        partial_parser = partial(du.parser.parse, dayfirst=True)
        for column in ["clearance_date"]:
            df[column] = df[column].apply(partial_parser)


def simple_smr(smr):
    # We can have different reviews for a same drug if this drug has different usages
    # A way to simplify data is then to count reviews by type (very good, good, bad, etc) for each drug

    smr["date_avis_commission_transparence"] = smr["date_avis_commission_transparence"].astype(str)
    smr["date_avis_commission_transparence"] = smr["date_avis_commission_transparence"].apply(du.parser.parse)
    smr["SMR_value"] = smr["SMR_value"].astype("category")
    grouped_smr = smr.groupby("CIS")
    filtered_smr = grouped_smr.apply(lambda x: x[x["date_avis_commission_transparence"] == x["date_avis_commission_transparence"].max()])

    simple_smr = filtered_smr.groupby("CIS")["SMR_value"].value_counts().unstack(fill_value=0)
    simple_smr["CIS"] = simple_smr.index

    def weights_func(comment, not_defined, insufficient, low, moderate, high):


        return 0*comment + 0*not_defined + -3*insufficient + 1*low + 2*moderate + 6*high

    categories = ['Commentaires',
                  'Non précisé',
                  'Insuffisant',
                  'Faible',
                  'Modéré',
                  'Important',
                  ]

    simple_smr["SMR_score"] = np.vectorize(weights_func)(*[simple_smr[cat] for cat in categories])

    return simple_smr

def simple_asmr(asmr):
    # We can have different reviews for a same drug if this drug has different usages
    # A way to simplify data is then to count reviews by type (very good, good, bad, etc) for each drug

    asmr["date_avis_commission_transparence"] = asmr["date_avis_commission_transparence"].astype(str)
    asmr["date_avis_commission_transparence"] = asmr["date_avis_commission_transparence"].apply(du.parser.parse)

    asmr["ASMR_value"] = asmr["ASMR_value"].astype("category")
    grouped_asmr = asmr.groupby("CIS")
    filtered_asmr =  grouped_asmr.apply(lambda x: x[x["date_avis_commission_transparence"] == x["date_avis_commission_transparence"].max()])
    simple_asmr = filtered_asmr.groupby("CIS")["ASMR_value"].value_counts().unstack(fill_value=0)
    simple_asmr["CIS"] = simple_asmr.index

    def weights_func(comment, not_defined, not_relevant, one, two, three, four, five):

        # An ASMR of 5 means improvement is inexistant, while an ASMR of one means the drug
        # is a major breakthrough

        return 0*comment +\
               0*not_defined +\
               0*not_relevant +\
               5*one +\
               4*two +\
               3*three +\
               2*four +\
               1*five


    categories = ["Commentaires sans chiffrage de l'ASMR",
                  "Non précisée",
                  "Sans objet",
                  "I",
                  "II",
                  "III",
                  "IV",
                  "V"]

    simple_asmr["ASMR_score"] = np.vectorize(weights_func)(*[simple_asmr[cat] for cat in categories])

    return simple_asmr


