import threading
import socket


def TCPServer():
    global globalVar
    diagnostics.debug("In TCP Server");
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.bind(("127.0.0.1", 8084));
    s.listen(60)
    conn, addr = s.accept()
    diagnostics.debug("Connected by {0}", addr)
    while True:
        data = conn.recv(1024)
        diagnostics.debug(data)
        if not data:
            break
        conn.sendall(data)

def update():
    global globalVar
    with lock:
    	var = globalVar
    
    #diagnostics.debug("globalVar = {0}", globalVar);
    diagnostics.watch(midi[2].data.channel); 	# midi channel
    diagnostics.watch(midi[2].data.status);		# eg. NoteON
    diagnostics.watch(midi[2].data.buffer[0]);	# eg. note value
    diagnostics.watch(midi[2].data.buffer[1]);	# eg. velocity
    
    if midi[2].data.channel == 0:
        if midi[2].data.status == MidiStatus.NoteOn:
            # It's either a Note On or a Note Off msg! (NoteOff is NoteOn with velocity 0)
            key = 0
            # Down
            if midi[2].data.buffer[0] == (22+12+12+12) or midi[2].data.buffer[0] == (21+12+12+12):
            	key = Key.DownArrow
            # Up
            if midi[2].data.buffer[0] == (24+12+12+12) or midi[2].data.buffer[0] == (23+12+12+12): 
                key = Key.UpArrow
            # Left
            if midi[2].data.buffer[0] == (26+12+12+12):
                key = Key.LeftArrow
            # Right
            if midi[2].data.buffer[0] == (28+12+12+12):
                key = Key.RightArrow
            # B
            if midi[2].data.buffer[0] == (28+12+12) or midi[2].data.buffer[0] == (30+12+12):
                key = Key.Z
            # A
            if midi[2].data.buffer[0] == (33+12+12+12) or midi[2].data.buffer[0] == (31+12+12+12):
                key = Key.X
            # Y
            if midi[2].data.buffer[0] == (26+12+12+12+12):
                key = Key.A
            # X
            if midi[2].data.buffer[0] == (35+12+12+12) or midi[2].data.buffer[0] == (36+12+12+12)or midi[2].data.buffer[0] == (37+12+12+12):
                key = Key.S
            # L
            if midi[2].data.buffer[0] == (29+12+12+12+12):
                key = Key.Q
            # R
            if midi[2].data.buffer[0] == (30+12+12+12+12):
                key = Key.W
            # Select
            if midi[2].data.buffer[0] == (19+12+12+8):
                key = Key.E
            # Start
            if midi[2].data.buffer[0] == (31+12):
                key = Key.R

            # if we got a key we're interested in, process it
            if key != 0:
                if midi[2].data.buffer[1] != 0:
                	diagnostics.debug("NoteOn: {0}, {1}, Key: {2}", midi[2].data.buffer[0], midi[2].data.buffer[1], key)
                	keyboard.setKeyDown(key)
                else:  # Key Off
                    diagnostics.debug("NoteOff")
                    keyboard.setKeyUp(key)


if starting:
    midi[2].update += update
    # Middle C = 60
    # lowest C = 24
    diagnostics.debug("Starting file");
    globalVar = 0
    lock = threading.Lock()
    t1 = threading.Thread(target=TCPServer,args=());
    t1.start(); 
  