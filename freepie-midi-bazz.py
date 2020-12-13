def update():
    diagnostics.watch(midi[0].data.channel); # midi channel
    diagnostics.watch(midi[0].data.status);		# eg. NoteON
    diagnostics.watch(midi[0].data.buffer[0]);	# eg. note value
    diagnostics.watch(midi[0].data.buffer[1]);	# eg. velocity
    
    if midi[0].data.channel == 0:
        if midi[0].data.status == MidiStatus.NoteOn:
            # It's either a Note On or a Note Off msg! (NoteOff is NoteOn with velocity 0)
            key = 0
            # Down
            if midi[0].data.buffer[0] == 24: # C-1
                key = Key.DownArrow
            # Up
            if midi[0].data.buffer[0] == 31: 
                key = Key.UpArrow # G-1
            # Left
            if midi[0].data.buffer[0] == 26:
                key = Key.LeftArrow # D-1
            # Right
            if midi[0].data.buffer[0] == 28:
                key = Key.RightArrow # E-1

            # B
            if midi[0].data.buffer[0] == (24+12):
                key = Key.Z # C-2
            # A
            if midi[0].data.buffer[0] == (26+12):
                key = Key.X # D-2
            # Y
            if midi[0].data.buffer[0] == (25+12):
                key = Key.A # C#2
            # X
            if midi[0].data.buffer[0] == (27+12):
                key = Key.S # D#2
            # L
            if midi[0].data.buffer[0] == (28+12):
                key = Key.Q # E-2
            # R
            if midi[0].data.buffer[0] == (29+12):
                key = Key.W # F-2
            # Select
            if midi[0].data.buffer[0] == 21:
                key = Key.E # A-0
            # Start
            if midi[0].data.buffer[0] == 23:
                key = Key.R # B-0

            # if we got a key we're interested in, process it
            if key != 0:
                if midi[0].data.buffer[1] != 0:
                	diagnostics.debug("NoteOn: {0}, {1}", midi[0].data.buffer[0], midi[0].data.buffer[1])
                	keyboard.setKeyDown(key)
                else:  # Key Off
                    diagnostics.debug("NoteOff")
                    keyboard.setKeyUp(key)


if starting:
    midi[0].update += update
    # Middle C = 60
    # lowest C = 24
  