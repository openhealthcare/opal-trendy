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

# so we pass back, subrecord__t__function__field="value"
# or subrecord__value__etc

# TODO, For condition I want, when another condition is selected for it to give
#       Me the % chance the patient has other conditions

# TODO, I probably want a start page I'm just not sure how I want this...
#       its not really necessary for RFH and only necessary for UCH

# TODO, I want a default subrecord that gives me an intelligent default
What does that look like
for singletons, give me something like ethnicity
ie a pie chart of the ethnicity, all time, and a pie chart of this quarter
maybe the most common ft and free text,
the amount that's not entered
the amount that's ft and fk


for singletons I want the number of coded jobbies
if there's



for non singletons
a pie chart of this quarter, a pie chart of the amount this quarter
maybe the most common ft and free text, the amount that's not entered
