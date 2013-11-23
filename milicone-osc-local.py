import subprocess, glob, time, csv, re, codecs, OSC

'''
this programme broadcasts and logs values from a csv file written by airodump-ng network scan. 
it sends the values over localhost:49999 port and at the same time writes the values to a logxxxx.csv file
'''

print 'why not work'

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

bssids, power, packets, beacons, essids=reading_values(csv_last, key_list)

###### the writing part
f_out=codecs.open("logs/log"+str(int(time.time()))+".csv", "w", encoding="utf-8") 
f_out.write('ID; address; value; timestamp;\n')

def logging(addr, value):
    f_out.write('localhost; ')
    f_out.write(str(addr)+'; ')
    f_out.write(str(value)+'; ')
    f_out.write(str(time.time())+'; \n')	


### OSC
send_address = '127.0.0.1', 49999
c = OSC.OSCClient()
c.connect( send_address ) 

conv = OSC.OSCMessage()
conv.setAddress("/conversation")
conv.append('0')

data = OSC.OSCMessage()
data.setAddress("/data")
data.append(0)

signal = OSC.OSCMessage()
signal.setAddress("/signal")
signal.append(0)

#sms = OSC.OSCMessage()

bundle = OSC.OSCBundle()



### the main loop ----------------------

print 'starting !!!!!!!!!!!'

# lists of values to print
current=[0.0, 0.0, 0.0, 0.0, 0.0]
new=[0.0, 0.0, 0.0, 0.0, 0.0]

which=raw_input('BSSID: ')
#which='00:0F:CB:C2:51:46'


while True:  
 
    # iterate through the list of lists 
    for i in range(len(bssids)):
        # match a bssid
        if bssids[i].strip()==which.strip():
            print 'found'
            #reset bundle
            bundle=[]
            ###conversation values (new[0] or current[0])
            # !!! update only if there is an increase; otherwise keep the old value
            new[0] = float(beacons[i])
            if new[0]>current[0]:
                conversation=new[0]-current[0]
            else:
                conversation=current[0]
            conv[0]=conversation
            logging('/conversation', conversation)
            ###data values (new[1] or current[1])
            new[1] = float(packets[i])
            if new[1]>current[1]:
                datas=new[1]-current[1]
            else:
                datas=current[1]
            data[0]=datas
            logging('/data', datas)
            ###signal alues (new[2] or current [2])
            new[2] = abs(float(power[i]))
            if new[2]>current[2]:
                signalz=new[2]-current[2]
            else:
                signalz=current[2]
            signal[0]=signalz
            logging('/signal', signalz)
            celldistance=0.5
            logging('/celldistance', celldistance)
            bundle.append(conv)
            bundle.append(data)
            bundle.append(signal)
            #bundle.append(sms)
            c.send(conv)
            c.send(data)
            c.send(signal)
            current=new
            bssids, power, packets, beacons, essids=reading_values(csv_last, key_list)
            time.sleep(3)
