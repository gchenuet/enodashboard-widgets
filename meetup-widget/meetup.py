#!/usr/bin/env python


import requests
import json
import time
import datetime

def get_next_event():
        con = requests.get('ADDRESS')
        res_json = json.loads(con.content)

        res = res_json.get('results', [])

        if not res:
                print "No Meetup"
        else:
                print "Next Meetup"
                print "Name: " + res[0]['name']
                print "Description: " + res[0]['description']
                print "Date: " + datetime.datetime.fromtimestamp(int(res[0]['time']/1000)).strftime('%A %d %B at %H:%M')
                print "Location: " + res[0]['venue']['name'] + " - " + res[0]['venue']['address_1'] + " - " + res[0]['venue']['city']


if __name__ == '__main__':
        get_next_event()
