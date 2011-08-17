import misaka

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

class Page(object):


    def __init__(self, output_dir_name, markdown_file):

        filename = markdown_file.split('.md')[0]

        page_name = str(output_dir_name.split('/')[-1]).title() + str(filename).title()
        page_name = page_name.replace('-', '')

        template_path = output_dir_name.split("/")
        page_template_name = "%s/%s.html" % ("/".join(template_path), filename) 


        if filename == "index":
            page_handler = "/%s/" % (output_dir_name)
        else:
            page_handler = "/%s/%s/" % (output_dir_name, filename)


        self.name = page_name
        self.markdown_file = markdown_file
        self.filename = filename
        self.template_name = page_template_name
        self.handler = page_handler
        self.output_dir_name = output_dir_name

    def write_html_file(self, output_directory, dirname):

        markdown_text = open(dirname + '/' + self.markdown_file, 'r')
        m = misaka.html(markdown_text.read())
        markdown_text.close()

        m = template_header + m + template_footer

        # make this path specifiable by the user as cmd arg
        

        # Change to a more readable format
        output_path = output_directory + "templates/%s/%s.html" % (self.output_dir_name, self.filename)
        output = open(output_path, 'w')
        output.write(m)
        output.close()



