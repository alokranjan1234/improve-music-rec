import numpy as np
from wav_to_specgram import *
import sys
from matplotlib import mlab
from wavio import *

def get_noisiest_window_index(arr, samplerate=44100, secs=30):
	"""given an array, returns the sample index of start and end of the window with the greatest sqrt of values
	   arr: array to find max in, will process by 0th dim
	   rate: how many samples per second. default set to standard
	   secs: size of window
	   incr: number of samples we shift window over each time 
	   		 before checking, by default 1/10th of the window size"""	
	rate = samplerate/128
	arr = arr.T
	print "arr.shape", arr.shape
	incr=(rate*secs)/6
	# assert window_size % incr == 0
	# number of incrs in our window
	incrs_per_window = (rate*secs)/incr
	
	# calculate all the sums of incrs
	incr_vals = []
	# current starting place of our window
	curr_index = 0
	while curr_index < arr.shape[0]/incr:
		left = curr_index*incr
		right = (curr_index+1)*incr
		sqrt_avg = np.sum(np.sqrt(np.sqrt(np.sqrt(np.sqrt(np.sqrt(arr[left:right]))))))
		incr_vals.append(sqrt_avg)
		time = convert_indexes_to_time((left, right), samplerate)
		print "{:3}:{:2} - {:3}:{:2} {:<17}".format(time[0]/60, time[0]%60, time[1]/60, time[1]%60, sqrt_avg)
		curr_index += 1

	current_max = 0
	max_index = 0
	incr_arr = np.asarray(incr_vals)
	for x in range(len(incr_vals) - incrs_per_window + 1):
		window_total = np.sum(incr_arr[x:x+incrs_per_window])
		if window_total > current_max:
			current_max = window_total
			max_index = x
	return (max_index*incr), ((max_index + incrs_per_window)*incr)

def convert_indexes_to_time(time_tuple, rate=44100):
	rate=rate/128
	return time_tuple[0]/rate, time_tuple[1]/rate

if (__name__ == "__main__"):
	if (len(sys.argv) != 2):
		print("usage: specgram_preprocessing.py <input .wav file>")
		sys.exit()
	# write_specgram_as_txt(sys.argv[1], sys.argv[2])

	audio_filename = sys.argv[1]
	samplerate, sampwidth, nchannels, samples = readwav(audio_filename) # Read the audio file
	samples = samples.T[0]	# Get the data for the channel (assuming this is a stem and we want the only existing channel)
	specgram = mlab.specgram(samples, Fs=samplerate)[0] # Compute the spectrogram
	time = convert_indexes_to_time(get_noisiest_window_index(specgram, samplerate=samplerate), rate=samplerate)
	print "{}:{} - {}:{}".format(time[0]/60, time[0]%60, time[1]/60, time[1]%60)