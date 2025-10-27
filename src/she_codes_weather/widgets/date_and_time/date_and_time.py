from datetime import datetime
from zoneinfo import ZoneInfo
from she_codes_weather.utils.html_widget import HTMLWidget

class DateAndTimeWidget(HTMLWidget):
    template_path="./date_and_time.html"

    def __init__(self):
        self.date_and_time = datetime.now(tz=ZoneInfo("Australia/Brisbane"))