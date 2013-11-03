milicone
========
| connect or not | 
=======

a project for investigating interaction with wireless communication traffic

The traffic is captured with an Android app^ and passed on to a Puredata patch which controls a DMX light. The app documentation^. The app is basically a modified traffic monitor based on Netcounter written by Cyril Jaquier (http://www.jaqpot.net/netcounter/). It was developed within the SINLAB research lab by Louis David Jean Magarshack in collaboration with Selena Savic. As an alternative to the app, a Python script analyses data captured by airodump-ng and send this as a stream to Puredata. 

Both Python and Android are using the OSC protocol to communicate with Puredata (the first on localhost, second targetting a specific IP address of the computer that's listening). They send over a bundle of messages with the following address patterns:

/ID
/conversation
/sms
/data
/signal
/celldistance

The messages contain information on total conversation duration (in seconds), number of sms messages (both received and sent), the number of data packets, signal strength (in db) and the distance to the cell the phone is connected to. The ID is based on the current phone's IP address. All these are listed in the phone status, and retreived by the app for the purpose of this experimentation. People who install the app volunteer to share this data with the system, anonymously.

The different information on the traffic are coupled with DMX channels of an RGB LED light (Fusion color 18 FC RGBW). The light is set to an 8-channel mode (1-red; 2-green; 3-blue; 4-white; 5-stroboscope; 6-rainbow effect?; 7-master dimmer; 8-colour temperature). 

using the pyOSC module developed at V2_lab, Rotterdam (https://trac.v2.nl/wiki/pyOSC)



