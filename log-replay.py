import subprocess, glob, time, csv, re, codecs, OSC


'''
this programme broadcasts OSC logs written by log-osc-traffic.py 
it uses the most recent csv file found in the current folder
it sends the values over localhost:49999 port
'''

csvs=subprocess.Popen("ls -t1 *csv | head -1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
csv_last=csvs.communicate()[0].strip()

'''
def lookup(dump, keyz):
    key_results=[]
    scan=open(dump, "rU")
    scanDict=csv.DictReader((line.replace('\0','') for line in scan), delimiter=';')
    for adict in scanDict:
        if adict.has_key(keyz) and adict.get(keyz)!=None:
            try:
                key_results.append(adict.get(keyz))
            except:
                pass
    return key_results
'''
# values to lookup
key_list=['ID', ' address',' value',' timestamp']
limiter=len(key_list)

scan=open(csv_last, "rU")
scanDict=csv.DictReader((line.replace('\0','') for line in scan), delimiter=';')

### OSC
send_address = '127.0.0.1', 50000
c = OSC.OSCClient()
c.connect( send_address ) 

msg=OSC.OSCMessage()
msg.setAddress('/conversation')
msg.append(0)
timez_start=1385047116.83

for adict in scanDict:
	msg.setAddress(str(adict.get(' address')))
	msg[0]=float(adict.get(' value'))
	timez=float(adict.get(' timestamp'))
	delay=timez-timez_start
	print delay
	c.send(msg)
	timez_start=timez
	time.sleep(delay)
