#!/usr/bin/env python
# encoding: utf-8
"""
parseSelection.py

Created by Stephen O'Connor on 2016-02-26.
Copyright (c) 2016 __MyCompanyName__. All rights reserved.
"""

import sys
import getopt
import json

help_message = '''
If you provide no arguments, it will use default values, looking for a file in the current directory called selection.json, and using output files according to IcoMoon.

usage:
parseIcomoonJson.py -if myselection.json -of MyFontIcons.h -c MyApp
'''

unrecognized_argument = 'Invalid argument provided.'

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def parse(inputFile, iconClass, outputFile):
	print >> sys.stderr, "Test Run!"
	
	jsonTextFile = open(inputFile)
	#print >> sys.stderr, jsonTextFile.read()
	
	if jsonTextFile == None:
		print >> sys.stderr, "Failed."
		return
	
	parsed_json = json.loads(jsonTextFile.read())
	#print >> sys.stderr, parsed_json
	if parsed_json == None:
		print >> sys.stderr, "Failed."
		return
	
	icoMoonFile = open(outputFile, "w")

	icoMoonFile.write(  "//\n" + 
	                    "//  " + outputFile + "\n" + 
	                    "//\n" +
	                    "//  Generated from " + inputFile + "\n" +
	                    "//\n\n\n" +
	                    "#ifndef " + iconClass + "_ICONS_h\n" +
	                    "#define " + iconClass + "_ICONS_h\n\n\n")
	
	#iterate over the keys
	
	outputArray = []
	
	for icon in parsed_json['icons']:
		props = icon['properties']
		iconName = props['name']
		iconCode = props['code']
		
		#sanitize
		iconName = iconName.split(", ")[0].encode('ascii', 'ignore').upper().replace("-", "_")
		
		#add to array of tuples
		outputArray.append((iconCode, iconName))
		
		print >> sys.stderr, iconName
		print >> sys.stderr, iconCode
		
	print >> sys.stderr, "\n"
	
	alreadyUsedNames = {}

	for key in outputArray:

		if key[1].__len__() > 0:
			suffix = ""
			if key[1] in alreadyUsedNames:
			    alreadyUsedNames[key[1]] = alreadyUsedNames[key[1]] + 1
			    lastNumber = alreadyUsedNames[key[1]]
			    suffix = "_%d" % lastNumber
			else:
			    alreadyUsedNames[key[1]] = 0
			#icoMoonFile.write(u'#define  ICOMOON_' + key[1] + suffix + ' "\\u%04X"\n' % (ord(key[0])))
			#line = u'#define  ' + iconClass + '_' + key[1] + suffix + ' ' + unichr(key[0]) + '\n'
			line = u'#define  ' + iconClass + '_' + key[1] + suffix + ' "\\u%04X"\n' % (key[0])
			print >> sys.stderr, line
			icoMoonFile.write(line)
	
	icoMoonFile.write("\n\n#endif");
	icoMoonFile.close();


def main(argv=None):
	
	output = None
	inFile = "selection.json"
	iconClass='ICOMOON'
	outputFile='IcomoonIcons.h'
	
	
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
		except getopt.error, msg:
			raise Usage(msg)
	
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--output"):
				output = value
			if option in ("-of", "--outputFile"):
				outputFile = value	
			if option in ("-if", "--input"):
				inFile = value
			if option in ("-c", "--class"):
				iconClass = value
			else:
				raise Usage(unrecognized_argument)
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2

	if output != None:
		print >> sys.stderr, 'There was output: ' + output
		
	parse(inFile, iconClass, outputFile)


if __name__ == "__main__":

#print >> sys.stderr, 'End of script.'
# It runs this line before the rest.  I guess you don't touch it
	sys.exit(main())
