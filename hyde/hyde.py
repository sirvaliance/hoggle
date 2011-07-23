""" Scripts for generating html templates from markdown files

Requirements:
	Misaka for generating Html from Markdown
	Tornado for generating code using templates
	https://github.com/FSX/misaka

	pip install misaka
	pip install tornado



"""
import os
import sys
import re
import dircache

import misaka

from tornado import template


main_app_template = "main_app_template.txt"

template_header = """
{% extends "../base.html" %}

{% block content %}
<div class="grid_7">

"""

template_footer = """
	<div class="clear_40"></div>
</div>	
{% end %}

"""


global template_list

def create_templates(arg, dirname, names):


	d_list = dirname.split("/")
	del d_list[0]
	output_dirname = "/".join(d_list)
	
	template_path = "templates/%s" % output_dirname

	# Check if template dir exists, if not create
	if not os.path.exists(template_path):
		os.makedirs(template_path)

	# Find all Markdown templates in current directory
	files = os.listdir(dirname)                    
	md_files = re.compile(".md$", re.IGNORECASE)
	files = filter(md_files.search, files) 

	# Iterate through all files in directory and gen output
	for f in files:

		markdown_text = open(dirname + '/' + f, 'r')
		m = misaka.html(markdown_text.read())
		markdown_text.close()

		m = template_header + m + template_footer

		# make this path specifiable by the user as cmd arg
		filename = f.split('.md')[0]

		
		# Change to a more readable format
		output_path = "templates/%s/%s.html" % (output_dirname, filename)
		output = open(output_path, 'w')
		output.write(m)
		output.close()

		cls = dict()
		cls["name"] = str(output_dirname.split('/')[-1]).title() + str(filename).title()
		cls["template_name"] = "%s/%s.html" % (output_dirname, filename) 

		if filename == "index":
			cls["handler"] = "/%s/" % (output_dirname)
		else:
			cls["handler"] = "/%s/%s/" % (output_dirname, filename)

		print cls["handler"]

		template_list.append(cls)
		

if __name__ == "__main__":

	template_list = list()
	os.path.walk('md/', create_templates, True)	

	t = template.Template(open(main_app_template, 'r').read())
	main_output = t.generate(classes=template_list)
	f = open('main.py', 'w')
	f.write(main_output)
	f.close()

