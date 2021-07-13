from selenium import webdriver
import time

# Setup Driver
driver = webdriver.Chrome()

# Where I will gather data from
host = 'https://www.mapdevelopers.com/distance_from_to.php'

# Origins and destinations from excel spreadsheet
origins = ['78731', '78749']
destinations = ['3509 Mt. Barker Dr.']

# Object holding all the data
data = {
    'origin': {
        'location' : 289,
        'location2' : 239
    }
}

# Loop through each origin and mark its connection to each destination
for origin in origins:
    for destination in destinations:
        # Process destination to replace all spaces with html safe characters
        destination = destination.replace(' ', '%20')
        # Get Data from website
        driver.implicitly_wait(3)
        driver.get(host + f'?&from={origin}&to={destination}')
        distances = driver.find_element_by_id('driving_status')
        time.sleep(3)
        print(distances.text)
