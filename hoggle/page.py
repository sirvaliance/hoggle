class Page(object):


    def __init__(self, output_dir_name, filename):
        page_name = str(output_dir_name.split('/')[-1]).title() + str(filename).title()
        page_name = page_name.replace('-', '')

        template_path = output_dir_name.split("/")
        page_template_name = "%s/%s.html" % ("/".join(template_path), filename) 

        if filename == "index":
            page_handler = "/%s/" % (output_dir_name)
        else:
            page_handler = "/%s/%s/" % (output_dir_name, filename)


        self.name = page_name
        self.template_name = page_template_name
        self.handler = page_handler





