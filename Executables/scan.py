#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import time
import os
import sys
import subprocess
import datetime
# Add btle.py path for import
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bluepy')))
import btle

if os.getenv('C','1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'

def dump_services(dev):
    services = sorted(dev.getServices(), key=lambda s: s.hndStart)
    for s in services:
        print ("\t%04x: %s" % (s.hndStart, s))
        if s.hndStart == s.hndEnd:
            continue
        chars = s.getCharacteristics()
        for i, c in enumerate(chars):
            props = c.propertiesToString()
            h = c.getHandle()
            if 'READ' in props:
                val = c.read()
                if c.uuid == btle.AssignedNumbers.device_name:
                    string = ANSI_CYAN + '\'' + val.decode('utf-8') + '\'' + ANSI_OFF
                elif c.uuid == btle.AssignedNumbers.device_information:
                    string = repr(val)
                else:
                    string = '<s' + binascii.b2a_hex(val).decode('utf-8') + '>'
            else:
                string=''
            print ("\t%04x:    %-59s %-12s %s" % (h, c, props, string))

            while True:
                h += 1
                if h > s.hndEnd or (i < len(chars) -1 and h >= chars[i+1].getHandle() - 1):
                    break
                try:
                    val = dev.readCharacteristic(h)
                    print ("\t%04x:     <%s>" % (h, binascii.b2a_hex(val).decode('utf-8')))
                except btle.BTLEException:
                    break

class ScanPrint(btle.DefaultDelegate):
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            status = "new"
        elif isNewData:
            if arg.new: return
            status = "update"
        else:
            if not arg.all: return
            status = "old"

        if dev.rssi < arg.sensitivity:
            return
	
	time = datetime.datetime.now().time()     

        if ( directory.has_key(dev.addr) ):
		[a, b, c] = dev.getScanData()[1]

		if ( not directory[dev.addr][0] and directory[dev.addr][1] < dev.rssi ):	#newly detected and entered
	       		#print ('    Device mac (%s), %d dBm entering' % ( dev.addr, dev.rssi) )
			directory[dev.addr][0] = True
			beacon = subprocess.Popen(["perl", "out.pl", "-mac=" + dev.addr, "-rssi=" + str(dev.rssi), "-time=" + str(time), "-stand=entry "  "&"], stdout=subprocess.PIPE)

		elif( directory[dev.addr][0] and directory[dev.addr][1] > dev.rssi and directory[dev.addr][2] < dev.rssi):
			#print ('    Device mac (%s), %d dBm leaving' % ( dev.addr, dev.rssi) )
			directory[dev.addr][0] = False
			beacon = subprocess.Popen(["perl", "out.pl", "-mac=" + dev.addr, "-rssi=" + str(dev.rssi), "-time=" + str(time), "-stand=exit "  "&"], stdout=subprocess.PIPE)
			output = beacon.communicate()[0]
			print ('%s', output )
        print


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument('host', action='store',
    #                    help='BD address of BT device')
    parser.add_argument('-t', '--timeout', action='store', type=int, default=4,
                        help='Scan delay, 0 for continuous')
    parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128,
                        help='dBm value for filtering far devices')
    parser.add_argument('-d', '--discover', action='store_true',
                        help='Connect and discover service to scanned devices')
    parser.add_argument('-a','--all', action='store_true',
                        help='Display duplicate adv responses, by default show new + updated')
    parser.add_argument('-n','--new', action='store_true',
                        help='Display only new adv responses, by default show new + updated')
    parser.add_argument('-v','--verbose', action='store_true',
                        help='Increase output verbosity')
    arg = parser.parse_args(sys.argv[1:])

    btle.Debugging = arg.verbose

    scanner = btle.Scanner().withDelegate(ScanPrint())

    directory = { '80:ea:ca:00:42:2a':[False, -70, -78], '80:ea:ca:00:42:27':[False, -70, -78], '80:ea:ca:00:41:f9':[False, -70, -78], '80:ea:ca:00:42:07':[False, -70, -78], '80:ea:ca:00:41:fa':[False, -70, -78], '80:ea:ca:00:42:28':[False, -70, -78], '80:ea:ca:00:41:fe':[False, -70, -78], '80:ea:ca:00:42:08':[False, -70, -78], '80:ea:ca:00:42:29':[False, -70, -78], '80:ea:ca:00:42:26':[False, -70, -78] }


    print (ANSI_RED + "Scanning for devices..." + ANSI_OFF)
    var = 1
    while var==1:
        devices = scanner.scan(5)
