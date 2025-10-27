<h1>The Codes Python Unit Project</h1>

> [!IMPORTANT]  
> TODO: replace csv files with another utils class that generates randomised data.

<h2>Table of Contents</h2>

- [Introduction](#introduction)
  - [How The Tools Work](#how-the-tools-work)
  - [What's Done Already](#whats-done-already)
  - [What You Need To Do](#what-you-need-to-do)

## Introduction
Your first unit showed you how to write HTML and CSS code to create websites. 

In this unit, you have learned how to write programs using Python. Perhaps you've been wondering: when do we get to the Python WEBSITES?

Great news! In this project we will demonstrate our Python skills in a way that also exercises our existing HTML/CSS knowledge! You'll use some tools we've written for you to create a webpage that shows weather information based on data from `.csv` files.

### How The Tools Work

The project repo defines a class called [`HTMLWidget`](./src/she_codes_weather/utils/html_widget.py) that you can use to create snippets of HTML. This class is already written for you, and you shouldn't need to touch it or read through it unless you want to do a deep dive on what's happening under the hood. 

Here's a quick explainer on how the `HTMLWidget` class is supposed to be used:

1. You create a subclass based on `HTMLWidget`. An example is [the `PageHeadingWidget` class](./src/she_codes_weather/widgets/page_heading/page_heading.py).
2. You create an HTML template using [the Jinja2 templating language](https://jinja.palletsprojects.com/en/stable/api/#basics), and add that template file's relative location to your new class as a **class attribute**. In the template, you specify how the attributes in your class should be rendered. Example: [the `page_heading.html` template](./src/she_codes_weather/widgets/page_heading/page_heading.html)
3. In your subclass, you write an `__init__` method to set one or more **instance attributes** on your subclass that define values that you want to render in HTML. For instance, `PageHeadingWidget`'s `__init__` method defines an attribute called `page_heading`.
4. You use the `.render()` method to insert the variables into the template, and then render the template as HTML! Check out [the `homepage.py` file](./src/she_codes_weather/widgets/homepage/homepage.py) to see `PageHeadingWidget` in use.

### What's Done Already

We've set up a widget called [`HomePageWidget`](./src/she_codes_weather/widgets/homepage/homepage.py) for you. It renders a homepage HTML file that is intended to display information about the weather. It does this by putting a bunch of HTML components together, by rendering a bunch of other widgets. But right now it is broken, because the component widgets are unfinished!

### What You Need To Do

Your job is to finish writing each of the HTML components. You'll need to complete the following components, and create a template for each of them:
- [`WeeklyForecastWidget`](./src/she_codes_weather/widgets/weekly_forecast/)
- [`DailySummaryWidget`](./src/she_codes_weather/widgets/daily_summary/)
- [`PageFooterWidget`](./src/she_codes_weather/widgets/page_footer/)

If you need an example of how this is supposed to work, take a look at the completed example widgets - [`PageHeadingWidget`](./src/she_codes_weather/widgets/page_heading/) and [`DateAndTimeWidget`](./src/she_codes_weather/widgets/date_and_time/). There's also a docstring in each widget's file describing how it is supposed to work and what it is supposed to look like.

> [!CAUTION]  
> Not yet there isn't!

You can check your work by running `bash run_tests.sh` from the project root directory. We've written some tests to make sure that your program creates the output we're expecting.

> [!CAUTION]  
> The tests aren't written yet!

The `HomePageWidget` also has a `styles.css` file in its directory. You can create whatever styles you like here to make the weather page beautiful, but they won't be tested, so they're completely up to you. Let your creative juices flow!