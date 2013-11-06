
""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""


import OSC
import time, threading, codecs

f_out=codecs.open("log"+str(int(time.time()))+".txt", "w", encoding="utf-8") 

f_out.write('ID; address; value; timestamp;\n')


# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = '0.0.0.0', 50000


# OSC Server. there are three different types of server. 
s = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking



# this registers a 'default' handler (for unmatched messages), 
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()



# define a message-handler function for the server to call.
def all_handler(addr, tags, stuff, source):
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    f_out.write(OSC.getUrlStr(source)+'; ')
    print "with addr : %s" % addr
    f_out.write(addr+'; ')
    print "typetags %s" % tags
    print "data %s" % stuff
    for smth in stuff:
        print smth
        f_out.write(str(smth))
        f_out.write('; ')
    f_out.write(str(time.time())+'; ')
    f_out.write('\n')

    
s.addMsgHandler("/conversation", all_handler) # adding our function
s.addMsgHandler("/data", all_handler) 
s.addMsgHandler("/sms", all_handler) 
s.addMsgHandler("/signal", all_handler) 
s.addMsgHandler("/celldistance", all_handler) 

# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr


# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()


try :
    while 1 :
        time.sleep(5)

except KeyboardInterrupt :
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
    f_out.close()
        
