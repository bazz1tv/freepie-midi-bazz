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
            if midi[0].data.buffer[0] == 24: # C
                key = Key.DownArrow
            # Up
            if midi[0].data.buffer[0] == 31: 
                key = Key.UpArrow # G
            # Left
            if midi[0].data.buffer[0] == 26:
                key = Key.LeftArrow # D
            # Right
            if midi[0].data.buffer[0] == 28:
                key = Key.RightArrow # E

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
  