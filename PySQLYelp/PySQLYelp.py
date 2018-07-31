# ref: https://artemiorimando.com/2017/03/25/extract-transform-and-load-yelp-data-using-python-and-microsoft-sql-server/
## https://www.yelp.ca/developers/documentation/v3/business 
## https://www.yelp.ca/developers/documentation/v3/authentication
# We import the requests module which allows us to make the API call
import requests
 
# Replace [app_id] with the App ID and [app_secret] with the App Secret
app_id = 'app_id'
app_secret = 'app_secret'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
headers = {'Authorization': 'Bearer %s' % app_secret}
 
# Call Yelp API to pull business data for UPCIC 
biz_id = 'universal-property-and-casualty-insurance-company-fort-lauderdale'
url = 'https://api.yelp.com/v3/businesses/%s' % biz_id
response = requests.get(url = url, headers = headers)
response_data = response.json()

print(response_data)
print(type(response_data))

# Extract the business ID, name, price, rating and address
biz_id = response_data['id']
biz_name = response_data['name']
price = '' #response_data['price']
rating = response_data['rating']
review_count = response_data['review_count']
location = response_data['location']
address = location['display_address']
street = address[0]
city_prov_pc = address[1]
country = '' #address[2]

# Reassign data types to extracted data points
biz_id = str(biz_id)
biz_name = str(biz_name)
price = str(price)
rating = float(rating)
review_count = int(review_count)
street = str(street)
city_prov_pc = str(city_prov_pc)
country = str(country)

# We import the pyodbc module which gives us the ability to transfer data straight into Microsoft SQL Server
import pyodbc
 
# Creating the connection string. Specify:
## Database name. If it already exists, tables will be overwritten. If not, it will be created.
## Server name. If conecting remotely to the DSVM, the full DNS address should be used with the port number 1433 (which should be enabled) 
## User ID and Password. Change them below if you modified the default values.  
server_name = 'localhost'
db_name = 'tpcxbb_1gb'

connection_string_master = 'DRIVER={};SERVER={};DATABASE=master;TRUSTED_CONNECTION=True'.format("SQL Server", server_name)
cnxn_master = pyodbc.connect(connection_string_master, autocommit = True)
cursor_master = cnxn_master.cursor()
query_db = "if not exists(SELECT * FROM sys.databases WHERE name = '{}') CREATE DATABASE {}".format(db_name, db_name)
cursor_master.execute(query_db)

connection_string = 'DRIVER={};SERVER={};DATABASE={};TRUSTED_CONNECTION=True'.format("SQL Server", server_name, db_name)
connection = pyodbc.connect(connection_string, autocommit = True) 

# After a connection is established, we write out the data storage commands to send to Microsoft SQL Server
table_name = 'Yelp'
cursor = connection.cursor()

add_table = "if object_id('{}')	is null	\
begin \
    create table {} (				\
	     id				varchar(50)	\
	    ,name			varchar(50)	\
	    ,price			varchar(5)	\
	    ,rating			float		\
	    ,review_count	int			\
	    ,street			varchar(50)	\
	    ,city_prov_pc	varchar(50)	\
	    ,country        varchar(50)	\
	    ) \
end".format(table_name, table_name)

cursor.execute(add_table)

cursor.execute('insert into yelp (id, name, price, rating, review_count, street, city_prov_pc, country) values (?, ?, ?, ?, ?, ?, ?, ?)', biz_id, biz_name, price, rating, review_count, street, city_prov_pc, country)
 
