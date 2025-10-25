from she_codes_weather.utils.html_widget import HTMLWidget
from she_codes_weather.widgets.page_heading.page_heading import PageHeadingWidget
from she_codes_weather.widgets.date_and_time.date_and_time import DateAndTimeWidget
from she_codes_weather.widgets.daily_summary.daily_summary import DailySummaryWidget
from she_codes_weather.widgets.weekly_forecast.weekly_forecast import WeeklyForecastWidget
from she_codes_weather.widgets.page_footer.page_footer import PageFooterWidget

class HomePageWidget(HTMLWidget):
    title = "She Codes Weather"
    page_heading = PageHeadingWidget().render()
    # date_and_time = DateAndTimeWidget().render()
    # daily_summary = DailySummaryWidget().render()
    # weekly_forecast = WeeklyForecastWidget().render()
    # page_footer  = PageFooterWidget().render()
    
    template_path = "./homepage.html"
    css_path = "./styles.css"
    

