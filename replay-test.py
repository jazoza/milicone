import subprocess, glob, time, csv, random
import OSC


# values to lookup
key_list=['BSSID', ' Power', ' # IV', ' # beacons']
limiter=len(key_list)


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
conv.append(17)
# pair conversation with beacon frames

sms=OSC.OSCMessage()
sms.setAddress("/sms")
sms.append(1)

data=OSC.OSCMessage()
data.setAddress("/data")
data.append(180)
# pair data with number of packets

signal=OSC.OSCMessage()
signal.setAddress("/signal")
signal.append(97)
# pair signal strength with power values

#cellco=OSC.OSCMessage()
#cellco.setAddress("/cellcoordinates")

celldist=OSC.OSCMessage()
celldist.setAddress("/celldistance")
celldist.append(9)
# pair celldistance with BSSID >> find a quick way to calculate this!!!!

# bundle : few messages sent together
# use them to send many different messages on every loop for instance in a game. saves CPU and it is faster
bundle = OSC.OSCBundle()
bundle.append(conv) # append prev msgs
bundle.append(sms)
bundle.append(data)
bundle.append(signal)
bundle.append(celldist)

client.send(bundle)

### the main loop ----------------------

print 'starting !!!!!!!!!!!'
print bundle


current=[0, 0, 0, 0]
new=[0, 0, 0, 0]

while True:     
    # take the first values of the 'lista' list and send them on via OSC
    for i in range(100):
        # first, reset the bundle
        del bundle[:5]
        # conversation increaces by 15+i
        conv[0]=15+i
        bundle.append(conv)
        # every thrd time get an sms (+0.34)
        sms[0]=0.3+i/100
        bundle.append(sms)
        #data increased by 96+i
        data[0]=96+i
        bundle.append(data)
        #signal decreases by 0.4++ 
        signal[0]=0.4+i/100
        bundle.append(signal)
        #celldistance grows by a 10th of i each time
        celldist[0]=i/10
        bundle.append(celldist)
        print bundle
        client.send(bundle) # send it!
        #flush the current list
        time.sleep(5)

