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


def find_markdown_templates(dirname):
    files = os.listdir(dirname)
    md_files = re.compile(".md$", re.IGNORECASE)
    return filter(md_files.search, files) 


def create_templates(arg, dirname, names):

    output_dir = dirname.replace(arg["repo_dir"], "")
    e = output_dir.split("/")
    output_dirname = e[-1]
    
    template_path = os.path.join(arg['output_dir'],"templates/") + output_dirname

	# Check if template dir exists, if not create

    if not os.path.exists(template_path):
        os.makedirs(template_path)

    print "Searching For Markdown Templates in %s/" % output_dirname

    files = find_markdown_templates(dirname)

    for f in files:
        page = Page(output_dirname, f)
        page.write_html_file(arg["output_dir"], dirname)
        arg["page_list"].append(page)
        print "Generated Page At %s" % page.handler


def build_site(args, config):
    print "Hoggle: Building Site at %s" % config["repo_dir"] 

    page_list = list()

    # Copy Over Project to Ouput Directory
    # This would include all static media, base templates
    dir_util.copy_tree(
            os.path.join(config["repo_dir"]),
            config["output_dir"])

    # Walk the md/ directory and generate the html templates
    os.path.walk(os.path.join(config["repo_dir"], 'md/'), 
                 create_templates,
                {"repo_dir": config["repo_dir"], 
                 "output_dir": config["output_dir"],
                 "page_list": page_list })


    # Use Tornado's templating system to generate the main.py python
    # File that the project will be run off of
    t = template.Template(open(main_app_template, 'r').read())
    main_output = t.generate(pages=page_list)
    f = open(config["output_dir"] + 'main.py', 'w')
    f.write(main_output)
    f.close()

def start_blog(args, config):
    blog_path = os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    "project_templates/blog")

    project_path = os.path.join(os.getcwd(), "blog")

    if not os.path.exists(project_path):
        os.makedirs(project_path)

    dir_util.copy_tree(blog_path, project_path)

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

    build_parse = command_parsers.add_parser("build")
    build_parse.add_argument("-repo", nargs=1)
    build_parse.add_argument("-output", nargs=1)

    blog_parse = command_parsers.add_parser("start-blog")
    blog_parse.add_argument("-path", nargs=1)
    
    args = arg_parse.parse_args()

    config = ConfigParser.RawConfigParser()
    config.read(os.path.expanduser(".hoggle"))
    config = {
        "repo_dir": config_value(config, "locations", "repo_dir"),
        "output_dir": config_value(config, "locations", "output_dir"),
    }
    if config["repo_dir"] is None or config["output_dir"] is None:
        print ("No .hoggle file found.")
        print ("You must setup a .hoggle file to build a project.")

    {
        "build": build_site,
        "start-blog": start_blog,

    }[args.command](args, config)
