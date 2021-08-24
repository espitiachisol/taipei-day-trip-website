import mysql.connector
from mysql.connector import pooling
from flask import Flask
import json,os
from dotenv import load_dotenv
load_dotenv()
PASSWORD=os.getenv("PASSWORD")

dbconfig = {
   "host":"localhost",
    "user":"root",
    "password":PASSWORD,
    "buffered":True
}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 5,
                                                      **dbconfig)
                                             
cnx= cnxpool.get_connection()
cursor = cnx.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS taipei_web_data")
cursor.execute("USE taipei_web_data")
#create tables
cursor.execute("CREATE TABLE IF NOT EXISTS attractions ( id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255), category VARCHAR(255), description TEXT(65535),address TEXT(65535),transport TEXT(65535),mrt TEXT(65535),latitude FLOAT(10,6),longitude FLOAT(10,6), images TEXT(65535) NOT NULL)")

cursor.execute("CREATE TABLE IF NOT EXISTS users( id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")

cursor.execute("CREATE TABLE IF NOT EXISTS orders( orderId BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,usermail VARCHAR(255),attractionId BIGINT NOT NULL,date VARCHAR(255), time VARCHAR(255), price VARCHAR(255))")

cursor.execute("CREATE TABLE IF NOT EXISTS payStatus( payStatusId BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,orderNumber VARCHAR(255) NOT NULL,status SMALLINT(1) NOT NULL,contactName VARCHAR(255),contactMail VARCHAR(255),contactphone VARCHAR(255),usermail VARCHAR(255),attractionId BIGINT NOT NULL,date VARCHAR(255), time VARCHAR(255), price VARCHAR(255))")



with open('taipei-attractions.json',mode='r',encoding='utf-8')as file:
    data=json.load(file)
    for each in data['result']['results']:
        #得到濾過的圖片的列表
        image_file= each['file'].split('http://')
        image_file_filtered=[]
        
        for each_image in image_file:
            each_image=each_image.lower()
            if "png" in each_image or "jpg" in each_image:
                url= "https://"+ each_image
                image_file_filtered.append(url)
        image_file_filtered=json.dumps(image_file_filtered)

   
        val = (each['stitle'], each['CAT2'],each['xbody'],each['address'],each['info'],each['MRT'],each['latitude'],each['longitude'],image_file_filtered)
        sql = "INSERT INTO attractions (name, category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, val)
        cnx.commit()
        
            
print ("okay") 
cnx.close()


