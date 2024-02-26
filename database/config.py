import psycopg2

#establishing the connection
conn = psycopg2.connect(database="youtube", user='youtube_user', password='ega12345', host='127.0.0.1', port= '5432')
conn.autocommit = True
#Creating a cursor object using the cursor() method
cursor = conn.cursor()