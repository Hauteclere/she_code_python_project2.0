import sys, os
from pathlib import Path
from bs4 import BeautifulSoup, Comment
from jinja2 import Environment, BaseLoader, TemplateSyntaxError, meta

class HTMLWidget():
    """
    Base class for creating HTML widgets with template and CSS support.
    
    This class provides a framework for creating reusable HTML components that can be
    rendered with Jinja2 templates and optional CSS styling. Widgets automatically
    inject CSS into templates and validate template variables against class attributes.
    
    Class Attributes:
        template_path (str): Relative path to the HTML template file. Must be defined by subclasses.
        css_path (str): Optional relative path to the CSS file for styling.
    """
    
    template_path = None
    css_path = None

    def _get_template_path(self):
        """
        Get the absolute path to the widget's HTML template file.
        
        Returns:
            Path: Absolute path to the template file.
            
        Raises:
            NotImplementedError: If template_path class attribute is not defined.
        """
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

    def _get_css_path(self):
        """
        Get the absolute path to the widget's CSS file.
        
        Returns:
            Path or None: Absolute path to the CSS file if css_path is defined, None otherwise.
        """
        if self.css_path is None:
            return None
        
        return Path(
            os.path.abspath(
                sys.modules[self.__class__.__module__].__file__
            )
        ).parent.joinpath(self.css_path)

    def _get_template_source(self):
        """
        Read and process the HTML template file, automatically injecting CSS if available.
        
        This method reads the template file, removes HTML comments, and automatically
        injects CSS styling into the appropriate location in the HTML structure:
        - If <head> exists: CSS added as <style> tag inside <head>
        - If <html> exists but no <head>: Creates <head> with <style> tag
        - For HTML fragments: Prepends <style> tag before content
        
        Returns:
            str: Processed and prettified HTML template source with CSS injected.
        """
        with open(self.template_path) as template_file:
            template_source = template_file.read()

        soup = BeautifulSoup(template_source, "html.parser")

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Add CSS to the template if available
        css_file_path = self._get_css_path()
        if css_file_path and css_file_path.exists():
            with open(css_file_path, 'r') as css_file:
                css_content = css_file.read()
                
                # Check if template already has a <head> tag
                head_tag = soup.find('head')
                if head_tag:
                    # Add style tag to existing head
                    style_tag = soup.new_tag('style')
                    style_tag.string = css_content
                    head_tag.append(style_tag)
                else:
                    # Check if we have an html tag to add head to
                    html_tag = soup.find('html')
                    if html_tag:
                        # Create head tag and add style
                        head_tag = soup.new_tag('head')
                        style_tag = soup.new_tag('style')
                        style_tag.string = css_content
                        head_tag.append(style_tag)
                        html_tag.insert(0, head_tag)
                    else:
                        # Just wrap the content with style tags (for widget fragments)
                        style_tag = soup.new_tag('style')
                        style_tag.string = css_content
                        soup.insert(0, style_tag)

        return soup.prettify()

    def _check_template_syntax(self):
        """
        Validate the Jinja2 template syntax.
        
        Raises:
            ValueError: If the template contains invalid Jinja2 syntax, with details
                       about the error location and message.
        """
        try:
            self.env.parse(self.template_source)
        except TemplateSyntaxError as e:
            raise ValueError(f'''
                Invalid template supplied to {self.__cls__.__name__}. 
                Error on line {e.lineno} of template.
                Error message: {e.message}
            ''')

    def _get_variables(self):
        """
        Validates that all template variables have corresponding class attributes and then returns the variables names as a set.
        
        Analyzes the template to find all undeclared Jinja2 variables and ensures
        that each variable has a corresponding attribute defined on the widget class.
        
        Returns:
            set: Set of variable names found in the template.
            
        Raises:
            NotImplementedError: If a template variable doesn't have a corresponding
                               class attribute.
        """
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
        """
        Initialize the HTML widget.
        
        Sets up the Jinja2 environment, processes the template file (including CSS injection),
        and validates that all template variables have corresponding class attributes.
        
        Raises:
            NotImplementedError: If template_path is not defined or if template variables
                               don't have corresponding class attributes.
            ValueError: If the template contains invalid Jinja2 syntax.
        """

        self.env = Environment(
            loader=BaseLoader,
            autoescape=True
        )

        self.template_path  = self._get_template_path()
        self.template_source = self._get_template_source()
        self._check_template_syntax()
        self.variables = self._get_variables()


    def render(self):
        """
        Render the widget to HTML using the template and class attributes.
        
        Creates a Jinja2 template from the processed template source and renders it
        using class attributes that match the template variables.
        
        Returns:
            str: Rendered HTML string with all template variables replaced by their
                 corresponding class attribute values.
        """
 
        template = self.env.from_string(
            self.template_source
        )
        
        data = {
            key: val for key, val in self.__class__.__dict__.items() if key in self.variables 
        }

        return template.render(**data)
    
    def save(self):
        """
        Save the rendered widget HTML to a file.
        
        Renders the widget and saves the output to a file named after the widget class
        in the current working directory. The filename format is: {ClassName}_output.html
        
        Example:
            If the widget class is 'PageHeadingWidget', the output file will be
            'PageHeadingWidget_output.html'
        """
        with open(f"./{self.__class__.__name__}_output.html", 'w') as output_file:
            output_file.write(self.render())
    
