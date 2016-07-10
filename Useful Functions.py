from collections import defaultdict
from datetime import datetime as dt
## Read in the data from daily_engagement.csv and project_submissions.csv 
## and store the results in the below variables.
## Then look at the first row of each table.
def opening(filename):
    with open(filename, 'rb') as f:
        #Dictionary reader because it has headers
        reader = unicodecsv.DictReader(f)
        return list(reader)

def parse_date(date):
    """Takes a date as a string, and returns a Python datetime object. If there is no date given, returns None
    Arguments:
    date -- Date to be parsed
    """
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')

def parse_maybe_int(i):
    """Takes a string which is either an empty string or represents an integer, and returns an int or None.
    Arguments:
    i -- Number to be parsed
    """
    if i == '':
        return None
    else:
        return int(i)

def parse_float_to_int(num):
    """Parses a float string into an integer
    Arguments:
    num -- Float String to be parsed
    """
    return int(float(num))

def parse_bool(value):
    """Parses a string into boolean value
    Arguments:
    value -- value to parsed into boolean
    """
    return value == "True"

def renaming_column(dic, old_name, new_name):
    """renames a column in the dictionary
    Arguments:
    dic: dictionary to rename
    old_name: 
    new_name
    
    """
    for item in dic:
        item["account_key"] = item["acct"]
        del item["acct"]




def count_distinct(l, col_name):
    """Find the total number of rows and the number of unique items in table in each table.
    Arguments:
    l -- list to take the unique items from
    col_name -- column you want to take distinct
    """
    unique = set()
    count = 0
    for item in l:
        count += 1
        unique.add(item[col_name])
    #print len(unique), count
    return unique

def records_missing(l1 , l2):
    """takes two lists representing records and prints items ocurring in the first record but not the second
    Arguments:
    l1 -- first record
    l2 -- second second
    key
    
    """
    for line in l1:
        if line["account_key"] not in l2:
            print line


# Given some data with an account_key field, removes any records corresponding to Udacity test accounts
def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data



def within_one_week(first_date, second_date):
    """find the difference of first_date - second_date
    Arguments:
    first_date -- datetime object for the first date
    second_date -- date time object for the second date
    """
    time_delta = first_date - second_date
    return time_delta.days < 7 and time_delta.days>=0

# Create a dictionary of engagement grouped by student.
# The keys are account keys, and the values are lists of engagement records.
def group_by(key, l):
    """Takes a key and list of dictionaries to return an aggregated dictionary with the key and a list value 
    Arguments
    key -- key to aggregate upon
    l   -- list to aggregate
    
    """
    dic = defaultdict(list)
    for item in l:
        account_key = item[key]
        dic[account_key].append(item)
    return dic

# In[184]:

# Create a dictionary with the total minutes each student spent in the classroom during the first week.
# The keys are account keys, and the values are numbers (total minutes)
def aggregate(dic, item):
    """
    """
    aggr_dict = {}
    for account_key, engagement_for_student in dic.items():
        total_minutes = 0
        for engagement_record in engagement_for_student:
            total_minutes += engagement_record[item]
        aggr_dict[account_key] = total_minutes
    return aggr_dict
total_minutes_by_account = aggregate(engagement_by_account, 'total_minutes_visited')


# In[185]:

import numpy as np

# Summarize the data about minutes spent in the classroom
total_minutes = total_minutes_by_account.values()
def calc_mean_sd(l):
    print 'Mean:', np.mean(l)
    print 'Standard deviation:', np.std(l)
    print 'Minimum:', np.min(l)
    print 'Maximum:', np.max(l)
calc_mean_sd(total_minutes)


# ## Debugging Data Analysis Code

# In[186]:

#####################################
#                 8                 #
#####################################

## Go through a similar process as before to see if there is a problem.
## Locate at least one surprising piece of data, output it, and take a look at it.
#max_student = 0
#for k in total_minutes_by_account:
    #if total_minutes_by_account[k] > max_student:
        #max_student =  k
#print max_student
##engagement_by_account[max_student]


# ## Lessons Completed in First Week

# In[187]:

#####################################
#                 9                 #
#####################################

## Adapt the code above to find the mean, standard deviation, minimum, and maximum for
## the number of lessons completed by each student during the first week. Try creating
## one or more functions to re-use the code above.
#lessons = aggregate(engagement_by_account, "lessons_completed")
#calc_mean_sd(lessons.values())


# ## Number of Visits in First Week

# In[236]:

######################################
#                 10                 #
######################################

## Find the mean, standard deviation, minimum, and maximum for the number of
## days each student visits the classroom during the first week.
#visited = aggregate(engagement_by_account, "has_visited")
#calc_mean_sd(visited.values())


# ## Splitting out Passing Students

# In[261]:

######################################
#                 11                 #
######################################

## Create two lists of engagement data for paid students in the first week.
## The first list should contain data for students who eventually pass the
## subway project, and the second list should contain data for students
## who do not.
#passing_keys= set()
#non_passing_keys = set()
#passing_engagement = []
#non_passing_engagement = []
#subway_project_lesson_keys = ['746169184', '3176718735']
#for submission in paid_submissions:
    #if (submission["lesson_key"] in ['746169184', '3176718735']) and (submission["assigned_rating"] in ["PASSED", "DISTINCTION"]) :
            #passing_keys.add(submission["account_key"])
#for k, v in engagement_by_account.iteritems():
    #if k in passing_keys:
        #for item in engagement_by_account[k]:
            #passing_engagement.append(item)
    #else:
        #for item in engagement_by_account[k]:
            #non_passing_engagement.append(item)
#print len(passing_engagement)
#print len(non_passing_engagement)


# ## Comparing the Two Student Groups

# In[ ]:

######################################
#                 12                 #
######################################

## Compute some metrics you're interested in and see how they differ for
## students who pass the subway project vs. students who don't. A good
## starting point would be the metrics we looked at earlier (minutes spent
## in the classroom, lessons completed, and days visited).


# ## Making Histograms

# In[ ]:

######################################
#                 13                 #
######################################

## Make histograms of the three metrics we looked at earlier for both
## students who passed the subway project and students who didn't. You
## might also want to make histograms of any other metrics you examined.


# ## Improving Plots and Sharing Findings

# In[ ]:

######################################
#                 14                 #
######################################

## Make a more polished version of at least one of your visualizations
## from earlier. Try importing the seaborn library to make the visualization
## look better, adding axis labels and a title, and changing one or more
## arguments to the hist() function.

