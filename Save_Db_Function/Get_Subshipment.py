import json
import requests
from pprint import pprint
import psycopg2
import datetime


def save_subshipments():
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
        # Pull data from Subshipment
        payload = {}
        headers = { 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkdW5haml5ZUBnbWFpbC5jb20iLCJzdWIiOjMsImlhdCI6MTcwNDAxMTE5OSwiZXhwIjoxNzA2NjAzMTk5fQ.02RS6sqOLk8-cpZXmQeqF6fnojcXBnpTh92Rb4BpE9A'}
        polyforte_url = "https://vm-backend-ane5.onrender.com/shipment?company=Polyforte"
        res_ = requests.request("GET",polyforte_url, headers=headers, data=payload)
        ship_op_object_poly = res_.json()
        print(ship_op_object_poly)
        
        Safari_Polymers_url = "https://vm-backend-ane5.onrender.com/shipment?company=Safari Polymers"
        res_ = requests.request("GET",Safari_Polymers_url, headers=headers, data=payload)
        ship_op_object_safari= res_.json()
        print(ship_op_object_safari)

        for data in ship_op_object_safari['data']:
            ship_op_list_safari = data
            # print(port_list)
            
        for data in ship_op_object_poly['data']:
            sort_op_list_poly = data
            # print(port_list)
    
            """
            Loop Through data list and pass neccessary Info
            """
            for list in data:
                cur.execute('SELECT * from "Shipment" where "Id" = %s',[data['id']])
                ship_op_safari = cur.fetchall()
                if len(ship_op_safari) == 0:
                    print(data['subShipments']['id']) 
                    cur.execute('Insert Into "Shipment" ("Shipment_Id","Date","Company_Name","Product_Type","Product_Quantity", "Created_At","Updated_At","SubShipment_Id") values (%s,%s,%s,%s,%s,%s,%s,%s)',([data['shipmentId'],data['date'],data['company'],data['productType'],data['productQuantity'],data['updatedAt'],data['subShipments']['id']]))
                    print("Added Safari to Shipment " + data['name'])
                    
            for list in data:
                cur.execute('SELECT * from "Shipment" where "Id" = %s',[data['id']])
                ship_op = cur.fetchall()
                if len(ship_op) == 0:
                    print(data['subShipments']['id']) 
                    cur.execute('Insert Into "Shipment" ("Shipment_Id","Date","Company_Name","Product_Type","Product_Quantity", "Created_At","Updated_At","SubShipment_Id") values (%s,%s,%s,%s,%s,%s,%s,%s)',([data['shipmentId'],data['date'],data['company'],data['productType'],data['productQuantity'],data['updatedAt'],data['subShipments']['id']]))
                    print("Added Safari to Shipment " + data['name'])
            
            conn.commit()    
            # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print('Database connection closed.')
save_subshipments()