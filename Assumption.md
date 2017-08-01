### Assumptions when using the ingandLTV calculation:

1.	Data type of event(e) in Ingest function must be dictionary.
2.	Data type of data file (D) in Ingest function must be string(file name with Filename Extension)
3.	Data type of Top N (x) in TopXSimpleLTVCustomers function must be numeric.
4.	Data type of data file (D) in TopXSimpleLTVCustomers function must be string, no matter it is file name or file path.
5.	No matter what kinds of update for the event, the event_time is always the latest one.
6.	Customers may create personal files prior to really coming to the store. As a result, when counting total weeks for visit, the start date will be the first time that customer really visit the store. (Event table with Site_Visit)
7.  Simple LTV only count the situation that customer's walk-in buying. Online shopping or order by other media do not take into account.
8.  Event_time is given whenever an event is given.

