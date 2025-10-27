from she_codes_weather.utils.html_widget import HTMLWidget

class PageHeadingWidget(HTMLWidget):
    template_path = "./page_heading.html"

    def __init__(self, heading_text):
        self.page_heading = heading_text
    