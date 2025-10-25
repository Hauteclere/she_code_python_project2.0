import sys, os
from pathlib import Path
from bs4 import BeautifulSoup, Comment
from jinja2 import Environment, BaseLoader, TemplateSyntaxError, meta

class HTML_Widget():
    
    template_path = None
    data = None

    def get_template_path(self):
        if self.template_path is None:
            raise NotImplementedError('''
                All widgets must define the 'template_path' class attribute. 
                This attribute should set the template location for the widget.    
            ''')
        
        return Path(
            os.path.abspath(
                sys.modules[self.__class__.__module__].__file__
            )
        ).parent.joinpath(self.template_path)

    def get_template_source(self):
        with open(self.template_path) as template_file:
            template_source = template_file.read()

        soup = BeautifulSoup(template_source, "html.parser")

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        return soup.prettify()

    def check_template_syntax(self):
        try:
            self.env.parse(self.template_source)
        except TemplateSyntaxError as e:
            raise ValueError(f'''
                Invalid template supplied to {self.__cls__.__name__}. 
                Error on line {e.lineno} of template.
                Error message: {e.message}
            ''')

    def check_variables(self):
        variables = meta.find_undeclared_variables(
            self.env.parse(
                self.template_source
            )
        )
        
        for v in variables:
            if not hasattr(self, v):   
                raise NotImplementedError(f'''
                    The template for the {self.__class__.__name__} class calls for a template variable called "{v}". 
                    But this attribute is not defined on the class!
                ''')
            
        return variables

    def __init__(self):

        self.env = Environment(
            loader=BaseLoader
        )

        self.template_path  = self.get_template_path()
        self.template_source = self.get_template_source()
        self.variables = self.check_variables()


    def render(self):
 
        template = Environment(
            loader=BaseLoader
        ).from_string(
            self.template_source
        )
        
        data = {
            key: val for key, val in self.__class__.__dict__.items() if key in self.variables 
        }

        return template.render(**data)
    
    def save(self):
        with open(f"./{self.__class__.__name__}_output.html", 'w') as output_file:
            output_file.write(self.render())
    
