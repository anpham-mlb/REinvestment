The purpose of the project is to help those who want to explore the price of the real estate market in Melbourne from 2016 - 2020. The dataset scraped from various websites were properties that are on market/off market at the time of the project starts. Through the dataset, people are likely to select properties based on some criteria such as number of floor area, number of rooms, number of parking spaces,...

After the dataset was cleaned, they will be put on Tableau to make visualisation.

Before running codes, it should be necessary to check the Chrome driver version on the computer. Then, Chrome driver with the respective version should be downloaded and put it on Python folder. At the time scraping data, Chrome version 87 was used (ChromeDriver 87.0.4280.88).

### Step 1: Scraped Melbourne property dataset from websites
- Got the Melbourne suburb dataset from https://en.wikipedia.org/wiki/List_of_Melbourne_suburbs -> [Mel] Wiki_suburbs.csv
- Cleaned [Mel] Wiki_suburbs.csv using Get_suburbs.py -> Clean_Mel_suburbs.csv
- Scraped dataset from onthehouse.com.au using Scrape.py -> [Mel] for_sale... and [Mel] off_market_...
- Store datasets in Scraped_Dataset.zip

### Step 2: Cleaned and combined scraped dataset
- Downloaded Melbourne property dataset from https://www.kaggle.com/anthonypino/melbourne-housing-market -> Kaggle_Melbourne_housing_FULL.csv
- Got the Melbourne region (North, West, East,...) dataset from https://www.onlymelbourne.com.au/list-of-melbourne-suburbs -> Suburb - Division - Council.csv
- Cleaned and combined Scraped_Dataset.zip and Kaggle_Melbourne_housing_FULL.csv and Suburb - Division - Council.csv using Clean_data.py -> Melbourne_property.xlsx

### Step 3: Scraped Melbourne suburb insight dataset from websites
- Got the Melbourne suburb code from ABS -> ABS_Suburb_code.csv
- Scraped Melbourne suburb insight dataset from ABS using Get_insights.py -> Suburb_insights.csv
- Cleaned Suburb_insights.csv using Clean_insightspy -> Clean_suburb_insight.csv

### Step 4: Made visualisation of dataset
- Datasets were visualised using Tableau
- There are three main datasets used in Tableau: Melbourne suburb shapefile (downloaed from ABS: https://drive.google.com/drive/folders/1L6bwtOoylRUJorMwzqVxAdy0q8HjhWpO?usp=sharing), Clean_suburb_insight.csv and Melbourne_property.xlsx
- The visualisation can be accessed via the link:https://public.tableau.com/profile/an.ho7452#!/vizhome/Melbourne_property/RealEstateDashboard?publish=yes

