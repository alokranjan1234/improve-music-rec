# By jasperlouie
# need to have vishnubob's python-midi library installed
# https://github.com/vishnubob/python-midi 
import midi

# =============================================
# Parameters
# =============================================
# CHANGE ME TO CHANGE THE FILE WE ARE STEMMING
midi_fname = "take5.mid"
# =============================================

def decompose_midi(fname, out_dir=None):
	"""takes fname and decomposes its tracks into multiple midi files in out_dir
	grouped by families found here https://www.midi.org/specifications/item/gm-level-1-sound-set""" 
	# load pattern as midi
	pattern = midi.read_midifile(fname)

	# list of names corresponding to following pc ranges
	family_names = ["piano", "chrom_percus", "organ", "guitar", "bass", "strings", "ensemble", "brass", "reed", "pipe", "synth_lead", "synth_pad", "synth_effects", "ethnic", "percussive", "sound_effects", "drums"]
	
	# constant ranges found in spec for instrument family grouping
	family_ranges = [range(0,8), range(8,16), range(16,24), range(24,32), range(32,40), range(40,48), range(48, 56), range(56,64), range(65,72), range(72,80), range(80, 88), range(88, 96), range(96,104), range(104,112), range(112, 120), range(120,128)]

	# create a list of lists to store tracks corresponding to each family
	grouped_tracks = [[] for x in family_ranges]

	for curr_family in range(len(family_ranges)):
		for track in pattern:
			track_done = False
			for event in track:
				# Channel 10 (0 indexed is 9) is only drums
				if "ProgramChangeEvent" in repr(event) and int(event.channel) != 9:
					if int(event.data[0]) in family_ranges[curr_family]:
						grouped_tracks[curr_family].append(track)
						track_done = True
						# print "Adding track titled {} to family {}".format(track[0].text, family_names[curr_family])
			if track_done:
				continue

	# handle drums specially
	drums = []			
	for track in pattern:
		track_done = False	
		for event in track:	
		# Channel 10 (0 indexed is 9) is drums
			if "ProgramChangeEvent" in repr(event):		
				if int(event.channel) == 9 :
					drums.append(track)
					track_done = True
					print "Adding track titled {} to family {}".format(track[0].text, family_names[-1])
	grouped_tracks.append(drums)

	fname_pre = fname.split(".")[0]

	for curr_family in range(len(family_names)):
		if grouped_tracks[curr_family] != []:
			out = midi.Pattern(format=pattern.format, resolution=pattern.resolution, tracks=grouped_tracks[curr_family])
			if out_dir is None:
				midi.write_midifile("{}_{}.mid".format(fname_pre, family_names[curr_family]), out)
			else:
				midi.write_midifile("{}_{}.mid".format(fname_pre, family_names[curr_family]), out)

decompose_midi(midi_fname)

# ============================================================
# In progress. attempt to decompose by channel for midis that 
# are compressed into one track. Not needed if using non-channel-compressed midis
# ============================================================
def decompose_by_channel(fname, out_dir=None):
	# load pattern as midi
	pattern = midi.read_midifile(fname)

	# list of names corresponding to following pc ranges
	family_names = ["piano", "chrom_percus", "organ", "guitar", "bass", "strings", "ensemble", "brass", "reed", "pipe", "synth_lead", "synth_pad", "synth_effects", "ethnic", "percussive", "sound_effects", "drums"]
	
	# constant ranges found in spec for instrument family grouping
	family_ranges = [range(0,8), range(8,16), range(16,24), range(24,32), range(32,40), range(40,48), range(48, 56), range(56,64), range(65,72), range(72,80), range(80, 88), range(88, 96), range(96,104), range(104,112), range(112, 120), range(120,128)]

	# create a list of lists to store tracks corresponding to each family
	grouped_tracks = [[] for x in family_ranges]

	channel_tracks = [midi.Track() for x in range(16)]
	track_has_content = [False for x in range(16)]
	# maps channels to instrument codes
	# channel_map = {}

	# make a track of all events that are not note on/note off events
	non_note_events = midi.Track()
	for track in pattern:
			for event in track:
				if "NoteOnEvent" not in repr(event) and "NoteOffEvent" not in repr(event):
					non_note_events.append(event)
					for t in channel_tracks:
						t.append(event)
				else:
					for i in range(len(channel_tracks)):
						if i == int(event.channel):
							channel_tracks[i].append(event)
						else:
							channel_tracks[i].append(midi.NoteOnEvent(tick=event.tick, velocity=0, pitch=midi.G_3))
				if "ProgramChangeEvent" in repr(event) and int(event.channel) != 9:
					for curr_family in range(len(family_ranges)):
						if int(event.data[0]) in family_ranges[curr_family]:
							grouped_tracks[curr_family].append(channel_tracks[int(event.channel)])
							break
					# channel_map[int(event.channel)] = int(event.data[0])
	grouped_tracks.append([channel_tracks[9]])

	fname_pre = fname.split(".")[0]

	for curr_family in range(len(grouped_tracks)):
		if grouped_tracks[curr_family] != []:
			out = midi.Pattern(format=pattern.format, resolution=pattern.resolution, tracks=(grouped_tracks[curr_family]))
			if out_dir is None:
				midi.write_midifile("{}_{}.mid".format(fname_pre, family_names[curr_family]), out)
			else:
				midi.write_midifile("{}_{}.mid".format(fname_pre, family_names[curr_family]), out)