import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd

def plots_things_about_reinbursement_rate(df):

    # Price vs reinbursement rate
    sb.stripplot(x="price", y="reinbursement_rate", data=df, jitter=True)
    plt.show()

    sb.stripplot(x="commercialisation_date", y="reinbursement_rate", data=df, jitter=True)
    plt.show()

    sb.stripplot(x="clearance_date", y="reinbursement_rate", data=df, jitter=True)
    plt.show()

    print(pd.crosstab(df["reinbursement_rate"], df["clearance_type"]))

def plots_things_about_price(df):

    # Price distribution
    sb.distplot(df["price"])
    plt.show()

    # Price vs galenic form plot (not very useful, some outliers for comprimés/gelules/injections
    p = sb.stripplot(x="galenic_form", y="price", data=df)
    p.set_xticklabels(p.get_xticklabels(), rotation=45)
    plt.show()

    # Price vs reinbursement rate
    p = sb.stripplot(x="reinbursement_rate", y="price", data=df, jitter=True)
    plt.show()

    # Price vs owner
    p = sb.boxplot(x="owners", y="price", data=df)
    p.set_xticklabels(p.get_xticklabels(), rotation=45)
    plt.show()
