import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.api import get

# Get the data
abs_code = pd.read_csv("ABS_Suburb_code.csv", header = None)
mel_sub = pd.read_csv("Clean_Mel_suburbs.csv")

# Edit Melbourne suburbs data
mel_sub["suburb"] = mel_sub["suburb"].apply(lambda i: i.split("-"))
mel_sub["suburb"] = mel_sub["suburb"].apply(lambda i: (" ").join(i[:-1]))
mel_sub["suburb"] = mel_sub["suburb"].apply(lambda i : i.title())

# Edit ABS code data
abs_code = abs_code[[0, 1]]
abs_code.columns = ["Code", "Suburb"]
abs_code = abs_code.drop(range(0,7), axis = 0).reset_index(drop = True)
abs_code = abs_code.dropna(subset = ["Suburb"])

def other_suburb(suburbs):
    other_suburb_index = []
    for suburb in suburbs:
        other_suburb_index.append([i for i in range(len(abs_code)) if suburb in abs_code["Suburb"][i]])
    other_suburb_index = [i for y in other_suburb_index for i in y]
    return other_suburb_index

other_suburb_index = other_suburb(["Qld", "SA", "WA", "Tas", "NT", "NSW", "ACT"])
abs_code = abs_code.drop(other_suburb_index, axis = 0).reset_index(drop = True)
abs_code["Suburb"] = abs_code["Suburb"].apply(lambda i: i.split(" (")[0])

abs_code["Order"] = range(len(abs_code))
abs_code["Sub_code"] = abs_code[["Suburb", "Order"]].apply(lambda i: {i[0] : i[1]}, axis = 1)
sub_order = abs_code["Sub_code"].tolist()
sub_order = [list(i.values())[0] for i in sub_order if list(i.keys())[0] in mel_sub["suburb"].tolist()]
abs_code = abs_code[["Code", "Suburb"]].iloc[sub_order].reset_index(drop = True)
abs_code.sort_values("Suburb", inplace = True)

abs_code.loc[len(abs_code)] = ["21614", "McCrae"]
abs_code.loc[len(abs_code)] = ["21618", "McKinnon"]
abs_code.loc[len(abs_code)] = ["21620", "McMahons Creek"]
abs_code.loc[len(abs_code)] = ["20827", "East Warburton"]
abs_code = abs_code.drop_duplicates()
abs_code.sort_values("Suburb", inplace = True)
abs_code = abs_code.reset_index(drop = True)

# Get the url of each suburb
urls = ["https://quickstats.censusdata.abs.gov.au/census_services/getproduct/census/2016/quickstat/SSC" + code + "?opendocument" for code in abs_code["Code"].tolist()]
urls.sort()

pages = [requests.get(url) for url in urls]
soups = [BeautifulSoup(page.content, "html.parser") for page in pages]

# Get suburbs
suburbs = [soup.find("h2", {"class" : "geo"}).text for soup in soups]

# Get figures for dwellings 
def get_insights(status):
    insights = []
    insight_soup = [soup.find_all("tr") for soup in soups]
    insight_soup = [soup for soups in insight_soup for soup in soups]
    for i in range(len(insight_soup)):
        if status in str(insight_soup[i]):
            insights.append(insight_soup[i].text)
            continue
    insights = [i.replace("\n", "/") for i in insights]
    return insights


def get_special_insights(status, place):
    insights = []
    insight_soup = [soup.find_all("tr") for soup in soups]
    insight_soup = [soup for soups in insight_soup for soup in soups]
    for i in range(len(insight_soup)):
        if status in str(insight_soup[i]):
            insights.append(insight_soup[i+place].text)
            continue
    insights = [i.replace("\n", "/") for i in insights]
    return insights

print(1_1, len(get_insights("Registered marital status")))
print(1,len(get_insights("Internet not accessed from dwelling")))
print(2, len(get_insights("Internet accessed from dwelling")))
print(3, len(get_special_insights("Internet accessed from dwelling", 1)))
print(4, len(get_insights("Median rent")))
print(5, len(get_insights("Households where rent payments are less than 30% of household income")))
print(6, len(get_insights("Households with rent payments greater than or equal to 30% of household income")))
print(6_1, len(get_insights("Median mortgage repayments")))
print(6_2, len(get_insights("Households where mortgage repayments are less than 30% of household income")))
print(6_3, len(get_insights("Households with mortgage repayments greater than or equal to 30% of household income")))
print(7, len(get_insights("Family households")))
print(8, len(get_insights("Single (or lone) person households")))
print(9, len(get_insights("Group households")))
print(10, len(get_insights("Less than $650 gross weekly income")))
print(11, len(get_insights("More than $3000 gross weekly income")))
print(12, len(get_special_insights("Unoccupied private dwellings", -1)))
print(13, len(get_insights("Unoccupied private dwellings")))
print(14, len(get_insights("Owned outright")))
print(15, len(get_insights("Owned with a mortgage")))
print(16, len(get_insights("Rented")))
print(17, len(get_insights("Other tenure type")))
print(18, len(get_insights("Tenure type not stated")))
print(18_1, len(get_insights("Both employed, worked full-time")))
print(18_2, len(get_insights("Both employed, worked part-time")))
print(18_3, len(get_insights("One employed full-time, one part-time")))
print(18_4, len(get_insights("One employed full-time, other not working")))
print(18_5, len(get_insights("One employed part-time, other not working")))
print(18_6, len(get_insights("Both not working")))
print(18_7, len(get_insights("Other (includes away from work)")))
print(18_8, len(get_insights("Labour force status not stated (by one or both parents in a couple family")))
print(18_9, len(get_insights("Couple family without children")))
print(18_10, len(get_insights("Couple family with children")))
print(18_11, len(get_insights("One parent family")))
print(18_12, len(get_insights("Other family")))
print(18_13, len(get_insights("Worked full-time")))
print(18_14, len(get_insights("Worked part-time")))
print(18_15, len(get_insights("Away from work")))
print(18_16, len(get_insights("Unemployed")))
print(18_17, len(get_insights("1-15 hours per week")))
print(18_18, len(get_insights("16-24 hours per week")))
print(18_19, len(get_insights("25-34 hours per week")))
print(18_20, len(get_insights("35-39 hours per week")))
print(18_21, len(get_insights("40 hours or more per week")))
print(19, len(get_insights("Personal")))
print(20, len(get_special_insights("Personal", 1)))
print(21, len(get_special_insights("Personal", 2)))
print(22, len(get_special_insights("Aboriginal and/or Torres Strait Islander people", -2)))
print(23, len(get_special_insights("Aboriginal and/or Torres Strait Islander people", -1)))
print(24, len(get_insights("Aboriginal and/or Torres Strait Islander people")))
print(24_1, len(get_special_insights("Aboriginal and/or Torres Strait Islander people", 2)))
print(25, len(get_insights("0-4 years")))
print(26, len(get_insights("5-9 years")))
print(27, len(get_insights("10-14 years")))
print(28, len(get_insights("15-19 years")))
print(29, len(get_insights("20-24 years")))
print(30, len(get_insights("25-29 years")))
print(31, len(get_insights("30-34 years")))
print(32, len(get_insights("35-39 years")))
print(33, len(get_insights("40-44 years")))
print(34, len(get_insights("45-49 years")))
print(35, len(get_insights("50-54 years")))
print(36, len(get_insights("55-59 years")))
print(37, len(get_insights("60-64 years")))
print(38, len(get_insights("65-69 years")))
print(39, len(get_insights("70-74 years")))
print(40, len(get_insights("75-79 years")))
print(41, len(get_insights("80-84 years")))
print(42, len(get_insights("85 years and over")))
print(43, len(get_insights("Married")))
print(44, len(get_insights("Separated")))
print(45, len(get_insights("Divorced")))
print(46, len(get_insights("Widowed")))
print(47, len(get_insights("Never married")))
print(48, len(get_insights("Registered marriage")))
print(49, len(get_insights("De facto marriage")))
print(50, len(get_insights("Not married")))
print(51, len(get_insights("Preschool")))
print(52, len(get_insights("Primary - Government")))
print(53, len(get_insights("Primary - Catholic")))
print(54, len(get_insights("Primary - other non Government")))
print(55, len(get_insights("Secondary - Government")))
print(56, len(get_insights("Secondary - Catholic")))
print(57, len(get_insights("Secondary - other non Government")))
print(58, len(get_insights("Technical or further education institution")))
print(59, len(get_insights("University or tertiary institution")))
print(60, len(get_special_insights("University or tertiary institution", 1)))
print(61, len(get_special_insights("University or tertiary institution", 2)))
print(62, len(get_insights("Bachelor Degree level and above")))
print(63, len(get_insights("Advanced Diploma and Diploma level")))
print(64, len(get_insights("Certificate level IV")))
print(65, len(get_insights("Certificate level III")))
print(66, len(get_insights("Year 12")))
print(67, len(get_insights("Year 11")))
print(68, len(get_insights("Year 10")))
print(69, len(get_special_insights("Year 10", 1)))
print(70, len(get_special_insights("Year 10", 2)))
print(71, len(get_insights("Year 9 or below")))
print(72, len(get_insights("No educational attainment")))
print(73, len(get_special_insights("No educational attainment", 1)))


# export into a csv file
data = {
    "Suburb" : get_insights("Registered marital status"),
    "Internet Accessed From Dwelling" : get_insights("Internet not accessed from dwelling"),
    "Internet Not Accessed From Dwelling" : get_insights("Internet accessed from dwelling"),
    "Not Stated Internet" : get_special_insights("Internet accessed from dwelling", 1),
    "Median Rent" : get_insights("Median rent"),
    # "Small Rent" : get_insights("Households where rent payments are less than 30% of household income"),
    # "Big Rent" : get_insights("Households with rent payments greater than or equal to 30% of household income"),
    "Median Mortgage Repayments" : get_insights("Median mortgage repayments"),
    # "Small Mortgage" : get_insights("Households where mortgage repayments are less than 30% of household income"),
    # "Big Mortgage" : get_insights("Households with mortgage repayments greater than or equal to 30% of household income"),
    "Family Households" : get_insights("Family households"),
    "Single (Or Lone) Person Households" : get_insights("Single (or lone) person households"),
    "Group Households" : get_insights("Group households"),
    "Small Income" : get_insights("Less than $650 gross weekly income"),
    "Big Income" : get_insights("More than $3000 gross weekly income"),
    "Occupied Private Dwellings" : get_special_insights("Unoccupied private dwellings", -1),
    "Unoccupied Private Dwellings" : get_insights("Unoccupied private dwellings"),
    "Owned Outright" : get_insights("Owned outright"),
    "Owned With a Mortgage" : get_insights("Owned with a mortgage"),
    "Rented" : get_insights("Rented"),
    "Other Tenure Type" : get_insights("Other tenure type"),
    "Tenure Type Not Stated" : get_insights("Tenure type not stated"),
    "Both Employed, Worked Full-time" : get_insights("Both employed, worked full-time"),
    "Both Employed, Worked Part-time" : get_insights("Both employed, worked part-time"),
    "One Employed Full-time, One Part-time" : get_insights("One employed full-time, one part-time"),
    "One Employed Full-time, Other Not Working" : get_insights("One employed full-time, other not working"),
    "One Employed Part-time, Other Not Working" : get_insights("One employed part-time, other not working"),
    "Both Not Working" : get_insights("Both not working"),
    "Other (Includes Away From Work)" : get_insights("Other (includes away from work)"),
    "Labour Force Status Not Stated (By One Or Both Parents In A Couple Family)" : get_insights("Labour force status not stated (by one or both parents in a couple family"),
    "Couple Family Without Children" : get_insights("Couple family without children"),
    "Couple Family With Children" : get_insights("Couple family with children"),
    "One Parent Family" : get_insights("One parent family"),
    "Other Family" : get_insights("Other family"),
    "Worked Full-time" : get_insights("Worked full-time"),
    "Worked Fart-time" : get_insights("Worked part-time"),
    "Away From Work" : get_insights("Away from work"),
    "Unemployed" : get_insights("Unemployed"),
    "1-15 hours per week" : get_insights("1-15 hours per week"),
    "16-24 hours per week" : get_insights("16-24 hours per week"),
    "25-34 hours per week" : get_insights("25-34 hours per week"),
    "35-39 hours per week" : get_insights("35-39 hours per week"),
    "40 hours or more per week" : get_insights("40 hours or more per week"),
    "Personal Median Income" : get_insights("Personal"),
    "Family Median Income" : get_special_insights("Personal", 1),
    "Household Median Income" : get_special_insights("Personal", 2),
    "Male Population" : get_special_insights("Aboriginal and/or Torres Strait Islander people", -2),
    "Female Population" : get_special_insights("Aboriginal and/or Torres Strait Islander people", -1),
    "Aboriginal and/or Torres Strait Islander people" : get_insights("Aboriginal and/or Torres Strait Islander people"),
    "Median Age" : get_special_insights("Aboriginal and/or Torres Strait Islander people", 2),
    "0-4 years" : get_insights("0-4 years"),
    "5-9 years" : get_insights("5-9 years"),
    "10-14 years" : get_insights("10-14 years"),
    "15-19 years" : get_insights("15-19 years"),
    "20-24 years" : get_insights("20-24 years"),
    "25-29 years" : get_insights("25-29 years"),
    "30-34 years" : get_insights("30-34 years"),
    "35-39 years" : get_insights("35-39 years"),
    "40-44 years" : get_insights("40-44 years"),
    "45-49 years" : get_insights("45-49 years"),
    "50-54 years" : get_insights("50-54 years"),
    "55-59 years" : get_insights("55-59 years"),
    "60-64 years" : get_insights("60-64 years"),
    "65-69 years" : get_insights("65-69 years"),
    "70-74 years" : get_insights("70-74 years"),
    "75-79 years" : get_insights("75-79 years"),
    "80-84 years" : get_insights("80-84 years"),
    "85 years and over" : get_insights("85 years and over"),
    "Married" : get_insights("Married"),
    "Separated" : get_insights("Separated"),
    "Divorced" : get_insights("Divorced"),
    "Widowed" : get_insights("Widowed"),
    "Never Married" : get_insights("Never married"),
    "Registered Marriage" : get_insights("Registered marriage"),
    "De Facto Marriage" : get_insights("De facto marriage"),
    "Not Married" : get_insights("Not married"),
    "Preschool" : get_insights("Preschool"),
    "Primary - Government" : get_insights("Primary - Government"),
    "Primary - Catholic" : get_insights("Primary - Catholic"),
    "Primary - other non Government" : get_insights("Primary - other non Government"),
    "Secondary - Government" : get_insights("Secondary - Government"),
    "Secondary - Catholic" : get_insights("Secondary - Catholic"),
    "Secondary - other non Government" : get_insights("Secondary - other non Government"),
    "Technical or further education institution" : get_insights("Technical or further education institution"),
    "University or tertiary institution" : get_insights("University or tertiary institution"),
    "Other Education" : get_special_insights("University or tertiary institution", 1),
    "Not Stated Education" : get_special_insights("University or tertiary institution", 2),
    "Bachelor Degree level and above" : get_insights("Bachelor Degree level and above"),
    "Advanced Diploma and Diploma level" : get_insights("Advanced Diploma and Diploma level"),
    "Certificate Level IV" : get_insights("Certificate level IV"),
    "Certificate Level III" : get_insights("Certificate level III"),
    "Year 12" : get_insights("Year 12"),
    "Year 11" : get_insights("Year 11"),
    "Year 10" : get_insights("Year 10"),
    "Certificate Level II" : get_special_insights("Year 10", 1),
    "Certificate Level I" : get_special_insights("Year 10", 2),
    "Year 9 Or Below" : get_insights("Year 9 or below"),
    "No Educational Attainment" : get_insights("No educational attainment"),
    "Not Stated Education" : get_special_insights("No educational attainment", 1)
}

headers = [
    "Suburb",
    "Available Internet",
    "Not Available Internet",
    "Not Stated Internet",
    "Median Rent",
    # "Small Rent",
    # "Big Rent",
    "Median Mortgage Repayments",
    # "Small Mortgage",
    # "Big Mortgage",
    "Family Households",
    "Single (or Lone) Person Households",
    "Group Households",
    "Small Income",
    "Big Income",
    "Occupied Private Dwellings",
    "Unoccupied private dwellings",
    "Owned outright",
    "Owned with a mortgage",
    "Rented",
    "Other tenure type",
    "Tenure type not stated",
    "Both employed, worked full-time",
    "Both employed, worked part-time",
    "One employed full-time, one part-time",
    "One employed full-time, other not working",
    "One employed part-time, other not working",
    "Both not working",
    "Other (includes away from work)",
    "Labour force status not stated (by one or both parents in a couple family)",
    "Couple family without children",
    "Couple family with children",
    "One parent family",
    "Other family",
    "Worked full-time",
    "Worked part-time",
    "Away from work",
    "Unemployed",
    "1-15 hours per week",
    "16-24 hours per week",
    "25-34 hours per week",
    "35-39 hours per week",
    "40 hours or more per week",
    "Personal Median Income",
    "Family Median Income",
    "Household Median Income",
    "Male Population",
    "Female Population",
    "Aboriginal and/or Torres Strait Islander people",
    "Median age",
    "0-4 years",
    "5-9 years",
    "10-14 years",
    "15-19 years",
    "20-24 years",
    "25-29 years",
    "30-34 years",
    "35-39 years",
    "40-44 years",
    "45-49 years",
    "50-54 years",
    "55-59 years",
    "60-64 years",
    "65-69 years",
    "70-74 years",
    "75-79 years",
    "80-84 years",
    "85 years and over",
    "Married",
    "Separated",
    "Divorced",
    "Widowed",
    "Never married",
    "Registered marriage",
    "De facto marriage",
    "Not married",
    "Preschool",
    "Primary - Government",
    "Primary - Catholic",
    "Primary - other non Government",
    "Secondary - Government",
    "Secondary - Catholic",
    "Secondary - other non Government",
    "Technical or further education institution",
    "University or tertiary institution",
    "Other Education",
    "Not Stated Education",
    "Bachelor Degree level and above",
    "Advanced Diploma and Diploma level",
    "Certificate level IV",
    "Certificate level III",
    "Year 12",
    "Year 11",
    "Year 10",
    "Certificate level II",
    "Certificate level I",
    "Year 9 or below",
    "No educational attainment",
    "Not Stated Education"
    ]


df = pd.DataFrame(data, columns = headers)
df.to_csv("Suburb_insights.csv", index = False)

