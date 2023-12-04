import psycopg2 

conn = psycopg2.connect(database="", user="", host="", password="") 
cursor = conn.cursor() 
cursor.execute("""SELECT * FROM teacher ORDER BY name""") 
conn.commit() 

rows = cursor.fetchall() 
for my_row in rows : 
    print(my_row)
