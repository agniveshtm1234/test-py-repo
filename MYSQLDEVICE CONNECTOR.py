#new mysql viewer2

while True:
    try:
        import mysql.connector as mc
        from prettytable import PrettyTable
        table1 = PrettyTable()
        table2 = PrettyTable()
        a = input("ENTER IP-ADDRESS OR DEVICE ID::")
        b = input("ENTER USER::")
        c = input("ENTER PASSWORD::")
        p = int(input("ENTER PORT NO::"))
        x = mc.connect(host = a , user = b , password = c , port= p)
        if x.is_connected():
            print(f"Successfully established connection with '{a}' MySQL Server")
        y= x.cursor()
        def DATABASE():
            y.execute("SHOW DATABASES")
            z = y.fetchall()
            count = y.rowcount
            table1.field_names=["Database_in_this_Server"]
            table1.clear_rows()
            for i in z:
                table1.add_row([i[0]])
            print()
            print(table1)
            print("NUMBER OF DATABASES IN THIS SERVER::",count)
            print()
            
        def TABLES():
            while True:
                try:
                    x.database = input("ENTER THE DATABASE NAME::")
                    table2.field_names=[f"Tables_in_{x.database}"]
                    y.execute("SHOW TABLES")
                    k = y.fetchall()
                    countt = y.rowcount
                    table2.clear_rows()
                    for j in k:
                        table2.add_row([j[0]])
                    print()
                    print(table2)
                    print("NUMBER OF TABLES IN THIS DATABASE::",countt)
                    print()
                    break
                except mc.Error as e:
                    if e.errno == 1049:
                        print()
                        print("         THERE IS NO SUCH DATABASE!!!        ")
                        print("+===========================================+")
                        print("| 1. ENTER DATABASE AGAIN --> PRESS(ENTER)  |")
                        print("| 2. EXIT FUNCTION        -->  TYPE EXIT    |")
                        print("+===========================================+")
                        c1 = input("ENTER YOUR CHOICE (PRESS ENTER/EXIT)::")
                        if c1 == "exit" or c1 == "EXIT":
                            break
                        else:
                            print()
                            continue
        def DATA():
            while True:
                try:
                    x.database = input("ENTER THE DATABASE NAME::")
                    table = input("ENTER TABLE NAME::")
                    t1 = "SHOW TABLES LIKE '{}'".format(table)
                    y.execute(t1)
                    z = y.fetchall()
                    if len(z) < 1:
                        print("THERE IS NO SUCH TABLE NAMED '{}' INSIDE THE DATABASE '{}'".format(table, x.database))
                        print("TRY AGAIN!!!")
                        print()
                    else:
                        t2 = "DESC {}".format(table)
                        y.execute(t2)
                        column_data = y.fetchall()
                        columns = [column[0] for column in column_data]
                        table3 = PrettyTable()
                        table3.clear_rows()
                        table3.field_names = columns
                        t3 = "SELECT * FROM {}".format(table)
                        y.execute(t3)
                        rows = y.fetchall()
                        if len(rows)<1:
                            print()
                            print("!!EMPTY SET/TABLE!!")
                            print("!!NOTHING TO SHOW!!")
                            print()
                        else:
                            counttt = y.rowcount
                            for row in rows:
                                table3.add_row(row)
                            print()
                            print(table3)
                            print("NUMBER OF ROWS IN THIS TABLE IS::",counttt)
                            print()
                            break
                except mc.Error as e:
                    if e.errno == 1049:
                        print()
                        print("         THERE IS NO SUCH DATABASE!!!        ")
                        print("+===========================================+")
                        print("| 1. ENTER DATABASE AGAIN --> PRESS(ENTER)  |")
                        print("| 2. EXIT FUNCTION        -->  TYPE EXIT    |")
                        print("+===========================================+")
                        c2 = input("ENTER YOUR CHOICE (PRESS ENTER/EXIT)::")
                        if c2 == "exit" or c2 == "EXIT":
                            break
                        else:
                            print()
                            continue


        def INSERT():
            while True:
                    try:
                        x.database = input("ENTER THE DATABASE NAME:: ")
                        table = input("ENTER THE TABLE NAME:: ")
                        t1 = "SHOW TABLES LIKE '{}'".format(table)
                        y.execute(t1)
                        z = y.fetchall()
                        if len(z) < 1:
                            print("THERE IS NO DATA IN THE TABLE NAMED '{}' IN DATABASE '{}'".format(table, x.database))
                            return
                        t2 = "DESC {}".format(table)
                        y.execute(t2)
                        coldata = y.fetchall()
                        n = int(input("ENTER THE NUMBER OF RECORDS:: "))
                        if n <= 0:
                            print("INVALID NUMBER OF RECORDS!")
                            return
                        columns = [col[0] for col in coldata]
                        query = "INSERT INTO {} ({}) VALUES ({})".format(
                            table,
                            ", ".join(columns),
                            ", ".join(["%s"] * len(columns))
                        )
                        
                        records = []
                        for _ in range(n):
                            values = []
                            print()
                            for col in coldata:
                                col_name = col[0]
                                value = input("ENTER THE {}:: ".format(col_name))
                                values.append(value if value != "" else None)
                            records.append(values)
                        y.executemany(query, records)
                        x.commit()
                        print(f"{n} RECORD(S) INSERTED SUCCESSFULLY!")
                        break
                    except ValueError:
                        print("INVALID INPUT! PLEASE ENTER A VALID NUMBER.")
                    except mc.Error as e:
                            if e.errno == 1049:
                                print()
                                print("         THERE IS NO SUCH DATABASE!!!        ")
                                print("+===========================================+")
                                print("| 1. ENTER DATABASE AGAIN --> PRESS(ENTER)  |")
                                print("| 2. EXIT FUNCTION        -->  TYPE EXIT    |")
                                print("+===========================================+")
                                c2 = input("ENTER YOUR CHOICE (PRESS ENTER/EXIT)::")
                                if c2 == "exit" or c2 == "EXIT":
                                    break
                                else:
                                    print()
                                    continue

                                
        def QUERY():
                while True:
                    try:
                        print("\n+======================================+")
                        print("|        CUSTOM QUERY EXECUTOR         |")
                        print("+======================================+")
                        print("|  Type your SQL query below.          |")
                        print("|  Type 'EXIT' to leave this section.  |")
                        print("+======================================+")
                        query = input("Enter your SQL Query: ")
                        if query.strip().upper() == "EXIT":
                            print("Exiting CUSTOM QUERY executor...")
                            break
                        y.execute(query)
                        # If the query produces results (e.g., SELECT), fetch and display them
                        if y.with_rows:
                            results = y.fetchall()
                            count = y.rowcount
                            if len(results) > 0:
                                table = PrettyTable()
                                table.field_names = [desc[0] for desc in y.description]
                                for row in results:
                                    table.add_row(row)
                                print("\nQuery Results:")
                                print(table)
                            else:
                                print("\nNo rows returned.")
                            print(f"Number of rows affected: {count}")
                        else:
                            # If the query does not produce results (e.g., INSERT, UPDATE, DELETE)
                            x.commit()
                            print(f"\nQuery executed successfully. Rows affected: {y.rowcount}")
                    except mc.Error as e:
                        print(f"\nMySQL Error: {e}")
                    except Exception as ex:
                        print(f"\nAn error occurred: {ex}")     
            
        while True:
            print()
            print("+=======================+")
            print("|       M Y S Q L       |")
            print("|       *********       |")
            print("|  |  1  | -> DATABASES |")
            print("|  |  2  | -> TABLES    |")
            print("|  |  3  | -> DATA      |")
            print("|  |  4  | -> INSERT    |")
            print("|  |  5  | -> QUERY     |")
            print("|  |  6  | -> EXIT      |")
            print("|                       |")
            print("+=======================+")
            print()
            ch = input("ENTER YOUR CHOICE:")
            if ch > "6":
                print("INVALID")
            elif ch == "1":
                DATABASE()
            elif ch == "2":
                TABLES()
            elif ch == "3":
                DATA()
            elif ch == "4":
                INSERT()
            elif ch == "5":
                QUERY()
            elif ch == "6":
                print("+=======================+")
                print("|        THANKYOU       |")
                print("+=======================+")
                break
            elif ch.isalpha():
                print("INVALID")
        break
        x.close()
    except mc.Error as e:
        if e.errno == 2005:
            print("+==================================================+")
            print("!                 *INVALID HOST                    !")
            print("! *ENTER THE VALID HOST-ID,IP-ADDRESS OR DEVICE-ID !")
            print("+==================================================+")
            continue
        if e.errno == 1045:
            print("+====================================+")
            print("!       *AUTHENTICATION FAILED       !")
            print("! *ENTER THE VALID USER AND PASSWORD !")
            print("+====================================+")
            continue
        if e.errno == 2003:
            print("+================================+")
            print("!         *ACCESS DENIED         !")
            print("!     *INVALID PORT-NUMBER       !")
            print("!  *ENTER THE VALID PORT-NUMBER  !")
            print("+================================+")
            continue
        if e.errno == 2013:
            print("+==========================================")
            print("!   *⚠️Lost Connection to the Server      !")
            print("!      *Internet Interrupted!!!           !")
            print("!  *Firewall rules changed for MySQL Port !")
            print("+=========================================+")
            continue
    except ValueError:
        print("+==================================================+")
        print("!                 *ACCESS DENIED                   !")
        print("!  *INVALID FORMAT FOR PORT NUMBER(USE NUMBERS)    !")
        print("!                  *TRY AGAIN                      !")
        print("+==================================================+")
        continue

    

