#!/usr/bin/env python

""" Scripts for generating html templates from markdown files

Requirements:
	https://github.com/FSX/misaka

	pip install misaka



"""
import os
import sys
import re
import dircache

import misaka


if __name__ == "__main__":

	files = os.listdir('md')                    
	md_files = re.compile(".md$", re.IGNORECASE)
	files = filter(md_files.search, files) 

	for f in files:
		template = open('md/' + f, 'r')
		m = misaka.html(template.read())
		template.close()

		# make this path specifiable by the user as cmd arg
		filename = f.split('.md')[0]
		# Change to a more readable format
		output = open('templates/'+filename+'.html', 'w')
		output.write(m)
		output.close()
		
		
	
