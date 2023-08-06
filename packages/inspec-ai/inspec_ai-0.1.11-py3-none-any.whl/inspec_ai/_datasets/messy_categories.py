import pandas as pd
import numpy as np
import os


edi = ["Edinburgh", "edinburgh", "Edinborgh", "Edenburgh", "Ed1burgh", "3d!burgh"]
london = ["Lond0n", "Londen", "Londin", "London", "Londoon", "nodonl"]
toronto = ["Toronto", "Toromto", "TO", "to"]
montreal = ["Montreal", "montreal", "montréal", "Montréal", "mlt", "MTL", "Mtl"]
california = [
    "CA",
    "ca",
    "Ca",
    "Caliphornia",
    "Californa",
    "Calfornia",
    "calipornia",
    "CAL",
    "CALI",
]

male = ["Male", "M", "m", "male", "mal"]
female = ["Female", "F", "f", "female", "femal"]

bach = ["Bachelor", "bachelor", "bachelors", "Bachelors", "b"]
married = ["married", "Married", "maried", "m"]
widow = ["widow", "Widow", "w"]

doctorat = ["phd", "PHD", "doctorate", "doctor", "doctor of philosophy"]
high_school = ["high school", "HS", "hs", "Highh School"]

lakers = ["Los Angeles Lakers", "Lakers"]
raptors = ["Toronto Raptors", "Raptors", "To Raptors"]
apple = [
    "Apple Inc.",
    "apple inc",
    "apple inc.",
    " Apple inc",
    "Apple inc ",
    "aplple",
    "apple incorporated",
]

arnold = [
    "C. Arnold",
    "C Arnold",
    "c. arnold",
    "C.. Arnold",
    "Arnold",
    "Charles Arnold",
]
josephine = ["C. Josephine", "Jo", "Josephine", "josephine", "Christie Josephine"]
carol = ["Carol", "carl", "A. Carol", "Caroll", "Areminde Carol"]


nb_rows = 1000

places = list(np.random.choice(edi + london + montreal + toronto + california, nb_rows))
sex = list(np.random.choice(male + female, nb_rows))
cie_names = list(np.random.choice(raptors + apple + lakers, nb_rows))
people_names = list(np.random.choice(arnold + carol + josephine, nb_rows))
education = list(np.random.choice(high_school + doctorat, nb_rows))
marital_status = list(np.random.choice(bach + married + widow, nb_rows))

height = np.random.random((nb_rows))
width = np.random.random((nb_rows))
depth = np.random.random((nb_rows))
ROI_ratio = np.random.random((nb_rows))

age = np.random.randint(0, high=100, size=nb_rows)
is_a_customer = np.random.randint(0, high=2, size=nb_rows)
type_of_subscription = np.random.randint(0, high=5, size=nb_rows)
years_since_last_attending_to_a_wedding = np.random.randint(0, high=10, size=nb_rows)

df = pd.DataFrame(
    {
        "places": places,
        "sex": sex,
        "cie_names": cie_names,
        "people_names": people_names,
        "education": education,
        "marital_status": marital_status,
        "height": height,
        "width": width,
        "depth": depth,
        "ROI_ratio": ROI_ratio,
        "age": age,
        "is_a_customer": is_a_customer,
        "type_of_subscription": type_of_subscription,
        "years_since_last_attending_to_a_wedding": years_since_last_attending_to_a_wedding,
    }
)


# randomnly adding missing values
for col in df.columns:
    df.loc[df.sample(frac=0.1).index, col] = None


if not os.path.exists("./out"):
    os.makedirs("./out")

df.to_csv(".out/with_null_data_messy_categories.csv", header=True, index=None)
