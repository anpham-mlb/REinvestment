import pandas as pd

# Get the data 
suburb = pd.read_csv("[Mel] Wiki_suburbs.csv", header = None)
suburb.columns = ["suburb"]

special_list = []
for i in range(len(suburb)):
    if "(" in suburb["suburb"].iloc[i]:
        special_list.append(i)
suburb["suburb"].iloc[special_list] = suburb["suburb"].iloc[special_list].apply(lambda i: i.split(" ("))
suburb["suburb"].iloc[special_list] = suburb["suburb"].iloc[special_list].str[0]
suburb["postcode"] = suburb["suburb"].apply(lambda i: i.split(" "))
suburb["postcode"] = suburb["postcode"].str[-1]

code_list = []
for i in range(len(suburb)):
    if suburb["postcode"].iloc[i].isdigit() is not True:
        code_list.append(i)

suburb = suburb.drop(suburb.index[code_list])
suburb["suburb"] = suburb["suburb"].apply(lambda i: i.lower())
suburb["suburb"] = suburb["suburb"].apply(lambda i: i.split(" "))
suburb["suburb"] = suburb["suburb"].apply(lambda i: "-".join(i))
suburb = suburb.drop_duplicates()
suburb = suburb.sort_values(by = ["suburb"])
suburb = suburb["suburb"].reset_index(drop = True)
suburb.iloc[496] = "east-warburton-3799"
suburb = suburb.drop([190,472, 319, 352], axis = 0).reset_index(drop = True)


suburb.to_csv("Clean_Mel_suburbs.csv", index = False)

# ['Capel Sound', 'Flemington, Victoria', 'Manor Lakes', 'Mccrae', 'Mckinnon', 'Mcmahons Creek', 'Monash University', 'No Longer An Official Name, But Stocksville Post Office Was Open Until', 'Tooradin North', 'Warburton East']