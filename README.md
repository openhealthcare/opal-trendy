This is trendy - an [Opal](https://github.com/openhealthcare/opal) plugin.

Trendy allows an easy way to ask common questions.

How long on average do patients with coughs stay in our system?

What is the difference in the number of people between Winter and Summer.

For patients who have condition x, what is the average duration of their stay if given
the drug y

If patient has condition y what is the pie chart actually showing you
it should show the % of episodes that have condition y, vs different conditions.

The api is that you declare either a histogram, gauge, or pie chart, then an
a method name on trend that returns a function for these.

These methods are split out between the different mixins.

# TODO I want primary diagnosis where available
# TODO links in bar charts aren't working
# TODO episode admissions are in the wrong order
