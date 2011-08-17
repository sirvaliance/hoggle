""" Hoggle
The code is in a horrid state and will be refactored and cleaned up in the
morning.  This will eventually be generallized for a broad audience.  Possibly
adding auto deployment with Fabric.

The command line scripts are modeled after the eldarion gondor client
application (command arg parsing section)




"""
import os
import sys
import re
import dircache
import argparse
import ConfigParser
from distutils import dir_util

from tornado import template

from page import Page

main_app_template = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "app_templates", "main_app_template.txt"
)

def create_templates(arg, dirname, names):

    o_dir = dirname.split(arg["repo_dir"])
   
    del o_dir[0]

    d = "".join(o_dir)
    e = d.split("/")
    del e[0]
    del e[0]
    output_dirname = "/".join(e)
    
    template_path = os.path.join(arg['output_dir'],"templates/") + output_dirname

	# Check if template dir exists, if not create

    if not os.path.exists(template_path):
        os.makedirs(template_path)

    # Find all Markdown templates in current directory
    files = os.listdir(dirname)
    md_files = re.compile(".md$", re.IGNORECASE)
    files = filter(md_files.search, files) 

	# Iterate through all files in directory and gen output
    for f in files:
        # Build Page
        page = Page(output_dirname, f)
        page.write_html_file(arg["output_dir"], dirname)
        arg["template_list"].append(page)


def build_site(args, config):
    print "Build Site"

    template_list = list()

    dir_util.copy_tree(
            os.path.join(config["repo_dir"]),
            config["output_dir"])

    os.path.walk(os.path.join(config["repo_dir"], 'md/'), 
                 create_templates,
                {"repo_dir": config["repo_dir"], 
                 "output_dir": config["output_dir"],
                 "template_list": template_list })

    t = template.Template(open(main_app_template, 'r').read())

    main_output = t.generate(pages=template_list)

    f = open(config["output_dir"] + 'main.py', 'w')
    f.write(main_output)
    f.close()



# Pulled directly from the Gondor client code
def config_value(config, section, key, default=None):
    try:
        return config.get(section, key)
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        return default


def main():
    arg_parse = argparse.ArgumentParser(prog="hoggle")
    arg_parse.add_argument("-v", action="version", version="0.1")
    
    command_parsers = arg_parse.add_subparsers(dest="command")

    command_parse = command_parsers.add_parser("build")
    command_parse.add_argument("-repo", nargs=1)
    command_parse.add_argument("-output", nargs=1)
    
    args = arg_parse.parse_args()

    config = ConfigParser.RawConfigParser()
    config.read(os.path.expanduser(".hoggle"))
    config = {
        "repo_dir": config_value(config, "locations", "repo_dir"),
        "output_dir": config_value(config, "locations", "output_dir"),
    }
    if config["repo_dir"] is None or config["output_dir"] is None:
        print ("You must setup a .hoggle file to run hoggle.")

    {
        "build": build_site,

    }[args.command](args, config)
