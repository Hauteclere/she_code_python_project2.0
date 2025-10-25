from _utils.html_widget import HTML_Widget
from widgets.page_heading.page_heading import PageHeadingWidget
from widgets.date_and_time.date_and_time import DateAndTimeWidget
from widgets.daily_summary.daily_summary import DailySummaryWidget
from widgets.weekly_forecast.weekly_forecast import WeeklyForecastWidget
from widgets.page_footer.page_footer import PageFooterWidget

class HomePageWidget(HTML_Widget):
    title = "She Codes Weather"
    page_heading = PageHeadingWidget().render()
    # date_and_time = DateAndTimeWidget().render()
    # daily_summary = DailySummaryWidget().render()
    # weekly_forecast = WeeklyForecastWidget().render()
    # page_footer  = PageFooterWidget().render()
    
    template_path = "./homepage.html"
    

