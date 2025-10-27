from she_codes_weather.utils.html_widget import HTMLWidget
from she_codes_weather.widgets.page_heading.page_heading import PageHeadingWidget
from she_codes_weather.widgets.date_and_time.date_and_time import DateAndTimeWidget
from she_codes_weather.widgets.daily_summary.daily_summary import DailySummaryWidget
from she_codes_weather.widgets.weekly_forecast.weekly_forecast import WeeklyForecastWidget
from she_codes_weather.widgets.page_footer.page_footer import PageFooterWidget

class HomePageWidget(HTMLWidget):
    
    
    template_path = "./homepage.html"
    css_path = "./styles.css"
    
    def __init__(self):
        self.title = "She Codes Weather"

        self.page_heading = PageHeadingWidget(
            heading_text="She Codes Weather"
        ).render()

        self.date_and_time = DateAndTimeWidget().render()

        self.weekly_forecast = WeeklyForecastWidget(
            source_data = "./data/this_week.csv"
        ).render()

        self.next_week_forecast = WeeklyForecastWidget(
            source_data = "./data/next_week.csv"
        ).render()

        self.daily_summary = DailySummaryWidget(
            source_data = "./data/this_week.csv"
        ).render()

        self.page_footer  = PageFooterWidget().render()

