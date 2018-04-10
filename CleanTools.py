import pandas as pd
from pandas.api.types import CategoricalDtype
import dateutil as du

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


def use_categorical_types(df):

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
        # print(f"Column {column} has values: {df[column].cat.categories}")


def use_date_types(df):
    # Transform all date fields into date datatype
    for column in ["commercialisation_date",
                   "clearance_date"]:
        df[column] = df[column].apply(du.parser.parse)