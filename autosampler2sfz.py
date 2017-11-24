#!/usr/bin/env python

from __future__ import print_function

import getopt
import glob
import os
import sys
from datetime import date
from getpass import getuser
from re import compile
from shutil import copy2


# Prints out a help message and exits
def exit_with_helpmsg(status=0):
    print ("Usage: autosampler2sfz.py [-h] [-n <name>] [-o <output_dir>] <samples_dir>\n")
    print ("Generates an SFZ sampled instrument from samples created by the Auto Sampler plugin.\n")
    print ("Arguments:")
    print ("  -h\tPrints out this help message.")
    print ("  -n\tThe name of the SFZ instrument. If not specified, the name of <samples_dir> will be used.")
    print ("  -o\tThe output directory. If not specified, the files will be saved to the current directory.")
    # TODO implement conversion to .wav
    # print("  -w\tConvert samples to .wav")
    # TODO output note names or note numbers
    print ()
    sys.exit(status)


# Prints out an error message and exits
def exit_with_error(s):
    print ("<Error> {0}\n".format(s))
    sys.exit(2)


noteOrder = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}


# Convert note name to note number
def note2number(note):
    note_regex = compile(r'^([A-G][#]?)([-]?\d)$')
    s = note_regex.search(note)
    if s:
        note_name = s.group(1)
        octave = int(s.group(2))
        if note_name in noteOrder:
            n = int(noteOrder[note_name]) + (int(octave) + 2) * 12
            if 0 <= n <= 127:
                return n
    return -1


# Convert note name to note number
def number2note(note_num):
    if 0 <= note_num <= 127:
        rem = (note_num % 12)
        octave = (note_num - rem) / 12 - 2
        note = ''
        for n in noteOrder.keys():
            if noteOrder[n] == rem:
                note = n
        if note != '':
            return note + str(octave)
    return ''


# Custom sort for sample file names
def sample_sort_cmp(f1, f2):
    cmp_regex = compile(r'^[\w,\s-]+([A-G][#]?)([-]?\d)-(\d{2,3})-[A-Z0-9]{4}\.AIF$')
    s1 = cmp_regex.search(os.path.basename(f1).upper())
    s2 = cmp_regex.search(os.path.basename(f2).upper())
    if s1 and s2:
        note1 = s1.group(1)
        octave1 = int(s1.group(2))
        velocity1 = int(s1.group(3))
        note2 = s2.group(1)
        octave2 = int(s2.group(2))
        velocity2 = int(s2.group(3))
        if octave1 > octave2:
            return 1
        elif octave1 < octave2:
            return -1
        elif noteOrder[note1] > noteOrder[note2]:
            return 1
        elif noteOrder[note1] < noteOrder[note2]:
            return -1
        elif velocity1 > velocity2:
            return 1
        elif velocity1 < velocity2:
            return -1
        else:
            return 0
    elif f1 > f2:
        return 1
    elif f1 == f2:
        return 0
    else:
        return -1


# Main function
def main(argv):
    opts = []
    args = []
    try:
        opts, args = getopt.getopt(argv, "hn:o:", [])
    except getopt.GetoptError:
        exit_with_helpmsg(2)

    # --------------------------
    # checking input directory -
    # --------------------------
    input_dir = ''
    samples = []
    if len(args) <= 0:
        exit_with_helpmsg(2)
    else:
        input_dir = args[0]
    if not(os.path.isdir(input_dir) and os.path.exists(input_dir)):
        exit_with_error("The input directory does not exist: " + input_dir)
    else:
        input_dir = os.path.normpath(input_dir)
        samples = glob.glob(input_dir + '/' + os.path.basename(input_dir) + '-*.aif')
        if not samples:
            exit_with_error('The input directory does not contain any Auto Sampler-generated samples.')
    sfz_name = os.path.basename(input_dir)

    # -------------------------
    # parsing other arguments -
    # -------------------------
    # convert2wav = False
    output_dir = ''
    for opt, arg in opts:
        if opt == '-h':
            exit_with_helpmsg()
        # elif opt == '-w':
        #    convert2wav = True
        elif opt == '-n':
            sfz_name = arg
        elif opt == '-o':
            output_dir = arg

    # ---------------------------
    # checking output directory -
    # ---------------------------
    if output_dir == '':
        output_dir = os.getcwd()
    elif not (os.path.isdir(output_dir) and os.path.exists(output_dir)):
        exit_with_error("The output directory does not exist: " + output_dir)
    else:
        output_dir = os.path.normpath(output_dir)
    output_samples_dir = output_dir + '/' + sfz_name
    if os.path.exists(output_samples_dir):
        if glob.glob(output_samples_dir + "/*.*"):
            exit_with_error("The following directory already exists and is not empty: " + output_samples_dir)
    else:
        os.makedirs(output_samples_dir)

    # --------------------------------
    # checking if SFZ already exists -
    # --------------------------------
    sfz_filename = sfz_name + '.sfz'
    if os.path.isfile(output_dir + '/' + sfz_filename):
        exit_with_error("File '{0}' already exists in the output directory.".format(sfz_filename))

    # --------------------
    # processing samples -
    # --------------------
    samples.sort(sample_sort_cmp)
    file_regex = compile(r'^[\w,\s-]+([A-G][#]?)([-]?\d)-(\d{2,3})-[A-Z0-9]{4}\.AIF$')

    # counting all notes used to calculate regions
    print ("Copying samples to the output directory...")
    notes = []
    for sample in samples:
        filename = os.path.basename(sample)
        s = file_regex.search(filename.upper())
        if s:
            note = s.group(1) + s.group(2)
            if note not in notes:
                notes.append(note)
            copy2(sample, output_samples_dir)

    # creating SFZ, writing header
    print ("Writing to {0}...".format(sfz_filename))
    f = open(output_dir + '/' + sfz_filename, 'w')
    print ("//-------------------------------------------------", file=f)
    print ("// SFZ created by autosampler2sfz.py", file=f)
    print ("// See https://github.com/shinybit/autosampler2sfz.py", file=f)
    print ("//", file=f)
    print ("// Name:   {0}".format(sfz_name), file=f)
    print ("// Author: {0}".format(getuser()), file=f)
    print ("// Date:   {0}".format(date.today().strftime('%d %b, %Y')), file=f)
    print ("//-------------------------------------------------\n", file=f)

    # writing regions to SFZ
    lovel = 0
    print ("<group>\n", file=f)
    for sample in samples:
        filename = os.path.basename(sample)
        s = file_regex.search(filename.upper())
        if s:
            hivel = int(s.group(3))
            lokey = s.group(1) + s.group(2)

            ind = notes.index(lokey)
            if ind + 1 == len(notes):
                hikey = lokey
            else:
                hikey = number2note(note2number(notes[ind + 1]) - 1)
            print ("<region>", file=f)
            print ("sample={0}\\{1}".format(sfz_name, filename), file=f)
            print ("lovel={0} hivel={1}".format(lovel, hivel), file=f)
            print ("lokey={0} hikey={1}".format(lokey.lower(), hikey.lower()), file=f)
            print ("pitch_keycenter={0}\n".format(lokey.lower()), file=f)
            if hivel < 127:
                lovel = hivel + 1
            else:
                lovel = 0

    # closing file and reporting success
    f.close()
    print ("Done.\n")


if __name__ == "__main__":
    main(sys.argv[1:])
