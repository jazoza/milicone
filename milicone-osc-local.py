import subprocess, glob, time, csv, re, codecs, OSC

'''
this programme broadcasts and logs values from a csv file written by airodump-ng network scan. 
it sends the values over localhost:50000 port and at the same time writes the values to a logxxxx.csv file
'''

### the scanning part -----------------

# airodump-ng is running and logging the results into a csv file
# with the following command: sudo airodump-ng -o csv -w manuf mon0
# subprocess looks for the last edited csv file in current folder
# this file is parsed by the csv module to find the number of data packets that have passed through the network since the last check 

#find the most recently written file
csvs=subprocess.Popen("ls -t1 logs/*csv | head -1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
key_list=['BSSID', ' Power', ' # IV', ' # beacons', 'ESSID']
limiter=len(key_list)

def reading_values(a_file, a_key_list):
    a_list=lookup(a_file, a_key_list)
    sublist1=a_list[::limiter]
    sublist2=a_list[1::limiter]
    sublist3=a_list[2::limiter]
    sublist4=a_list[3::limiter]
    sublist5=a_list[4::limiter]
    return sublist1, sublist2, sublist3, sublist4, sublist5

# prepare values for sending:
# power = signal
# packets = data
# beacons = conversation

bssids, power, packets, beacons, essids=reading_values(csv_last, key_list)

###### the writing part
f_out=codecs.open("logs/log"+str(int(time.time()))+"airodump.csv", "w", encoding="utf-8") 
f_out.write('ID; address; value; timestamp;\n')

def logging(addr, value):
    f_out.write('localhost; ')
    f_out.write(str(addr)+'; ')
    f_out.write(str(value)+'; ')
    f_out.write(str(time.time())+'; \n')	


### OSC
send_address = '127.0.0.1', 50000
c = OSC.OSCClient()
c.connect( send_address ) 

conv = OSC.OSCMessage()
conv.setAddress("/conversation")
conv.append(0)

data = OSC.OSCMessage()
data.setAddress("/data")
data.append(0)

signal = OSC.OSCMessage()
signal.setAddress("/signal")
signal.append(0)


new=[0.0, 0.0, 0.0, 0.0]
current=[0.0, 0.0, 0.0, 0.0]

### the main loop ----------------------


which=raw_input('BSSID: ')

for i in range(len(bssids)):
    try:
        if bssids[i].strip()==which.strip():
            #create the 'CURRENT' list to compare values with
            current=[float(beacons[i]), float(packets[i]), abs(float(power[i]))]
    except AttributeError:
        print 'errrrr'
        current=[0.0, 0.0, 0.0]

while True:  
    bssids_new, power_new, packets_new, beacons_new, essids_new=reading_values(csv_last, key_list)
    for i in range(len(bssids)):
        try:
            if bssids[i].strip()==which.strip():
                #create the 'CURRENT' list to compare values with
                current=[float(beacons[i]), float(packets[i]), abs(float(power[i]))]
                print 'found current', i, current, bssids[i]
                for j in range(len(bssids)):
                    if bssids_new[j].strip()==which.strip():
                        #create the 'NEW' list 
                        new=[float(beacons_new[j]), float(packets_new[j]), abs(float(power_new[j]))]
                        print 'found also in new', j, new, bssids_new[j]
                        conv[0]=new[0]-current[0]
                        data[0]=new[1]-current[1]
                        signal[0]=new[2]-current[2]
                        print conv, data, signal
                        #send
                        c.send(conv)
                        c.send(data)
                        c.send(signal)
                        #log
                        logging('/conversation', conv[0])
                        logging('/data', data[0])
                        logging('/signal', signal[0])
                        print '....'
                        time.sleep(10)
                    current=new
        except AttributeError:
            print "error, waiting"
            time.sleep(3)


