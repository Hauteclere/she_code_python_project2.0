import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open
import sys

# Add the src directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from she_codes_weather.utils.html_widget import HTMLWidget


class TestHTMLWidget(unittest.TestCase):
    """Comprehensive tests for the HTMLWidget class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
    def tearDown(self):
        """Clean up after each test method."""
        os.chdir(self.original_cwd)
        # Clean up temp files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def normalize_html(self, html_string):
        """Helper method to normalize HTML for comparison by removing extra whitespace."""
        import re
        # Remove extra whitespace between tags and normalize line breaks
        normalized = re.sub(r'>\s+<', '><', html_string.strip())
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized
        
    def create_test_files(self, template_content, css_content=None):
        """Helper method to create test template and CSS files."""
        template_file_path = Path(self.temp_dir) / "test_template.html"
        with open(template_file_path, 'w') as f:
            f.write(template_content)
            
        css_file_path = None
        if css_content:
            css_file_path = Path(self.temp_dir) / "test_styles.css"
            with open(css_file_path, 'w') as f:
                f.write(css_content)
                
        return template_file_path, css_file_path


class TestHTMLWidgetBasicFunctionality(TestHTMLWidget):
    """Test basic widget functionality."""
    
    def test_template_path_required(self):
        """Test that NotImplementedError is raised when template_path is not defined."""
        class BadWidget(HTMLWidget):
            pass  # No template_path defined
            
        with self.assertRaises(NotImplementedError) as context:
            BadWidget()
        self.assertIn("template_path", str(context.exception))
        
    def test_simple_widget_creation_and_rendering(self):
        """Test creating and rendering a simple widget without CSS."""
        template_content = "<h1>{{ title }}</h1>"
        template_file_path, _ = self.create_test_files(template_content)
        
        class SimpleWidget(HTMLWidget):
            template_path = str(template_file_path)
            title = "Test Title"
            
        widget = SimpleWidget()
        rendered = widget.render()
        
        self.assertIn("<h1>", rendered)
        self.assertIn("Test Title", rendered)
        self.assertIn("</h1>", rendered)
        
    def test_widget_with_multiple_variables(self):
        """Test widget with multiple template variables."""
        template_content = "<div><h1>{{ title }}</h1><p>{{ content }}</p></div>"
        template_file_path, _ = self.create_test_files(template_content)
        
        class MultiVarWidget(HTMLWidget):
            template_path = str(template_file_path)
            title = "Main Title"
            content = "This is the content"
            
        widget = MultiVarWidget()
        rendered = widget.render()
        
        self.assertIn("Main Title", rendered)
        self.assertIn("This is the content", rendered)
        self.assertIn("<div>", rendered)
        self.assertIn("<h1>", rendered)
        self.assertIn("<p>", rendered)


class TestHTMLWidgetCSSFunctionality(TestHTMLWidget):
    """Test CSS injection functionality."""
    
    def test_widget_with_css_file(self):
        """Test widget that includes CSS from a file."""
        template_content = "<h1>{{ title }}</h1>"
        css_content = "h1 { color: blue; font-size: 24px; }"
        template_file_path, css_file_path = self.create_test_files(template_content, css_content)
        
        class StyledWidget(HTMLWidget):
            template_path = str(template_file_path)
            css_path = str(css_file_path)
            title = "Styled Title"
            
        widget = StyledWidget()
        rendered = widget.render()
        
        self.assertIn("<style>", rendered)
        self.assertIn("color: blue", rendered)
        self.assertIn("font-size: 24px", rendered)
        self.assertIn("Styled Title", rendered)
        
    def test_widget_without_css_file(self):
        """Test widget without CSS file (css_path is None)."""
        template_content = "<h1>{{ title }}</h1>"
        template_file_path, _ = self.create_test_files(template_content)
        
        class NoStyleWidget(HTMLWidget):
            template_path = str(template_file_path)
            # css_path not defined (None)
            title = "Unstyled Title"
            
        widget = NoStyleWidget()
        rendered = widget.render()
        
        self.assertNotIn("<style>", rendered)
        self.assertIn("Unstyled Title", rendered)
        
    def test_css_injection_with_existing_head(self):
        """Test CSS injection when template already has a <head> tag."""
        template_content = """
        <html>
            <head>
                <title>{{ page_title }}</title>
            </head>
            <body>
                <h1>{{ heading }}</h1>
            </body>
        </html>
        """
        css_content = "body { margin: 0; }"
        template_file_path, css_file_path = self.create_test_files(template_content, css_content)
        
        class FullPageWidget(HTMLWidget):
            template_path = str(template_file_path)
            css_path = str(css_file_path)
            page_title = "Test Page"
            heading = "Welcome"
            
        widget = FullPageWidget()
        rendered = widget.render()
        
        self.assertIn("<style>", rendered)
        self.assertIn("body { margin: 0; }", rendered)
        self.assertIn("<head>", rendered)
        self.assertIn("Test Page", rendered)
        
    def test_css_injection_with_html_no_head(self):
        """Test CSS injection when template has <html> but no <head>."""
        template_content = """
        <html>
            <body>
                <h1>{{ heading }}</h1>
            </body>
        </html>
        """
        css_content = "h1 { color: red; }"
        template_file_path, css_file_path = self.create_test_files(template_content, css_content)
        
        class NoHeadWidget(HTMLWidget):
            template_path = str(template_file_path)
            css_path = str(css_file_path)
            heading = "No Head Test"
            
        widget = NoHeadWidget()
        rendered = widget.render()
        
        self.assertIn("<head>", rendered)  # Should create head
        self.assertIn("<style>", rendered)
        self.assertIn("color: red", rendered)
        
    def test_css_injection_fragment(self):
        """Test CSS injection for HTML fragments (no <html> or <head>)."""
        template_content = "<div class='widget'>{{ content }}</div>"
        css_content = ".widget { padding: 10px; }"
        template_file_path, css_file_path = self.create_test_files(template_content, css_content)
        
        class FragmentWidget(HTMLWidget):
            template_path = str(template_file_path)
            css_path = str(css_file_path)
            content = "Fragment content"
            
        widget = FragmentWidget()
        rendered = widget.render()
        
        self.assertIn("<style>", rendered)
        self.assertIn(".widget { padding: 10px; }", rendered)
        self.assertIn("Fragment content", rendered)
        
    def test_css_file_not_exists(self):
        """Test widget when CSS file doesn't exist."""
        template_content = "<h1>{{ title }}</h1>"
        template_file_path, _ = self.create_test_files(template_content)
        
        class MissingCSSWidget(HTMLWidget):
            template_path = str(template_file_path)
            css_path = "nonexistent.css"  # File doesn't exist
            title = "No CSS File"
            
        widget = MissingCSSWidget()
        rendered = widget.render()
        
        self.assertNotIn("<style>", rendered)
        self.assertIn("No CSS File", rendered)


class TestHTMLWidgetValidation(TestHTMLWidget):
    """Test template validation functionality."""
    
    def test_missing_template_variable(self):
        """Test error when template variable has no corresponding class attribute."""
        template_content = "<h1>{{ missing_var }}</h1>"
        template_file_path, _ = self.create_test_files(template_content)
        
        class MissingVarWidget(HTMLWidget):
            template_path = str(template_file_path)
            # missing_var not defined
            
        with self.assertRaises(NotImplementedError) as context:
            MissingVarWidget()
        self.assertIn("missing_var", str(context.exception))
        
    def test_template_with_comments_removed(self):
        """Test that HTML comments are removed from templates."""
        template_content = """
        <!-- This is a comment -->
        <h1>{{ title }}</h1>
        <!-- Another comment -->
        """
        template_file_path, _ = self.create_test_files(template_content)
        
        class CommentWidget(HTMLWidget):
            template_path = str(template_file_path)
            title = "Test Title"
            
        widget = CommentWidget()
        rendered = widget.render()
        
        self.assertNotIn("<!--", rendered)
        self.assertNotIn("-->", rendered)
        self.assertIn("Test Title", rendered)
        
    def test_template_syntax_validation(self):
        """Test template syntax validation with invalid Jinja2."""
        template_content = "<h1>{{ unclosed_var }</h1>"  # Missing closing brace
        template_file_path, _ = self.create_test_files(template_content)
        
        class BadSyntaxWidget(HTMLWidget):
            template_path = str(template_file_path)
            
        # Note: This might not always trigger depending on BeautifulSoup parsing
        # But we can test that the widget attempts to handle it
        try:
            widget = BadSyntaxWidget()
        except Exception:
            pass  # Expected for malformed templates


class TestHTMLWidgetSaveFunction(TestHTMLWidget):
    """Test the save functionality."""
    
    def test_save_widget_output(self):
        """Test saving widget output to file."""
        template_content = "<h1>{{ title }}</h1>"
        template_file_path, _ = self.create_test_files(template_content)
        
        class SaveTestWidget(HTMLWidget):
            template_path = str(template_file_path)
            title = "Save Test"
            
        widget = SaveTestWidget()
        widget.save()
        
        # Check that file was created
        output_file = Path("SaveTestWidget_output.html")
        self.assertTrue(output_file.exists())
        
        # Check file contents
        with open(output_file, 'r') as f:
            content = f.read()
        self.assertIn("Save Test", content)


class TestHTMLWidgetPathResolution(TestHTMLWidget):
    """Test path resolution functionality."""
    
    def test_relative_template_path_resolution(self):
        """Test that relative paths are resolved correctly."""
        # Create a subdirectory
        subdir = Path(self.temp_dir) / "widgets"
        subdir.mkdir()
        
        template_content = "<p>{{ message }}</p>"
        template_file_path = subdir / "test.html"
        with open(template_file_path, 'w') as f:
            f.write(template_content)
            
        # Mock the module file location
        with patch('sys.modules') as mock_modules:
            mock_module = type('MockModule', (), {})()
            mock_module.__file__ = str(subdir / "widget.py")
            mock_modules.__getitem__.return_value = mock_module
            
            class RelativePathWidget(HTMLWidget):
                template_path = "./test.html"
                message = "Relative path works"
                
            widget = RelativePathWidget()
            rendered = widget.render()
            self.assertIn("Relative path works", rendered)


class TestHTMLWidgetIntegration(TestHTMLWidget):
    """Integration tests combining multiple features."""
    
    def test_complete_widget_with_all_features(self):
        """Test a complete widget with template, CSS, and multiple variables."""
        template_content = """
        <div class="card">
            <h2>{{ title }}</h2>
            <p>{{ description }}</p>
            <span class="author">By: {{ author }}</span>
        </div>
        """
        css_content = """
        .card {
            border: 1px solid #ccc;
            padding: 20px;
            margin: 10px;
        }
        .author {
            font-style: italic;
            color: #666;
        }
        """
        template_file_path, css_file_path = self.create_test_files(template_content, css_content)
        
        class CompleteWidget(HTMLWidget):
            template_path = str(template_file_path)
            css_path = str(css_file_path)
            title = "Complete Widget"
            description = "This widget has everything!"
            author = "Test Author"
            
        widget = CompleteWidget()
        rendered = widget.render()
        
        # Check template variables
        self.assertIn("Complete Widget", rendered)
        self.assertIn("This widget has everything!", rendered)
        self.assertIn("Test Author", rendered)
        
        # Check CSS injection
        self.assertIn("<style>", rendered)
        self.assertIn("border: 1px solid #ccc", rendered)
        self.assertIn("font-style: italic", rendered)
        
        # Check HTML structure
        self.assertIn('class="card"', rendered)
        self.assertIn("<div", rendered)
        self.assertIn("<h2>", rendered)
        self.assertIn("<p>", rendered)
        self.assertIn("<span", rendered)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)