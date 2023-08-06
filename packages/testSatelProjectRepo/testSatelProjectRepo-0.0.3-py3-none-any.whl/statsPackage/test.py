import urllib.request
import json
import statistics
import operator
import collections
import pandas
from collections import OrderedDict


#Read DB URL
def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        jsonData = json.loads(data)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData

#select year from date
def parseDateTime(date):
    return date[0:4]

def main():
    #create dictionary to save some DB values
    dict = {}
    urlData = "https://data.nasa.gov/resource/mc52-syum.json"
    jsonData = getResponse(urlData)
    #read all the json object and save the "year vs energy" values in a dictionary
    for row in jsonData:
        dateTimePeakBrightness = row['date_time_peak_brightness_ut']
        year = parseDateTime(str(dateTimePeakBrightness))
        totalEnergyJ = row['total_radiated_energy_j']
        if year in dict.keys():
            dict[year].append(totalEnergyJ)
        else:
            values = []
            dict[year] = values
            dict[year].append(totalEnergyJ)
    #energy average per year in a new dictionary
    dict2={}
    for k,v in dict.items():
        vint=[]
        mean=0        
        for i in v :
            #e-12
            vint+=[int(i)/1000000000000]       
        mean=statistics.mean(vint)       
        if k in dict2.keys():
            dict2[k].append(mean)
        else:
            values = []
            dict2[k] = values
            dict2[k].append(mean)
    #sort per values
    sortedDict2 = OrderedDict(sorted(dict2.items(), key=lambda x: x[1]))
    print('Total Average Radiated Energy Sorted per Year[J]')
    for k2,v2 in sortedDict2.items():
        print('year: ',k2,'values', v2,'e+12')

main()


