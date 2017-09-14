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


# TODO, I want a default subrecord that gives me an intelligent default
check how the count of number of subrecords works with patient subrecords

# TODO I want episode detail
I want episode admissions for the last quaters
I want mean episode length, I want lower quaterile, upper quartile per quarter

# TODO I want a default view so that I can extend and implement my own views
I want to be able to register my own trendy views
I want to be able to add a prefix
