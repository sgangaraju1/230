
import pandas as pd

def get_attribute_person(row):
    return row["person"].replace(" ", "_")

def get_attribute_gender(row):
    if (row["Male"] > 0):
        return 'MALE'
    return 'FEMALE'

def get_attribute_race(row):
    race_max = max(row["Asian"], row["White"], row["Black"])
    if (row["Asian"] == race_max):
        return 'ASIAN'
    if (row["White"] == race_max):
        return "WHITE"
    return "BLACK"

def get_attribute_age(row):
    age_max = max(row["Child"], row["Youth"], row["Middle Aged"], row["Senior"])
    if (row["Child"] == age_max):
        return 'CHILD'
    if (row["Youth"] == age_max):
        return 'YOUTH'
    if (row["Middle Aged"] == age_max):
        return 'MIDAGE'
    return "SENIOR"

def fix_attribute_gender(df):
    df["Gender"] = df.apply(get_attribute_gender, axis=1)
    persons      = df.person.unique()
    for person in persons:
        df_person = df[(df.person == person)][["person", "Gender"]].groupby(["Gender"]).count()
        df_person = pd.DataFrame(df_person).reset_index()
        gender    = df_person.max()["Gender"]
        df.loc[df.person == person, "Gender"] = gender    
    return df

def fix_attribute_race(df):
    df["Race"]   = df.apply(get_attribute_race, axis=1)
    persons      = df.person.unique()
    for person in persons:
        df_person = df[(df.person == person)][["person", "Race"]].groupby(["Race"]).count()
        df_person = pd.DataFrame(df_person).reset_index()
        race      = df_person.max()["Race"]
        df.loc[df.person == person, "Race"] = race    
    return df

def fix_attribute_age(df):
    df["Age"]    = df.apply(get_attribute_age, axis=1)
    persons      = df.person.unique()
    for person in persons:
        df_person = df[(df.person == person)][["person", "Age"]].groupby(["Age"]).count()
        df_person = pd.DataFrame(df_person).reset_index()
        age       = df_person.max()["Age"]
        df.loc[df.person == person, "Age"] = age    
    return df