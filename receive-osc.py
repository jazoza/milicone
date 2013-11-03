
""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""


import OSC
import time, threading



# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = '0.0.0.0', 50000


# OSC Server. there are three different types of server. 
serv = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking



# this registers a 'default' handler (for unmatched messages),
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
serv.addDefaultHandlers()


'''
# define a message-handler function for the server to call.
def printing_handler(addr, tags, stuff, source):
    print "---"
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"

'''
def conversation_handler(addr, tags, stuff, source):
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff

def data_handler(addr, tags, stuff, source):
    print "received new osc msg with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff



#serv.addMsgHandler("/print", printing_handler) # adding our function


# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in serv.getOSCAddressSpace():
    print addr


# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = serv.serve_forever )
st.start()

try :
    while 1 :
        serv.addMsgHandler("/conversation", conversation_handler)
        serv.addMsgHandler("/data", conversation_handler)
        time.sleep(5)

except KeyboardInterrupt :
    print "\nClosing OSCServer."
    serv.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
        
