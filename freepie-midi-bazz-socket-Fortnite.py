import threading
import socket

def TCPServer():
    global ignoreInput, s, conn
    diagnostics.debug("In TCP Server");
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 8097));
    s.listen(1)
    while True:
        conn, addr = s.accept()
        diagnostics.debug("Connected by {0}", addr)
        while True:
            data = conn.recv(1024)
            diagnostics.debug(data)
            
            if data == "ignoreInputFalse":
                ignoreInput = False
            elif data == "ignoreInputTrue":
                ignoreInput = True
            diagnostics.debug("[THREAD] ignoreInput = {0}", ignoreInput);
            
            if not data:
                diagnostics.debug("Closing connection")
                conn.shutdown(socket.SHUT_RDWR);
                conn.close()
                conn = None
                break
            conn.sendall(data)

def update():
    global ignoreInput
    global deltaX, deltaY
    #diagnostics.debug("[UPDATE] ignoreInput = {0}", ignoreInput);
    noteOn = midi[2].data.buffer[1] != 0
    
    #diagnostics.debug("globalVar = {0}", globalVar);
    #diagnostics.watch(midi[2].data.channel);    # midi channel
    #diagnostics.watch(midi[2].data.status);     # eg. NoteON
    #diagnostics.watch(midi[2].data.buffer[0]);  # eg. note value
    #diagnostics.watch(midi[2].data.buffer[1]);  # eg. velocity
    
    if ignoreInput != True and midi[2].data.channel == 0:
        #diagnostics.debug("MIDI: {0}, {1}, {2}", midi[2].data.status, format(midi[2].data.buffer[0], 'x'), format(midi[2].data.buffer[1], 'x'))
        if midi[2].data.status == MidiStatus.NoteOn:
            # It's either a Note On or a Note Off msg! (NoteOff is NoteOn with velocity 0)
            key = 0
            mymouse = 0 # 1 = left button, 2 = middle, 3 = right, 4 = Wheel Down
            midiNote = midi[2].data.buffer[0]

            # Down
            # 57 is A string 12th fret
            if midiNote == (57) or midiNote == (58):
                key = Key.S # Down
            # Up
            if midiNote == (59): 
                key = Key.W
            # Left
            # 62 is D string 12th fret
            if midiNote == (62):
                key = Key.A
            # Right
            if midiNote == (64):
                key = Key.D

            # E to Open Doors
            if midiNote == 40: #E string open
                key = Key.E
            # R to RELOAD
            if midiNote == 54: #E string 14th fret
                key = Key.R
                
            # Shift To Run TODO
            if midiNote == 52: # E string 12th fret
                key = Key.LeftShift

            # Ctrl to Duck TODO
            if midiNote == 70: # b string 11th fret
                key = Key.LeftControl

            # Spacebar to Jump TODO
            if midiNote == (67) or midiNote == (69):
                key = Key.Space

            # Number keys 1-5 for Weapon Slots Selection
            if midiNote == 44:
                key = Key.F # Pickaxe Toggle
            if midiNote == 45: # E string 5th fret
                key = Key.D1
            if midiNote == 45+1:
                key = Key.D2
            if midiNote == 45+2:
                key = Key.D3
            if midiNote == 45+3:
                key = Key.D4
            if midiNote == 45+4:
                key = Key.D5



            ###### MOUSE STUFF
            ## Clicks
            # Left Click
            if midiNote == (71) or midiNote == (72)or midiNote == (73): #b string 12-14 fret
                mymouse = 1
            # Middle Click
            #if midiNote == (83):
            #    mymouse = 2
            # Right Click
            if midiNote == 78 or midiNote == 79: #e string 14-15th fret
                mymouse = 3
            # # Wheel Down TODO
            if midiNote == 83: #e string 19th fret
                mymouse = 4

            ## Mouse Position High Sensitivity followed by Low Sensitivity
            ### X AXIS high sense
            if midiNote == 50: #D string 10th fret
                if noteOn:
                    deltaX = -5
                    diagnostics.debug("MOUSE NOTE ON")
                else:
                    deltaX = 0
                    diagnostics.debug("MOUSE NOTE OFF")
                #diagnostics.debug("Mouse DeltaX adjusted")
            elif midiNote == 51:
                if noteOn:
                    deltaX = 5
                else:
                    deltaX = 0
                #diagnostics.debug("Mouse DeltaX adjusted")
            ### X axis low sense
            if midiNote == 55: #D string 10th fret
                if noteOn:
                    deltaX = -1
                    diagnostics.debug("MOUSE NOTE ON")
                else:
                    deltaX = 0
                    diagnostics.debug("MOUSE NOTE OFF")
                #diagnostics.debug("Mouse DeltaX adjusted")
            elif midiNote == 56:
                if noteOn:
                    deltaX = 1
                else:
                    deltaX = 0
                #diagnostics.debug("Mouse DeltaX adjusted")
            ### Y AXIS High Sense
            if midiNote == 60: # G string 10th fret
                if noteOn:
                    deltaY = 5
                else:
                    deltaY = 0
                #diagnostics.debug("Mouse DeltaY adjusted")
            elif midiNote == 61:
                if noteOn:
                    deltaY = -5
                else:
                    deltaY = 0
                #diagnostics.debug("Mouse DeltaY adjusted")
            ### Y AXIS Low Sense
            elif midiNote == 65: # G string 10th fret
                if noteOn:
                    deltaY = 1
                else:
                    deltaY = 0
                #diagnostics.debug("Mouse DeltaY adjusted")
            elif midiNote == 66:
                if noteOn:
                    deltaY = -1
                else:
                    deltaY = 0
                #diagnostics.debug("Mouse DeltaY adjusted")

            
            



            # # B
            # if midiNote == (28+12+12) or midiNote == (30+12+12):
            #     key = Key.Z
            
            # # Y
            # if midiNote == (26+12+12+12+12):
            #     key = Key.A
            
            # # L
            # if midiNote == (29+12+12+12+12):
            #     key = Key.Q
            # # R
            # if midiNote == (30+12+12+12+12):
            #     key = Key.W
            # # Select
            # if midiNote == (19+12+12+8):
            #     key = Key.E
            # # Start
            # if midiNote == (31+12):
            #     key = Key.R

            # if we got a key we're interested in, process it
            if key != 0:
                if midi[2].data.buffer[1] != 0:
                    diagnostics.debug("NoteOn: {0}, {1}, Key: {2}", midi[2].data.buffer[0], midi[2].data.buffer[1], key)
                    #if key != Key.E:
                    keyboard.setKeyDown(key)
                else:  # Key Off
                    diagnostics.debug("NoteOff")
                    keyboard.setKeyUp(key)

            # if we got a mouse click we're interested in, process it
            if mymouse != 0:
                if midi[2].data.buffer[1] != 0:
                    diagnostics.debug("Mouse NoteOn: {0}, {1}, Mouse: {2}", midi[2].data.buffer[0], midi[2].data.buffer[1], mymouse)
                    if mymouse == 1:
                        mouse.leftButton = True
                    elif mymouse == 2:
                        mouse.middleButton = True
                    elif mymouse == 3:
                        mouse.rightButton = True
                    elif mymouse == 4:
                        mouse.middleButton = True
                        mouse.wheelDown = True
                else:
                    diagnostics.debug("Mouse NoteOff")
                    if mymouse == 1:
                        mouse.leftButton = False
                    elif mymouse == 2:
                        mouse.middleButton = False
                    elif mymouse == 3:
                        mouse.rightButton = False
                    elif mymouse == 4:
                        mouse.middleButton = False
                        mouse.wheelUp = True


if starting:
    #system.setThreadTiming(TimingTypes.HighresSystemTimer)
    #system.threadExecutionInterval = 1
    global ignoreInput, s, conn, t1
    global deltaX, deltaY
    conn = None;
    s = None;
    ignoreInput = False

    deltaX = 0
    deltaY = 0

    midi[2].update += update
    # Middle C = 60
    # lowest C = 24
    diagnostics.debug("Starting file");
    lock = threading.Lock()
    t1 = threading.Thread(target=TCPServer,args=());
    t1.daemon = True
    t1.start();
    
if stopping:
    global conn, s, t1
    diagnostics.debug("STOPPING")
    if conn != None:
        conn.shutdown(socket.SHUT_RDWR);
        conn.close();
    #s.shutdown(socket.SHUT_RDWR);
    s.close();

mouse.deltaX = deltaX
mouse.deltaY = deltaY
#diagnostics.debug("BEEP")