import json
import requests
from pprint import pprint
import psycopg2
import datetime


def save_subtrade():
    print('Connecting to the PostgreSQL database...')
    try:
        conn = psycopg2.connect(
            host= "db-postgresql-lon1-10501-do-user-15128192-0.c.db.ondigitalocean.com",
            database= "defaultdb",
            user= "doadmin",
            password= "AVNS_18bVhfxQtTTBCXwY6Lw",
            port=25060
        )
        cur = conn.cursor() 
        # Pull data from Dodois
        subtrade_object = requests.get("http://159.65.21.91:3000/sub-trade")
        subtrade_object = subtrade_object.json()
        # return subtrade_object
            
        for data in subtrade_object['data']:
            subtrade_list = data
            print(subtrade_list)
            """
            Loop Through data list and pass neccessary Info
            """
            for list in data:
                cur.execute('SELECT * from "SubTrade" where "Id" = %s',[data['id']])
                subt = cur.fetchall()
                # print(subt)
                if len(subt) == 0:
                    print(data['sourcingStatus'])
                    cur.execute('Insert Into "SubTrade" ("Cost","Expenses_Amount","SourceTrading","Created_At","Updated_At","Remarks","Comments","ForeignCurrency","Quantity") values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(data['cost'],data['expenses']['amount'],data['sourcingStatus'],data['createdAt'],data['updatedAt'],data['remarks'],data['amountInForeignCurrency'],[data['quantity']]))
                    conn.commit()
                    print("Added to SubTrade" + data['quantity'])
                else:
                    len(subt) == True
                print("SubTrade Exists")
                
                
            # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
save_subtrade()