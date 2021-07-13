from selenium import webdriver
import time
import re
import pandas as pd

# Setup Driver
options = webdriver.chrome.options.Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Where I will gather data from
host = 'https://www.mapdevelopers.com/distance_from_to.php'

# Pull in spreadsheet from excel into pandas
df = pd.read_excel('distances.xlsm', header=1)
# Drop population column
df = df.drop('Unnamed: 1', axis=1)
# Fix columns
df.columns = ['zip'] + list(df.columns[1:])
# Purge useless rows (non data)
df = df.drop(0)

# Origins and destinations from excel spreadsheet
origins = list(df['zip'])
destinations = list(df.columns)[1:] # [1:] to ignore the zip column

# Object holding all the data
data = {}

# Saving function
def save_data(data, save_file):
    distances_df = pd.DataFrame.from_dict(data, orient='index')
    # distances_df.to_excel('data.xlsx')
    distances_df.to_csv(save_file, sep=',')

# Loop through each origin and mark its connection to each destination
for origin in origins:
    # Add origin to data set
    data[origin] = {}
    for destination in destinations:
        # Process destination to replace all spaces with html safe characters
        html_destination = destination.replace(' ', '%20')
        # Get Data from website
        driver.get(host + f'?&from={origin}&to={html_destination}')
        distances = driver.find_element_by_id('driving_status')
        # Rest for a bit so that the update can occur
        time.sleep(3)
        # Pull out miles
        miles = re.search(r'\d*\.?\d+', distances.text).group()
        # Add miles under destination label for origin
        data[origin][destination] = miles
    # Make a backup csv of each origin every time you go through
    save_data(data, 'data_partial.csv')
# Make the final one
save_data(data, 'data_final.csv')