
# coding: utf-8

# In[30]:

def Ingest(e, D):
    ## Since ast is the default package of python, I do not add this package to the source file
    import ast
    ## Read data
    path = '.\\input\\'+D
    Data = open(path, "r")
    ## Transform string data to list with dict elements
    Data = ast.literal_eval(Data.read())
    ##　Append Event with Dictionary format
    Data.append(e)
    ## Output and replace as txt file
    with open(path, "w") as output:
        output.write(str(Data))


def TopXSimpleLTVCustomers(x, D):
    ## import necessary package
    import ast
    from src import pandas as pd
    
    #### Read data and reformat it into dataframe
    path = '.\\input\\'+D
    Data = open(path, "r") 
    df = pd.DataFrame(ast.literal_eval(Data.read()))
    ## Transform event_time to datatime
    df['event_time'] = pd.to_datetime(df['event_time'])

    
    #### LTV caculating process:
    ## Expenditure_per_visit = revenue / visit
    ## Number_of_visit_per_week = visits / week
    ## a = Expenditure_per_visit * Number_of_visit_per_week (a = Average_customer_value_per_week)
    ## LTV = 52(a)*t ## t=10 since average lifespan for Shutterfly is 10 years
    
    
    #### TotalRevenue for each customer: 
    ## Select Order table for calculating revenue
    RevData = df.ix[(df['type'] == 'ORDER')]
    ## We assume that "update" always happens after "new", 
    ## and then we just need to select the row with greatest event time for each order to get the updated information.
    RevData = RevData[RevData.groupby(['key'])['event_time'].transform(max) == RevData['event_time']]
    ## Reset index and drop column
    RevData = RevData.reset_index().drop('index', 1)
    ## Select customer_id and total_amount (each expenditure)
    Revenue_customer = RevData[['customer_id', 'total_amount']]
    ## Extract the numbers from string (total_amount) and transform it into numeric for calculation
    Revenue_customer['total_amount'] = pd.to_numeric(Revenue_customer['total_amount'].str.split(' ').str[0])
    ## Group by customer_id and get the summation
    Revenue_customer = Revenue_customer.groupby('customer_id').sum()

    
    ### Total visit for each customer:
    ## Select customer_id and type
    Total_visit = df[['customer_id', 'type']]
    ## Group by customer_id and count when 'type' = visit
    Total_visit = pd.DataFrame(Total_visit.groupby(['customer_id'])['type'].apply(lambda x: x[x =='SITE_VISIT'].count()))

    
    ### Total weeks from his first time visit to the last date :
    ## Select customer_id, event_time, type
    Total_weeks = df[['customer_id', 'event_time', 'type']]
    ## Only retain even type = site visit so that to get the correct time that customer first visit. Then drop the event type column.
    Total_weeks = Total_weeks.ix[(Total_weeks['type'] == 'SITE_VISIT')].drop('type', 1)
    ## Group by customer_id and get the time that customer first visit
    Total_weeks = Total_weeks[Total_weeks.groupby(['customer_id'])['event_time'].transform(min) == Total_weeks['event_time']]
    ## Get the updated time
    recent_date = df['event_time'].max()
    ## Count the weeks by getting the difference between the week number and year
    Total_weeks['count']= (recent_date.year-Total_weeks['event_time'].dt.year)*52+(recent_date.week-Total_weeks['event_time'].dt.week)+1
    ## Set index for merging table
    Total_weeks = Total_weeks.set_index('customer_id')

    #### Create big a geneal big table to record some important metrics and even for the usage in the future 
    ## Merging table by index: customer_id
    BigTable = pd.concat([Revenue_customer, Total_visit, Total_weeks], axis=1)
    ## Create column 'Expenditure_per_visit'
    BigTable['Expenditure_per_visit'] = BigTable['total_amount'] / BigTable['type']
    ## Create column 'Number_of_visit_per_week'
    BigTable['Number_of_visit_per_week'] = BigTable['type'] / BigTable['count']
    ## Create column 'a' (a = Average_customer_value_per_week)
    BigTable['a'] = BigTable['Expenditure_per_visit'] * BigTable['Number_of_visit_per_week']
    ## Average Lifetime Spam 
    t=10
    ## Create column 'LTV' to get every customer's LTV
    BigTable['LTV'] = 52*(BigTable['a'])*t
    ## Sort customers by LTV
    TopN = BigTable.sort_values(by='LTV',ascending=False)
    ## Only retain Top N customers
    TopN = TopN.head(x)
    ## reset index
    TopN = TopN.reset_index()
    ## get customer_id as list
    TopNlist = list(TopN.iloc[0:x]['customer_id'])
    
    
    ####Combine customer_id, LTV, and customer's last name
    ## Select Customer table 
    CusData = df.ix[(df['type'] == 'CUSTOMER')]
    ## We assume that "update" always happens after "new", 
    ## and then we just need to select the row with greatest event time for each customer to get the latest information.
    CusData = CusData[CusData.groupby(['key'])['event_time'].transform(max) == CusData['event_time']]
    ## Select data of TopN customers
    CusData = CusData[CusData['key'].isin(TopNlist)].reset_index().drop('index', 1)
    ## Left join to merge TopN table and TopN customer data, so that it prevent from that some table with customer_id but without last name
    Result = pd.merge(TopN, CusData, how = 'left', left_on = 'customer_id', right_on = 'key')
    ## Select 'customer_id', 'last_name', 'LTV' as what we need and rename column name
    Result = Result[['customer_id_x', 'last_name', 'LTV']].rename(columns={'customer_id_x':'customer_id'})
    
    outputpath = '.\\output\\TopXSimpleLTVCustomers('+str(x)+', '+D+').txt'
    Result.to_csv(outputpath)
    
    return Result

        

