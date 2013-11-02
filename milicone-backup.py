import subprocess, glob, time, csv, random
import OSC

'''
this programme is made to communicate values from a csv file (written by airodump-ng network scan) via OSC protocol. 
it uses the pyOSC module developed at V2_Lab https://trac.v2.nl/wiki/pyOSC‎ 
'''

### the scanning part -----------------

# airodump-ng is running and logging the results into a csv file
# with the following command: sudo airodump-ng -o csv -w manuf mon0
# subprocess looks for the last edited csv file in current folder
# this file is parsed by the csv module to find the number of data packets that have passed through the network since the last check 

#find the most recently written file
csvs=subprocess.Popen("ls -t1 *csv | head -1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
csv_last=csvs.communicate()[0].strip()


def lookup(dump, keyz):
    key_results=[]
    scan=open(dump, "rU")
    next(scan)
    scanDict=csv.DictReader((line.replace('\0','') for line in scan), delimiter=',')
    for adict in scanDict:
        for k in range(len(keyz)):
            try:
                key_results.append(adict.get(keyz[k]))
            except:
                pass
    return key_results


# values to lookup
key_list=['BSSID', ' Power', ' # IV', ' # beacons']
limiter=len(key_list)

lista=lookup(csv_last, key_list)
bssids=lista[::limiter]
power=lista[1::limiter]
packets=lista[2::limiter]
beacons=lista[3::limiter]


###### and now, the OSC!
""" sending OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
"""

# initiate the client 
client=OSC.OSCClient()
client.connect( ('127.0.0.1', 50000) )

# initiate the message(s)
conv=OSC.OSCMessage()
conv.setAddress("/conversation")
conv.append(0)
# pair conversation with beacon frames

#sms=OSC.OSCMessage()
#sms.setAddress("/sms")

data=OSC.OSCMessage()
data.setAddress("/data")
data.append(0)
# pair data with number of packets

signal=OSC.OSCMessage()
signal.setAddress("/signal")
signal.append(0)
# pair signal strength with power values

#cellco=OSC.OSCMessage()
#cellco.setAddress("/cellcoordinates")

celldist=OSC.OSCMessage()
celldist.setAddress("/celldistance")
celldist.append(0)
# pair celldistance with BSSID >> find a quick way to calculate this!!!!

# bundle : few messages sent together
# use them to send many different messages on every loop for instance in a game. saves CPU and it is faster
bundle = OSC.OSCBundle()
bundle.append(conv) # append prev msgs
bundle.append(data)
bundle.append(signal)
bundle.append(celldist)

### the main loop ----------------------

print 'starting !!!!!!!!!!!'
print bundle

# how many and/or which networks
net=4
which=2
current=[0, 0, 0, 0]
new=[0, 0, 0, 0]

while True:     
    # take the first values of the 'lista' list and send them on via OSC
    for i in range(net+1):
        if i==which:
            # first, reset the bundle
            del bundle[:4]
            # then calculate the difference
            new[0] = float(beacons[i])
            # update only if there is an increase; otherwise keep the old value
            if new[0]>current[0]:
                conv[0]=new[0]-current[0]
            else:
                conv[0]=current[0]
            bundle.append(conv)
            new[1] = float(packets[i])
            if new[1]>current[1]:
                data[0]=new[1]-current[1]
            else:
                data[0]=current[1]
            bundle.append(data)
            new[2] = float(power[i])
            if new[2]>current[2]:
                signal[0]=new[2]-current[2]
            else:
                signal[0]=current[2]
            bundle.append(signal)
            celldist[0]=6
            bundle.append(celldist)
            print bundle
            client.send(bundle) # send it!
            #flush the current list
            current=new
            time.sleep(5)

