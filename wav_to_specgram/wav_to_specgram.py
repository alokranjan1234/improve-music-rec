import sys

from matplotlib import mlab
from wavio import *

def gen_specgram(audio_filename):
	"""generates spectogram from audio_filename"""
	samplerate, sampwidth, nchannels, samples = readwav(audio_filename) # Read the audio file
	samples = samples.T[0]	# Get the data for the channel (assuming this is a stem and we want the only existing channel)
	return mlab.specgram(samples, Fs=samplerate) # Compute the spectrogram

"""
- Compute and write out the spectrogram for a .wav audio file.
- Format of the spectrogram: each row corresponds to a time step, and each column is the intensity of
  the frequency at that time step.
- Individual values are delimited by spaces, and rows are delimited by newlines.
- Warning: writing out spectrograms for large audio files will take a long time and produce a very large output file.
"""
def write_specgram_as_txt(audio_filename, out_filename):
	Pxx, freqs, bins = gen_specgram(audio_filename)
	out = open(out_filename, "w");	# Write out the spectrogram
	for i in range(len(Pxx)):
		for j in range(len(Pxx[i])):
			out.write(str(Pxx[i][j]) + " ")
		out.write("\n")
	out.close()

def write_specgram_as_pickle(audio_filename, out_filename):
	Pxx, freqs, bins = gen_specgram(audio_filename)
	Pxx.dump(out_filename)


if (__name__ == "__main__"):
	if (len(sys.argv) != 3):
		print("usage: wav_to_specgram.py <input .wav file> <output file>")
		sys.exit()
	# write_specgram_as_txt(sys.argv[1], sys.argv[2])
	write_specgram_as_pickle(sys.argv[1], sys.argv[2])