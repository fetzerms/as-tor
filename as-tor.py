#!/usr/bin/env python

import json
import urllib2
import sys

# Url to Oninoo status protocol,
# See https://onionoo.torproject.org/
onionooUrl = 'https://onionoo.thecthulhu.com/details'

if len(sys.argv) < 2:
    print "Usage: ", sys.argv[0], " <AS-Number>"
    sys.exit(0)

asNumber = sys.argv[1]

# If AS-Number is only passed as a number.
if not asNumber.lower().startswith("as"):
    asNumber = "AS" + asNumber

# Get relay list.
response = urllib2.urlopen(onionooUrl)
raw_relays = response.read()

relays_list = json.loads(raw_relays)

template = "|{0:^20}|{1:^15}|{2:^25}|"
print '+--------------------+---------------+-------------------------+'
print template.format("Address", "Is Exit", "Nickname", "Contact information")
print '+--------------------+---------------+-------------------------+'

# relay counter
numRelays = 0

for relay in relays_list['relays']:

    # We only care about running relays and ones that have an as_number
    if relay['running'] == True and 'as_number' in relay:

        # is this relay running inside the passed AS?
        if relay['as_number'].lower() == asNumber.lower():

            nickname =  relay['nickname']

            # Check if this relay is an exit relay.
            if 'Exit' in relay['flags']:
                exit = 'Exit node'
            else:
                exit = 'Relay node'

            #
            # As some contact information can be quite long, it breaks the output.
            # This is left in the code for reference.
            #
            #if 'contact' in relay:
            #    contact = relay['contact']
            #else:
            #    contact = "No contact information"

            if 'or_addresses' in relay:
                ip = relay['or_addresses'][0].split(':')[0]
            else:
                ip = 'unknown'

            print template.format(ip, exit, nickname)
            numRelays = numRelays + 1

print '+--------------------+---------------+-------------------------+'
template = "|{0:^36}|{1:^25}|"
print template.format("Total number of relays in this AS:", numRelays)
print '+--------------------+---------------+-------------------------+'