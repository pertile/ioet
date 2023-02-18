# Installing and execution
To test this software you need Python 3 installed and execute:
1. Clone this project
2. Open a terminal
3. Go to the directory in which you cloned the project
4. Execute `python -m unittest discover`

Test data is on datatest.txt. You may chnage this file to test each line you want, or you could execute python then in Python shell type:

`from wage.wage import calculate_wage
calculate_wage("RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00")`

That would run the script for the first line of test data.

Also you can execute the script for a different file:
`python wage.py path/to/file`

# Architecture
The exercise defines a _paytable_ with the amount you pay according to the day of the week and time range worked.

Also sets a text file where each line represents weekday and timerange for a worker in a week.

Script consists of a single file `wage.py` in which I defined:
* a constant for the _paytable_
* a class named `Worktime` which represents timerange for a single day. This Worktime class has a method `get_amount` to calculate the wage for that worktime
* a function which receives a string to calculate the wage for a person. String is just a line of the textfile.
* a function that receives a filepath as a parameter and return what you should pay for eac line in the file.

The trick is that each worktime range may spread over more than one range in the Paytable. So you have to split the worktime to match Paytable ranges.

## Aproach
My main objective was to get a calculation that is not coupled with input format, so you could extend it later with a direct input from the user or an API. I could have built an object for the person, an interval or a day, it just seemed to me it would be overkilled for the complexity of the exercise.

I defined the paytable as a constant looking for a good balance between what they asked me for, and having an extensible behaviour. In a future you could replace the constant with an object read from another source.

### Paytable
Paytable is a list of objects, each of which consists of a day of the week (as defined in the exercise), a range of times made up by a _lower_ and an _upper_ attributes, and an amount value. 

For _upper_ and _lower_ I used `datime.timedelta` type because you can not substract two `datetime.time` but you can substract two `timedelta`.

### Worktime class
Worktime consists of a day of the week, and two attributes _lower_ and _upper_ that define a timerange (also defined as `timedelta` instead of `time`).

The main logic is defined on `get_amount()`. Firstly, it gets all of the possible timeranges for the weekday of the current Worktime. Then it compares Worktime range with each of the possible timeranges for that weekday. When you compare them there are five possibilities:
1. Your worktime start and end in the same range (the simplest scenario). You calculate wage for all of the worktime and current payment range. Example: worktime 10:00-15:00, payment range 09:00-17:00; 5 hours in that range.
2. Your worktime starts **and** ends after or before payment range (). You get 0 for current payment range. Example: worktime 2:00-7:00, payment range 09:00-17:00; 0 hours in that range
3. Your worktime starts in the interval but ends beyond of it. You calculate wage for worktime start and current payment upper limit. Example: worktime 10:00-20:00, payment range 09:00-17:00; 7 hours in that range 
4. Your worktime ends in the interval but starts before of it.  You calculate wage for worktime start and current payment upper limit. Example: worktime 10:00-20:00, payment range 09:00-17:00; 7 hours in that range 
5. Your worktime starts before the range **and** end after the range. You calculate wage for all of the current payment range. Example: worktime 08:00-20:00, payment range 09:00-17:00; 8 hours in that range

It multiples hours in that range by amount of the range and accumulates the result.

### Exceptions
It manages some exceptions in order not to crash for some wront input data, as not having an "=" sign to separate worker name from timerange, or having wrong hour format.



