import pyodbc

server = 'localhost'
db = 'first_test'
username = 'sa'
password = 'testingHuskies.123'

con_string = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ',1433;DATABASE=' + db + ';UID=' + username + ';PWD=' + password +';Encrypt=no;TrustServerCertificate=yes'
print(con_string)

con = pyodbc.connect(con_string)



cursor = con.cursor()

cursor.execute("""
  CREATE TABLE books_table (
    bookID INT IDENTITY(1, 1) PRIMARY KEY,
    rating VARCHAR(20),
    product_type VARCHAR(20),
    upc VARCHAR(20),
    title VARCHAR(20)
  )
""")

con.commit()
cursor.close()