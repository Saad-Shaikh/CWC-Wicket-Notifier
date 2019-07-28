from bs4 import BeautifulSoup
from selenium import webdriver
import re
from playsound import playsound
import sys
import json

# set options for Chrome
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("PATH/TO/chromedriver", options=options)

# open cricbuzz, get html using BeautifulSoup and scrape only the required <div> from the html
driver.get("https://www.cricbuzz.com/cricket-match/live-scores")
source = driver.page_source
content = BeautifulSoup(source, "html.parser")
scraped = content.find('div', attrs={"class": "cb-lv-scrs-col text-black"}).text
print(scraped)

# split the text in div to get the overs and runs/wickets
regex = re.compile('\s+')
split_data = regex.split(scraped)
print(split_data)

regex1 = re.compile('\(')
overs = regex1.split(split_data[2])

regex2 = re.compile('/')
numbers = regex2.split(split_data[1])
print(numbers, overs[1])
if (len(numbers) != 2) or (len(overs) != 2):
    print('The match doesn\'t seem to be going on right now\nExiting process')
    sys.exit()

currwicket = numbers[1]
dataarr = []
filename = split_data[0] + "_vs_" + split_data[5] + ".json"

while float(overs[1]) != 50:
    driver.get("https://www.cricbuzz.com/cricket-match/live-scores")
    source = driver.page_source
    content = BeautifulSoup(source, "html.parser")
    scraped = content.find('div', attrs={"class": "cb-lv-scrs-col text-black"}).text
    # print(scraped)

    regex = re.compile('\s+')
    split_data = regex.split(scraped)
    # print(split_data)

    regex1 = re.compile('\(')
    overs = regex1.split(split_data[2])

    regex2 = re.compile('/')
    numbers = regex2.split(split_data[1])
    if (len(numbers) != 2) or (len(overs) != 2):
        print('The match doesn\'t seem to be going on right now\nExiting process')
        sys.exit()
    print(numbers, overs[1])

    newwicket = numbers[1]
    if int(newwicket) > int(currwicket):
        playsound('office.mp3')
        dataobj = {
            "runs": numbers[0],
            "wickets": numbers[1],
            "overs": overs[1]
        }
        dataarr.append(dataobj)
        with open(filename, 'w') as outfile:
            json.dump(dataarr, outfile)
        currwicket = newwicket

print('Seems like 50 overs have been completed\nExiting process')
