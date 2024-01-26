# to import MySQLdb need to install pip install mysql-connector-python
# tutorial link: https://techwasti.com/fastapi-mysql-simple-rest-api-example
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '',
    'db': 'fastapi',
}

# Create a connection to the database
conn = mysql.connector.connect(**db_config)