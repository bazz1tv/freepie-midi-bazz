def update():
    diagnostics.watch(midi[2].data.channel); # midi channel
    diagnostics.watch(midi[2].data.status);		# eg. NoteON
    diagnostics.watch(midi[2].data.buffer[0]);	# eg. note value
    diagnostics.watch(midi[2].data.buffer[1]);	# eg. velocity
    
    if midi[2].data.channel == 0:
        if midi[2].data.status == MidiStatus.NoteOn:
            # It's either a Note On or a Note Off msg! (NoteOff is NoteOn with velocity 0)
            key = 0
            # Down
            if midi[2].data.buffer[0] == (22+12+12+12): # A-1
                key = Key.DownArrow
            # Up
            if midi[2].data.buffer[0] == (23+12+12+12): 
                key = Key.UpArrow # A#1
            # Left
            if midi[2].data.buffer[0] == (26+12+12+12):
                key = Key.LeftArrow # D-1
            # Right
            if midi[2].data.buffer[0] == (28+12+12+12):
                key = Key.RightArrow # E-1

            # B
            if midi[2].data.buffer[0] == (28+12+12):
                key = Key.Z # E-0
            # A
            if midi[2].data.buffer[0] == (33+12+12+12) or midi[2].data.buffer[0] == (31+12+12+12):
                key = Key.X # E-2
            # Y
            if midi[2].data.buffer[0] == (26+12+12+12+12):
                key = Key.A # D-2
            # X
            if midi[2].data.buffer[0] == (35+12+12+12) or midi[2].data.buffer[0] == (37+12+12+12):
                key = Key.S # G-2
            # L
            if midi[2].data.buffer[0] == (29+12+12+12+12):
                key = Key.Q # G-2
            # R
            if midi[2].data.buffer[0] == (30+12+12+12+12):
                key = Key.W # B-2
            # Select
            if midi[2].data.buffer[0] == (19+12+12):
                key = Key.E # A-0
            # Start
            if midi[2].data.buffer[0] == (23+12+12):
                key = Key.R # B-0

            # if we got a key we're interested in, process it
            if key != 0:
                if midi[2].data.buffer[1] != 0:
                	diagnostics.debug("NoteOn: {0}, {1}", midi[2].data.buffer[0], midi[2].data.buffer[1])
                	keyboard.setKeyDown(key)
                else:  # Key Off
                    diagnostics.debug("NoteOff")
                    keyboard.setKeyUp(key)


if starting:
    midi[2].update += update
    # Middle C = 60
    # lowest C = 24
  