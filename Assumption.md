### Assumptions when using the ingandLTV calculation:

1.	Data type of event(e) in Ingest function must be dictionary.
2.	Data type of data file (D) in Ingest function must be string(file name with Filename Extension)
3.	Data type of Top N (x) in TopXSimpleLTVCustomers function must be numeric.
4.	Data type of data file (D) in TopXSimpleLTVCustomers function must be string, no matter it is file name or file path.
5.	No matter what kinds of update for the event, the event_time is always the latest one.
6.	Customers may create personal files prior to really coming to the store. As a result, when counting total weeks for visit, the start date will be the first time that customer really visit the store. (Event table with Site_Visit)
7.  Simple LTV put emphasis on visiting the site, even though the orders may be from online shopping or by other media.
8.  Event_time is given whenever an event is given, and all the Event_times are in the correct format.


## Something about Pandas:

Pandas is a pretty convenient package for data preprocessing and data visualization. 

For example, we can handle the whole column by a single function without using for loop. It can easily construct list or dictionary into data table and output it. The most important thing is that there is no specific total columns or rows limit when using Pandas. In most of the situation we don’t need to do split into subset and combine them later, which is confusing and prone to mistakes.

Of course, there is still some drawback, like that the error-proof of pandas is weak, so sometimes we will need to check all the data prior to directly using Pandas and that Pandas is sensitive and prone to show warning message whenever it considers it’s a potential mistake point by human being, even though the coding logic is reasonable and that’s what you want to do.

In conclusion, pandas is easy to learn and full of powerful function. I will suggest that no matter we work for data analysis, data preprocess, or machine learning part,  it will be definitely beneficial to making good use of Pandas.

