# ref: https://artemiorimando.com/2017/03/25/extract-transform-and-load-yelp-data-using-python-and-microsoft-sql-server/
# We import the requests module which allows us to make the API call
import requests
 
# Replace [app_id] with the App ID and [app_secret] with the App Secret
app_id = 'fp4o2wDF6FEzfrc1TWBQVA'
app_secret = 'mBWWL0UKTLCFRaW7bp7n8ltlJE79SvQXirCronnLevqW6IZbeVYDw7FYrhQmMDNSovGS7G62hqK6Y1nnk3iIht3C3EHLp7eDdr2uC6qR4FniDs9I6awrKBZ6BaRgW3Yx'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
token = requests.post('https://api.yelp.com/oauth2/token', data = data)
#access_token = token.json()['access_token']
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

# We import the pyodbc module which gives us the ability and functionality to transfer data straight into Microsoft SQL Server
import pyodbc
 
# Connect to the appropriate database by replacing [datasource_name] with the data source name as set up through the ODBC Data Source Administrator and by replacing [database] with the database name within SQL Server Management Studio
server_name = 'localhost'
db_name = 'tpcxbb_1gb'
connection_string = 'DRIVER={};SERVER={};DATABASE={};TRUSTED_CONNECTION=True'.format("SQL Server", server_name, db_name)
connection = pyodbc.connect(connection_string, autocommit = True)
 
# After a connection is established, we write out the data storage commands to send to Microsoft SQL Server
cursor = connection.cursor()

cursor.execute('INSERT INTO YELP (id, name, price, rating, review_count, street, city_prov_pc, country) values (?, ?, ?, ?, ?, ?, ?, ?)', biz_id, biz_name, price, rating, review_count, street, city_prov_pc, country)
 
cursor.commit()
