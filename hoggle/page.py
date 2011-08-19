import misaka

class Page(object):

    def __init__(self, output_dir_name, markdown_file):

        filename = markdown_file.split('.md')[0]

        page_name = output_dir_name.split('/')[-1].title()
        page_name += filename.title()
        page_name = page_name.replace('-', '')

        template_path = output_dir_name.split("/")
        page_template_name = "%s/%s.html" % ("/".join(template_path), filename)

        if filename == "index":
            page_handler = "/%s/" % (output_dir_name)
        else:
            page_handler = "/%s/%s/" % (output_dir_name, filename)

        self.name = page_name
        self.title = self.create_title(output_dir_name)
        self.markdown_file = markdown_file
        self.filename = filename
        self.template_name = page_template_name
        self.handler = page_handler
        self.output_dir_name = output_dir_name

    def create_title(self, output_dir_name):
        return output_dir_name.replace("-", " ").title()

    def wrap_template(self, body):
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

        return template_header + body + template_footer

    def write_html_file(self, output_directory, dirname):

        markdown_text = open(dirname + '/' + self.markdown_file, 'r')
        m = misaka.html(markdown_text.read())
        markdown_text.close()

        m = self.wrap_template(m)

        # Change to a more readable format
        output_path = output_directory + "templates/%s/%s.html"
        output_path = output_path % (self.output_dir_name, self.filename)
        output = open(output_path, 'w')
        output.write(m)
        output.close()
