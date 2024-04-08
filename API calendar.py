#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# """
# Created on Sun Jun 19 16:19:24 2022

# @author: robertbass
# """


#this script interfaces with google's API to update my personal calendar.

#for my research project, i worked with mice, and i needed to give these mice a drug called tamoxifen at a specific age.
# i also needed to euthanize these animals on specific days.
#for example, i would need to give an animal tamoxifen at 5 weeks of age (35 days) for a period of 8 days. i also needed to euthanize the animals at various time points
# such as 3, 6, or 9 months. manually counting 252 days (9 months) into the future is tedious and annoying. so, i wrote this script that connects to my google calendar 
#via google's API. running this program from the command line, i can input a mouse's birth date, and it will tell me the specific day
#35 days in the future (5 weeks) and also 3, 6, or 9 months in the future. it will then create calendar events on those specific days in my google calendar.



#notes: 
    
#try running this file from the terminal. that means making its parent file
#the working directory and running it
#cd /Users/robertbass/Documents/Xu\ Lab/Programming/Python/
#python API\ calendar.py
#the backslashes allow you to use spaces in the file name
    
# if the token expires, go to the main directory robertbass and delete
#the token and credentials files. keep the  quickstart file.
#then, go onto the API console, setup a new OAuth 2.0 Client ID credential
#download the JSON file associated with that credential
#name it "credentials" and place it in robertbass
#then, go to the terminal and run quickstart.py
#running this will create the token.json file in robertbass
# and it will open up the log in
#screen in firefox. so then you log in and you are verified with the new 
#credential

# from _future_ import print_function
from googleapiclient.discovery import build
# !pip install --upgrade google-api-python-client
# !pip install --upgrade googleapiclient
# !pip install --upgrade googleapis
# !pip install apiclient
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
    
SCOPES = "https://www.googleapis.com/auth/calendar"
store = file.Storage("storage.json")
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets("client_secrets.json", SCOPES)
    creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)
    
CAL = build("calendar", "v3", http=creds.authorize(Http()))


#litter title and mouse birthday
def get_dates():
    x = input("Enter Mouse Birthday: yyyy mm dd:")
    if (len(x) < 8):
        return
    else:
        x = x.split()
        mousebirth = datetime.date(int(x[0]), int(x[1]), int(x[2]))
    global toes
    global wean
    global tamoxifen
    global breed
    global threemonth
    global days107
    global fourmonth
    global fivemonth
    global days157
    global sixmonth
    global ninemonth
    toes = [str([mousebirth + datetime.timedelta(7)]), "toes"]
    wean = [str([mousebirth + datetime.timedelta(3*7)]), "wean"]
    tamoxifen = [str([mousebirth + datetime.timedelta(5*7)]), "Tamoxifen",
              str([mousebirth + datetime.timedelta(5*7+12)])]
    breed = [str([mousebirth + datetime.timedelta(7*7)]), "breed"]
    threemonth = [str([mousebirth + datetime.timedelta(12*7)]), "3 months"]
    days107 = [str([mousebirth + datetime.timedelta(107)]), "107"]
    fourmonth = [str([mousebirth + datetime.timedelta(16*7)]), "4 months"]
    fivemonth = [str([mousebirth + datetime.timedelta(20*7)]), "5 months"]
    days157 = [str([mousebirth + datetime.timedelta(157)]), "157"]
    sixmonth = [str([mousebirth + datetime.timedelta(24*7)]), "6 months"]
    ninemonth = [str([mousebirth + datetime.timedelta(36*7)]), "9 months"]
    #dates you want on the calendar
    dates = [toes, wean, tamoxifen, breed, threemonth, days107, fourmonth,\
             fivemonth, days157, sixmonth, ninemonth]
    dates = format_dates_visual(dates)
    inquire()
    
def format_dates_visual(dates):    
    EVENTS = []
    for date in dates: 
        #formatting
        date[0] = date[0][15:-2]
        date[0] = date[0].replace(", ", "-")
        if date[1] == "Tamoxifen":
            date[2] = date[2][15:-2]
            date[2] = date[2].replace(", ", "-")
        print(date)
        EVENTS.append(date)
    return EVENTS
        
def format_dates_calendar(dates, LitterTitle):    
    EVENTS = []
    for date in dates: 
        if date[1] == "Tamoxifen":
            EVENT = {
            "summary": LitterTitle + " " + str(date[1]),
            "start": {"date": str(date[0]),
                      "timeZone": "America/New_York",
              },
            "end":   {"date": str(date[2]),
                      "timeZone": "America/New_York",
              },
            }
            # print(date[2])
        else: 
            EVENT = {
            "summary": LitterTitle + " " + str(date[1]),
            "start": {"date": str(date[0]),
                      "timeZone": "America/New_York",
              },
            "end":   {"date": str(date[0]),
                      "timeZone": "America/New_York",
              },
            }
        EVENTS.append(EVENT)
    return EVENTS

def inquire():        
    question = input("Create calendar events? y or n:")   
    if question == "y":
            eventresponse = input("which events? list month numbers, no commas.\
                                      say n to quit:")
            if eventresponse == "n":
                return
            else: 
                eventresponse = eventresponse.split()
                count = 0
                for event in eventresponse:
                    if event == "toes":
                        eventresponse[count] = toes
                    elif event == "wean":
                        eventresponse[count] = wean
                    elif event == "tamoxifen":
                        eventresponse[count] = tamoxifen
                        # print(event)
                    elif event == "breed":
                        eventresponse[count] = breed
                    elif event == "3":
                        eventresponse[count] = threemonth
                    elif event == "107":
                        eventresponse[count] = days157
                    elif event == "4":
                        eventresponse[count] = fourmonth
                    elif event == "5":
                        eventresponse[count] = fivemonth
                    elif event == "157":
                        eventresponse[count] = days157 
                    elif event == "6":
                        eventresponse[count] = sixmonth
                    elif event == "9":
                        eventresponse[count] = ninemonth
                    else:
                        print("you typed something wrong")
                        return
                    count += 1
                title = input("Title of Mouse group?:")
                formatted_events = format_dates_calendar(eventresponse, title)
                create_event(formatted_events)
    else:
            return
        
        
    
def create_event(EVENTS):        
    for event in EVENTS: 
        e = CAL.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (e.get('htmlLink')))

get_dates()
    # LitterTitle = "Gen 6" + " "
# mousebirth = datetime.date(2022, 1, 16)



# GMT_OFF = "-0:04"
# {"dateTime": "2022-06-22T14:00:00%s" % GMT_OFF}
# TIMEZONE =  "America/New_York"
   # "end":   {"date": "2022-06-22T16:00:00",
   # "start": {"date": "2022-06-22",

   