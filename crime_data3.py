#Aliya Merali
#Crime Data - NYPD_Public_Indicators
#Assessment 3 - this program parses the data from the CSV file on socrata and outputs 2 files - first for excel, with crime title, precinct, month, date, count of that crime in that month, and YTD runnign count of that crime in that precinct; second file for GIS with same information but iterated so there is a line of data for each incident recorded, to make GIS mapping easier

import csv
import re
from collections import defaultdict

log = open('NYPD_Public_Indicators.csv','r')
outputFile = open('NYPD_Indicator_Assess_Excel.csv','w')
outputFile_GIS = open('NYPD_Indicator_Assess_GIS.csv','w')
csv_fp = csv.writer(outputFile, delimiter=',', lineterminator='\n')
csv_fp_GIS = csv.writer(outputFile_GIS, delimiter=',', lineterminator='\n')


crime_log_pre = csv.DictReader(log)
#sort the csv input file by year / month value
crime_log = sorted(crime_log_pre, key = lambda d: str(d['Month']))
crime_dict = {}
count_dict = {}

#This only works if input file is sorted by date (as done above), because the event count runs off a count that changes as you iterate through file
csv_fp.writerows([['Crime','Year','Month','Precinct', 'Month Count', 'YTD Value']])
csv_fp_GIS.writerows([['Crime','Year','Month','Precinct', 'Month Count', 'YTD Value']])


for line in crime_log:
    data = line['Sub-Indicator']
    precinct = re.findall(r'\d+',data)
    date = line['Month'].split(' / ')
    crime = line['Indicator Name']
    YTD_count = line['YTD Value']
    if precinct != []:
        if YTD_count != '':
            key = str(precinct[0]) + ' Precinct, Crime:  '+ str(crime)
            if key not in count_dict:
                event_count = int(YTD_count)
            else: 
                event_count = int(YTD_count) - int(count_dict[key])
            count_dict[key] = YTD_count
            csv_fp.writerows([[str(line['Indicator Name']),str(date[0]),str(date[1]),str(precinct[0]), str(event_count), str(YTD_count)]] )
            n = 0
            while n < event_count:
                csv_fp_GIS.writerows([[str(line['Indicator Name']),str(date[0]),str(date[1]),str(precinct[0]), str(event_count), str(YTD_count)]] )
                n = n + 1
                
