#!/usr/bin/env python

import logging
import argparse
import requests
import json
from datetime import datetime

LOG = logging.getLogger('meetup')

class Meetup(object):
    """
    Get information from meetup web site and
    provide json and cli output
    """

    def __init__(self, address):
        self._address = address

    def get_next_event(self):
        "Print next meetup"

        # Get content from address
        try:
            con = requests.get(self._address)
            res_json = json.loads(con.content)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.MissingSchema) as e:
            LOG.debug('Fail to get content from %s : %s' % (self._address, e))
            return False
        except ValueError as e:
            LOG.debug('Fail to read content from %s : %s' % (self._address, e))
            return False

        res = res_json.get('results', [])

        if not res:
            print 'No Meetup'
            return False

        name = res[0]['name']
        description = res[0]['description']
        timestamp = int(res[0]['time']/1000)
        date = datetime.fromtimestamp(timestamp).strftime('%A %d %B at %H:%M')
        location_name = res[0]['venue']['name']
        location_addr = res[0]['venue']['address_1']
        location_city = res[0]['venue']['city']

        print 'Next Meetup'
        print 'Name: %s' % name
        print 'Description: %s' % description
        print 'Date: %s' % date
        print 'Location: %s - %s - %s' % (location_name,
                                              location_addr, location_city)


if __name__ == '__main__':
    # Set args
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-d", "--debug",
            help="Set logger in debug mode",
            action='store_true')
    PARSER.add_argument("-a", "--address",
            help="Set meetup api address",
            required=True)
    ARGS = PARSER.parse_args()

    if ARGS.debug:
        LOG.setLevel(logging.DEBUG)

    # Set LOG handler
    hdl = logging.StreamHandler(); LOG.addHandler(hdl)

    # Launch app
    app = Meetup(address=ARGS.address)
    app.get_next_event()

