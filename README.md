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

# TODO, I want to histogram of ages
# TODO, I want a graph of episode starts per team
# TODO, For condition I want, when another condition is selected for it to give
#       Me the % chance the patient has other conditions

# TODO, I want a graph of the average amount of time between start and end
#       I want median, mean, max, min +1 std + 2std, -1 std -2std (as lowercase sigma)

# TODO, I probably want a start page I'm just not sure how I want this...
#       its not really necessary for RFH and only necessary for UCH
