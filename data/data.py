import mysql.connector
from flask import Flask
import json

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="su3cl3jo3m6@A"
)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS taipei_web_data")
cursor.execute("USE taipei_web_data")
cursor.execute("CREATE TABLE IF NOT EXISTS attractions ( id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255), category VARCHAR(255), description TEXT(65535),address TEXT(65535),transport TEXT(65535),mrt TEXT(65535),latitude FLOAT(10,6),longitude FLOAT(10,6), images TEXT(65535) NOT NULL)")

with open('taipei-attractions.json',mode='r',encoding='utf-8')as file:
    data=json.load(file)
    for each in data['result']['results']:
        #得到濾過的圖片的列表
        image_file= each['file'].split('http://')
        image_file_filtered=[]
        
        for each_image in image_file:
            each_image=each_image.lower()
            if "png" in each_image or "jpg" in each_image:
                url= "http://"+ each_image
                image_file_filtered.append(url)
            
        print(each['stitle'])
        image_file_filtered=json.dumps(image_file_filtered)

   
        val = (each['stitle'], each['CAT2'],each['xbody'],each['address'],each['info'],each['MRT'],each['latitude'],each['longitude'],image_file_filtered)
        sql = "INSERT INTO attractions (name, category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, val)
        db.commit()  

