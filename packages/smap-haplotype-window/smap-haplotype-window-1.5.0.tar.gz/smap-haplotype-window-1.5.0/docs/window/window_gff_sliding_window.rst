.. _SMAPwindowgffscripts:

###############################################
Creating sliding windows for Shotgun Sequencing
###############################################

| Here, we describe a short workflow to generate sets of Borders flanking sliding windows for haplotyping Shotgun Sequencing data. A bash script is used to pass arguments on to a Python script that, in turn, creates a GFF file containing the Borders flanking a set of sliding windows for a given reference sequence.
| Users can define Stepsize, Windowsize, and Borderlength that together delineate the sliding windows.
| The end of line (EOL) of the bash script should be Unix (LF). The output GFF file will appear in the same directory as the reference FASTA file.
| Usage: ``bash /path/to/Writegff.sh``.

Writegff.sh
-----------

::

	#!/bin/bash
	source /path/to/VirtualEnvironmentContainingPython/.venv/bin/activate

	# A simple script that creates a GFF file based on a FASTA file 
	# with customizable Stepsize, Windowsize, and Borderlength.
	# The output file name is the same as the input file name but with suffix .gff 
	# The GFF will be placed in the same directory as the reference sequence.
	# Usage: bash /path/to/Writegff.sh

	python3 /path/to/Writegff.py \
		--Fasta /path/to/reference/sequence/sequence.fa \
		--Windowsize 50 \
		--Stepsize 10 \
		--Borderlength 10

	deactivate

----

Writegff.py
-----------

::

	#!usr/bin/python3

	import argparse
	import os

	# Create an ArgumentParser object
	parser = argparse.ArgumentParser(description = '')

	parser.add_argument('--Fasta',
						type = str,
						default = None)

	parser.add_argument('--Windowsize',
						type = int,
						default = None)

	parser.add_argument('--Stepsize',
						type = int,
						default = None)

	parser.add_argument('--Borderlength',
						type = int,
						default = None)

	# Parse arguments to a dictionary
	args = vars(parser.parse_args())

	def Writegff(windowsize = args['Windowsize'], stepsize = args['Stepsize'], borderl = args['Borderlength'], reference = args['Fasta']):
		outputname = "".join(reference.split('.')[:-1]) + '.gff'
		outputfile = open(outputname,"w+")
		ref = open(reference, "r")
		for row in ref:
			if row.startswith(">"):
				ID = row.replace('>','').rstrip()
				seq = next(ref)
				seq = seq.rstrip()
				stoppos = len(seq)
				seqlen = len(str(stoppos))
				pos = 1
				SerialNumber = 1
				SerialNumberLen = len(str((stoppos - windowsize - 2*borderl) // stepsize))
				while pos < stoppos and pos + windowsize + 2*borderl < stoppos:
					print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(ID, "SMAP", "Border_Up", pos, pos + borderl, ".", "+", ".", "NAME=" + ID + "_" + str(pos).zfill(seqlen) +"_" + str(SerialNumber).zfill(SerialNumberLen) + " " + "POOL=" + os.path.splitext(os.path.basename(reference))[0] + " " + "SEQ=" +seq[pos-1: pos + borderl -1]), file =outputfile)
					print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(ID, "SMAP", "Border_Down", pos + borderl + windowsize +1, pos + 2*borderl + windowsize, ".", "+", ".", "NAME=" + ID + "_" + str(pos).zfill(seqlen) +"_" + str(SerialNumber).zfill(SerialNumberLen) + " " + "POOL=" + os.path.splitext(os.path.basename(reference))[0] + " " + "SEQ=" +seq[pos + borderl + windowsize +1 : pos + 2*borderl + windowsize +1]), file =outputfile)
					pos = pos + stepsize
					SerialNumber = SerialNumber + 1

		return

	Writegff()