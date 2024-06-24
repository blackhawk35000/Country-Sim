import wbgapi as wb
import array as arr
import csv
import os,sys
import subprocess
import glob
from os import path

NUM_COUNTRY_CODES = 188
NUM_OF_QUERIES = 2
country_codes = ["Deadbeef"] * NUM_COUNTRY_CODES
countries = ["Deadbeef"] * (NUM_COUNTRY_CODES*14)
queries = ["GC.DOD.TOTL.CN","GC.DOD.TOTL.GD.ZS"]

def pullCodes(country_codes):
    with open('country_code.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            country_codes[i] = row["World_Bank_Code"]
            i+=1

def updatedata(country_codes, countries, query):
    i = 0
    c = 0
    if countries[c]=="Deadbeef":
        while i!=(NUM_COUNTRY_CODES):
            for row in wb.data.fetch(query, country_codes[i], range(2010, 2024)):
                countries[c] = [row['economy'], row['value'],  row['time']]
                c+=1
            i+=1
    else:
        while i!=(NUM_COUNTRY_CODES):
            for row in wb.data.fetch(query, country_codes[i], range(2010, 2024)):
                countries[c].append(row['value'])
                c+=1
            i+=1

def exportData(countries):
    i = 0
    with open('countryFinanceData.csv', 'w', newline='') as csvfile:
        dataWriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        dataWriter.writerow(['Copountry, Public Debt, Year, Public Debt/GDP'])
        while i<(NUM_COUNTRY_CODES*14):
            dataWriter.writerow([countries[i]])
            i+=1

def importPublicFinanceData():
    pullCodes(country_codes)
    i = 0
    while i<NUM_OF_QUERIES:
        print("importing " + queries[i] + "...." )
        updatedata(country_codes, countries, queries[i])
        i+=1
    exportData(countries)
