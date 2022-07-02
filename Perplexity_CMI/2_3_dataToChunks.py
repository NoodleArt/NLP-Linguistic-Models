# Divide data into chunks and store in seperate files based on the range of perplexities in the order of 10 from 0 to 100.
# "3_CMI_values.txt" contains CMI values for about 11000 tweets.

# Initialization
CMI_values = []

# Read CMI values and store them in the list.
def getCMIValues(filename):
	f =open(filename, 'r')
	global CMI_values
	CMI_values = f.readlines()

# Divide the data into Chunks and store in seperate files.
def divideDataIntoChunks():
	f1 = open("Chunks/0_10.txt", 'w')
	f2 = open("Chunks/10_20.txt", 'w')
	f3 = open("Chunks/20_30.txt", 'w')
	f4 = open("Chunks/30_40.txt", 'w')
	f5 = open("Chunks/40_50.txt", 'w')
	f6 = open("Chunks/50_60.txt", 'w')
	f7 = open("Chunks/60_70.txt", 'w')
	f8 = open("Chunks/70_80.txt", 'w')
	f9 = open("Chunks/80_90.txt", 'w')
	f10 = open("Chunks/90_100.txt", 'w')
	f = open("3_text.txt", 'r')
	cnt=0
	for line in f:
		print cnt
		print CMI_values[cnt][:-1]
		cmi = float(CMI_values[cnt][:-1])
		if cmi>=0 and cmi<=