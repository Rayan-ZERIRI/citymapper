f = open("emplacement-des-gares-idf.csv", 'r')
next(f)

for line in f:
    items = line.rstrip("\n").split(";")
    
    num_attributes = len(items)
    lst=items[0].split(',')
    i = 0
    insert_line = "INSERT INTO metros VALUES ( "
    while i < num_attributes:
        item = items[i].replace("'", "''")
        insert_line = insert_line + "'" + item + "'"
        if i != num_attributes - 1:
            insert_line = insert_line + ", "
        i = i + 1

    
    insert_line = insert_line + ", '" + lst[0] + "', '" + lst[1] + "');"
    print(insert_line)