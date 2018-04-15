# -*- coding: utf-8 -*-

import pandas as pd
from pandas.api.types import CategoricalDtype
import dateutil as du
import numpy as np

# with pd.option_context("display.max_rows", 30000):
#     display(forms_drugs['price'])


# Clean prices
def clean_prices(df, col_name="price"):

    # Clean all prices cause they have weird format (eg: 47,522,55, I assumed it means 47 522.55)
    def clean_price(price):
        if type(price) == str:
            comma_pos = price.rfind(",")
            if comma_pos != -1:
                price = price[:comma_pos] + "." + price[comma_pos + 1:]
        return price

    df[col_name] = df[col_name].apply(clean_price)
    df[col_name] = df[col_name].str.replace(",", "").astype(float)


def clean_reinbursement_rates(df, col_name="reinbursement_rate"):
    """Make reinbursement_rate a categorical value and merge rates like 15 % and 15%"""

    df[col_name] = df[col_name].str.replace(" ", "")
    reinbursement_rates = CategoricalDtype(categories=["15%", "30%", "65%", "100%"], ordered=True)
    df[col_name] = df[col_name].astype(reinbursement_rates)


def use_categorical_types(df, print_galenic=False, print_route=False):

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
        df[column] = df[column].astype('category')

        # TODO: Decommentt this, analyze categories, and fix them when needed
        # For example, we sometimes have two or three different categories because there is a typo...
        #print(f"Column {column} has values: {df[column].cat.categories}")

    df.loc[df['galenic_form']=='capsule molle ou','galenic_form']='capsule molle'
    df["galenic_form_simplified"]=df["galenic_form"]

    df["galenic_form_simplified"]=df["galenic_form_simplified"].astype('str')

    df.loc[df['galenic_form'].str.contains('émulsion'),"galenic_form_simplified"]="émulsion"
    df.loc[df['galenic_form'].str.contains('comprimé'),"galenic_form_simplified"]="comprimé"
    df.loc[df['galenic_form'].str.contains('ovule'),"galenic_form_simplified"]="ovule"
    df.loc[df['galenic_form'].str.contains('capsule'),"galenic_form_simplified"]="capsule"
    df.loc[df['galenic_form'].str.contains('collyre'),"galenic_form_simplified"]="collyre"
    df.loc[df['galenic_form'].str.contains('granules'),"galenic_form_simplified"]="granules"
    df.loc[df['galenic_form'].str.contains('granulés'),"galenic_form_simplified"]="granules"
    df.loc[df['galenic_form'].str.contains('suppositoire'),"galenic_form_simplified"]="suppositoire"
    df.loc[df['galenic_form'].str.contains('lotion'),"galenic_form_simplified"]="lotion"
    df.loc[df['galenic_form'].str.contains('lyophilisat'),"galenic_form_simplified"]="lyophilisat"
    df.loc[df['galenic_form'].str.contains('implant'),"galenic_form_simplified"]="implant"
    df.loc[df['galenic_form'].str.contains('pâte'),"galenic_form_simplified"]="pâte"
    df.loc[df['galenic_form'].str.contains('pilule'),"galenic_form_simplified"]="pilule"
    df.loc[df['galenic_form'].str.contains('pommade'),"galenic_form_simplified"]="pommade"
    df.loc[df['galenic_form'].str.contains('pansement'),"galenic_form_simplified"]="pansement"
    df.loc[df['galenic_form'].str.contains('vernis'),"galenic_form_simplified"]="vernis"
    df.loc[df['galenic_form'].str.contains('microgranule'),"galenic_form_simplified"]="granules"
    df.loc[df['galenic_form'].str.contains('gélule'),"galenic_form_simplified"]="gélule"
    df.loc[df['galenic_form'].str.contains('mousse'),"galenic_form_simplified"]="mousse"
    df.loc[df['galenic_form'].str.contains('poudre'),"galenic_form_simplified"]="poudre"
    df.loc[df['galenic_form'].str.contains('suspension'),"galenic_form_simplified"]="suspension"
    df.loc[df['galenic_form'].str.contains('solution'),"galenic_form_simplified"]="solution"
    df.loc[df['galenic_form'].str.contains('crème'),"galenic_form_simplified"]="autre"
    df.loc[df['galenic_form'].str.contains('dispositif'),"galenic_form_simplified"]="autre"
    df.loc[df['galenic_form'].str.contains('emplâtre'),"galenic_form_simplified"]="autre"
    df.loc[df['galenic_form'].str.contains('film'),"galenic_form_simplified"]="autre"
    df.loc[df['galenic_form'].str.contains('gel'),"galenic_form_simplified"]="autre"

    if print_galenic==True:
        print("\nForme pharmaceutiques disponibles après nettoyage")
        for form in sorted(df['galenic_form_simplified'].unique()):
            print(form)

    # We build a vectorized representation of route of administration
    all_routes=[]
    for elem in df["route_of_administration"].cat.categories:
        elem_sp = elem.split(";")
        for route in elem_sp:
            if route not in all_routes:
                all_routes.append(route)

    if print_route ==True:
        print("\nVoie d'administration disponible après nettoyage")
        for administration in sorted(all_routes):
            print(administration)

    #print("Length of the route admin vector is %i" % len(all_routes))

    def f_vectorize(elem__list):
        all_vect=[]
        for elem in elem__list:
            vect=[0]*len(all_routes)
            for i in range(0,len(all_routes)):
                if all_routes[i] in elem.split(";"):
                    vect[i]=1
            all_vect.append(vect)
        return all_vect
    df['route_vect'] = f_vectorize(df['route_of_administration'])

def use_date_types(df):
    # Transform all date fields into date datatype
    for column in ["commercialisation_date",
                   "clearance_date"]:
        df[column] = df[column].apply(du.parser.parse)