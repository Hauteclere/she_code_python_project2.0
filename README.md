<h1>The Codes Python Unit Project</h1>

<h2>Table of Contents</h2>

- [Introduction](#introduction)
  - [How This Project Works](#how-this-project-works)
  - [What You Need To Do](#what-you-need-to-do)

## Introduction
Your first unit showed you how to write HTML and CSS code to create websites. 

In this unit, you have learned how to write programs using Python. Perhaps you've been wondering: when do we get to the Python WEBSITES?

Honestly, that's the next unit. In that unit we will use a Python library called Django Rest Framework to create a website back-end.

But in the meantime, there's no reason we can't choose a way to demonstrate out Python skills that exercises our existing HTML/CSS knowledge! That's what this project aims to do.

### How This Project Works

The project repo defines a class called [`HTMLWidget`](./src/she_codes_weather/utils/html_widget.py) that you can use to create snippets of HTML. This class is already written for you, and you shouldn't need to touch it or read through it unless you want to do a deep dive on what's happening under the hood. 

Here's a quick explainer on how the `HTMLWidget` class is supposed to be used:

1. You create a subclass based on `HTMLWidget`. An example is [the `PageHeadingWidget` class](./src/she_codes_weather/widgets/page_heading/page_heading.py).
2. You set one or more class attributes on your subclass that define values that you want to render in HTML. For instance, `PageHeadingWidget` defines an attribute called `page_heading`.

> [!CAUTION]  
> Need to refactor this. They should be instance attributes that get set in an `__init__` method, but I'll need to change the `HTMLWidget` code to make that work.

3. You create an HTML template using [the Jinja2 templating language](https://jinja.palletsprojects.com/en/stable/api/#basics), and add that template's relative location to your new class as a **class attribute**. In the template, you specify how the attributes in your class should be rendered.
4. You use the `.render()` method to insert the variables into the template, and then render the template as a string!

### What You Need To Do

We've set up a widget called [`HomePageWidget`](./src/she_codes_weather/widgets/homepage/homepage.py) for you. It renders a homepage HTML file that is intended to display information about the weather. It does this by putting a bunch of HTML components together, by rendering a bunch of other widgets. But right now it is broken, because the component widgets are unfinished!

Your job is to finish writing each of the HTML components. You'll need to complete the following components, and create a template for each of them:
- [`DateAndTimeWidget`](./src/she_codes_weather/widgets/date_and_time/)
- [`DailySummaryWidget`](./src/she_codes_weather/widgets/daily_summary/)
- [`WeeklyForecastWidget`](./src/she_codes_weather/widgets/weekly_forecast/)
- [`PageFooterWidget`](./src/she_codes_weather/widgets/page_footer/)

> [!NOTE]  
> Need to insert another element here that uses the weekly forecast widget to show next week's forecast too. This will demonstrate to students why we are using classes to begin with.

There's a docstring in each widget's file describing how it is supposed to work and what it is supposed to look like.

You can check your work by running `bash run_tests.sh` from the project root directory. We've written some tests to make sure that your program creates the output we're expecting.

The `HomePageWidget` also has a `styles.css` file in its directory. You can create whatever styles you like here to make the weather page beautiful, but they won't be tested, so they're completely up to you. Let your creative juices flow!