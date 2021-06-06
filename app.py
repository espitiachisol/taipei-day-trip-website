from flask import *
import mysql.connector
import json, time,secrets,os
import requests, random
from datetime import datetime
from mysql.connector import pooling
from dotenv import load_dotenv

app=Flask(__name__,static_folder="static", 
static_url_path="/")
load_dotenv()
PASSWORD=os.getenv("PASSWORD")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = secrets.token_hex(16)
#connect database
dbconfig = {
   "host":"localhost",
    "user":"root",
	"database":"taipei_web_data",
    "password":PASSWORD,
    "buffered":True
}
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 5,
                                                      **dbconfig)
                                             


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
@app.route("/member")
def member():
	return render_template("member.html")

@app.route("/api/attractions")
def api_attractions():
	#get keyword and page query
	cnx= cnxpool.get_connection()
	cursor = cnx.cursor()
	keyword=request.args.get("keyword")
	page=request.args.get("page")
	if page:
		page=int(page)
		nextPage=0
		result=[]
		#輸入keyword和page的判斷	
		if keyword:
			#根據所在page得到資料庫的十二筆資料
			cursor.execute(f"SELECT * FROM attractions WHERE name LIKE '%{keyword}%' ORDER BY id LIMIT {page*12},12")
			matched_data=cursor.fetchall()
			#得到資料庫總筆數
			cursor.execute(f"SELECT COUNT(id) FROM attractions WHERE name LIKE '%{keyword}%'")
			attractions_counts= cursor.fetchone()

		#只有輸入Page的判斷	
		else: 
			#根據所在page得到資料庫的十二筆資料
			cursor.execute(f"SELECT * FROM attractions ORDER BY id LIMIT {page*12},12")
			matched_data=cursor.fetchall()
			#得到資料庫總筆數
			cursor.execute("SELECT COUNT(id) FROM attractions")
			attractions_counts= cursor.fetchone()
		#nextpage判斷
		if(attractions_counts[0]-(page*12+12))>0:
			nextPage=page+1
		else:
			nextPage=None
		#將得到資料放入json格式資料
		for each_matched_data in matched_data:
			images=json.loads(each_matched_data[9])
			each_matched_data={
			"id":each_matched_data[0],
			"name":each_matched_data[1],
			"category":each_matched_data[2],
			"description":each_matched_data[3],
			"address":each_matched_data[4],
			"transport":each_matched_data[5],
			"mrt":each_matched_data[6],
			"latitude":each_matched_data[7],
			"longitude":each_matched_data[8],
			"images":images}
			# print(each_matched_data)
			result.append(each_matched_data)
			
		#回傳json格式
		data={"nextPage": nextPage,"data":result}
		data=json.dumps(data)
		cnx.close()
		return (data,200)
		
	else:
		data={"error": True,"message": "自訂的錯誤訊息"}
		data=json.dumps(data)
		cnx.close()
		return (data,500)

	


@app.route("/api/attraction/<attractionId>")
def api_attraction(attractionId):
	#得到資料庫總筆數
	cnx= cnxpool.get_connection()
	cursor = cnx.cursor()
	cursor.execute("SELECT COUNT(id) FROM attractions")
	attractions_counts= cursor.fetchone()
	
	if attractionId.isnumeric() and (int(attractionId)<attractions_counts[0]): 
		cursor.execute(f"SELECT * FROM attractions WHERE id={attractionId}")
		api_attraction=cursor.fetchone()
		#將得到資料放入json格式資料
		if api_attraction:
			images=json.loads(api_attraction[9])
			data={
			"data":{
				"id":api_attraction[0],
				"name":api_attraction[1],
				"category":api_attraction[2],
				"description":api_attraction[3],
				"address":api_attraction[4],
				"transport":api_attraction[5],
				"mrt":api_attraction[6],
				"latitude":api_attraction[7],
				"longitude":api_attraction[8],
				"images":images}
			}
			#回傳json格式
			data=json.dumps(data)
			cnx.close()
			return (data,200)

		else:
			data={"error": True,"message": "自訂的錯誤訊息"}
			data=json.dumps(data)
			cnx.close()
			return (data,500)
		
	else:
		data={"error": True,"message": "自訂的錯誤訊息"}
		data=json.dumps(data)
		cnx.close()
		return (data,400)

@app.route("/api/user",methods=["GET","POST","PATCH","DELETE"])
def api_user():
	cnx= cnxpool.get_connection()
	cursor = cnx.cursor()
	if request.method == "POST":
		username=request.json["name"]
		email=request.json["email"]
		password=request.json["password"]
		if username and email and password:
			cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
			currentUserEmail=cursor.fetchone()
			if currentUserEmail:
				cnx.close()
				return jsonify({"error": True,"message": "email重複"}),400
			else:
				print(username,email,password)
				val = (username, email, password)
				sql = "INSERT INTO users (name, email,password) VALUES (%s, %s, %s)"
				cursor.execute(sql, val)
				cnx.commit()
				cnx.close()
				return jsonify({"ok": True}),200

		return jsonify({"error": True,"message": "輸入不完整"}),400

	elif request.method =="GET":
		 userEmail=session.get('userEmail')
		 if userEmail:
			 cursor.execute("SELECT * FROM users WHERE email = %s",(userEmail,))
			 currentUserEmail=cursor.fetchone()
			 data={"data":
			 {"id":currentUserEmail[0],
			 "name":currentUserEmail[1],"email":currentUserEmail[2]}}
			 print(data)
			 cnx.close()
			 return  jsonify(data),200
			 
			
		 cnx.close()
		 return jsonify({"data":None}),200
		 
		

	elif request.method=="PATCH":
		email=request.json["email"]
		password=request.json["password"]
		if email and password:
			cursor.execute("SELECT email FROM users WHERE email = %s",(email,))
			currentUserEmail = cursor.fetchone()
			if currentUserEmail:
				cursor.execute("SELECT * FROM users WHERE email = %s and password = %s",(email, password))
				currentUser = cursor.fetchone()
				if currentUser:
					session['userEmail']=email
					cnx.close()
					return jsonify({"ok": True}),200
				else:
					cnx.close()
					return jsonify({"error":True,"message": "密碼不正確"}),500
			cnx.close()
			return jsonify({"error":True,"message": "帳號或密碼不正確"}),500
		cnx.close()
		return jsonify({"error":True,"message": "輸入不完整"}),400

	elif request.method=="DELETE":
		userEmail=session.get('userEmail')
		if userEmail:
			session.pop('userEmail',None)
			cnx.close()
			return jsonify({"ok": True}),200
		else:
			cnx.close()
			return jsonify({"error":True,"message": "找不到帳號"})

@app.route("/api/booking",methods=["GET","POST","PATCH","DELETE"])
def api_booking():
	cnx= cnxpool.get_connection()
	cursor = cnx.cursor()
	if request.method == "POST":
		userEmail=session.get('userEmail')
		if userEmail:
			attractionId=request.json["attractionId"]
			date=request.json["date"]
			time=request.json["time"]
			price=request.json["price"]
			if attractionId and date and time and price:
				val = (userEmail, attractionId, date,time,price,0)
				sql = "INSERT INTO orders (usermail, attractionId,date, time, price) VALUES (%s, %s, %s, %s, %s)"
				cursor.execute(sql, val)
				cnx.commit()
				cnx.close()
				return jsonify({"ok": True}),200

			else:
				cnx.close()
				return jsonify({"error":True,"message": "建立失敗，輸入不正確或其他原因"}),400

		else:
			cnx.close()
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}),403

	if request.method == "GET":
		userEmail=session.get('userEmail')
		if userEmail:
			 cursor.execute("SELECT * FROM orders WHERE usermail = %s ORDER BY orderId DESC LIMIT 1",(userEmail,))
			 userOrder=cursor.fetchone()
			 if userOrder:
				 cursor.execute("SELECT * FROM attractions WHERE id = %s",(userOrder[2],))
				 userOrderattraction = cursor.fetchone()
				 images=json.loads(userOrderattraction[9])
				 data={"data":{"attraction":{"id":userOrderattraction[0],"name":userOrderattraction[1],"address":userOrderattraction[4],"image":images[0]},"date":userOrder[3],"time":userOrder[4],"price":userOrder[5]}}
				
				 print(jsonify(data))
				 cnx.close()
				 return  jsonify(data),200
			 else:
				 cnx.close()
				 return jsonify({"error":True,"message": "沒有您的訂購"}),500

		else:
			cnx.close()
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}),403

	if request.method == "DELETE":
		userEmail=session.get('userEmail')
		if userEmail:
			cursor.execute("DELETE FROM orders WHERE usermail = %s ",(userEmail,))
			cnx.commit()
			cnx.close()
			return jsonify({"ok": True}),200
		else:
			cnx.close()
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}),403
				 

@app.route("/api/orders",methods=["POST","GET"])
def api_orders():
	cnx= cnxpool.get_connection()
	cursor = cnx.cursor()
	if request.method == "GET":
		result=[]
		userEmail=session.get('userEmail')
		if userEmail:
			cursor.execute("SELECT * FROM payStatus WHERE usermail = %s AND status=  %s ORDER BY payStatusId DESC LIMIT 3 ",(userEmail,0,))
			dataFromPayStatus=cursor.fetchall()
			if dataFromPayStatus:
				for eachData in dataFromPayStatus:
					cursor.execute("SELECT attractions.id,attractions.name,attractions.images FROM payStatus INNER JOIN attractions ON payStatus.attractionId=attractions.id WHERE attractionId =%s",(eachData[7],))
					dataFromAttractionId=cursor.fetchone()
					images=json.loads( dataFromAttractionId[2])
					data={"data": {
						"number": eachData[1],
						"attraction": {
							"name": dataFromAttractionId[1],"image":images[0]},
						"date": eachData[8]},
						}
					result.append(data)
					print(result)
				cnx.close()
				return jsonify(result),200
			else:
				data={"error": True,"message": "沒有資料"}
				cnx.close()
				return jsonify(data),500
			
		else:
			cnx.close()
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}),403 	


	if request.method == "POST":
		userEmail=session.get('userEmail')
		if userEmail:
			dataFromFront=request.json
			contactPhone=dataFromFront["order"]["contact"]["phone"]
			contactname=dataFromFront["order"]["contact"]["name"]
			contactEmail=dataFromFront["order"]["contact"]["email"]
			prime=dataFromFront["prime"]
			attractionId=dataFromFront["order"]["trip"]["attraction"]["id"]
			date=dataFromFront["order"]["trip"]["date"]
			time=dataFromFront["order"]["trip"]["time"]
			price=dataFromFront["order"]["price"]
			if contactPhone and contactname and contactEmail and prime:
	
				#insert data to databese
				OrderNumber=giveOrderNumber();
				val = (OrderNumber, 1, contactname,contactEmail,contactPhone,userEmail,attractionId,date,time,price)
				sql = "INSERT INTO payStatus(orderNumber, status,contactName, contactMail, contactphone,usermail,attractionId,date,time,price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, val)
				cnx.commit()

				#send data to tappay
				partnerKey="partner_aGYmA1y9p7cqFyTL16ek0KsTjNkoFEsO7Xgo6DmodSkP4XB7oiuzwYl1"
				url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
				dataToTappay={"prime": prime,
				"partner_key": partnerKey,
				"merchant_id": 'chijo3m6_CTBC',
				"details":"TapPay Test",
				"amount": 1,
				"cardholder": {
					"phone_number": contactPhone,
					"name": contactname,
					"email": contactEmail,
					},
				}
				headers = {
					"Content-Type": "application/json",
					"x-api-key":partnerKey
				}
				r = requests.post(url,headers=headers,json=dataToTappay)
				dataGetFromTappay = r.json()
				print(dataGetFromTappay)
				if dataGetFromTappay['status']==0:
					message="付款成功"
					status=0
					cursor.execute("UPDATE payStatus SET status=0 WHERE orderNumber = %s",(OrderNumber,))
					cnx.commit()
				else:
					status=1
					message="付款失敗"

				dataToFront={"data":
				{"number":OrderNumber,
				"payment":{"status": status,"message": message}}
				}
				cnx.close()
				return  jsonify(dataToFront),200

			else:
				cnx.close()
				return jsonify({"error":True,"message": "訂單建立失敗，輸入不正確或其他原因"}),400
		else:
			cnx.close()
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}),403 	
	else:
		cnx.close()
		return jsonify({"error":True,"message": "伺服器內部錯誤"}),500

@app.route("/api/order/<orderNumber>")
def api_order(orderNumber):
	cnx= cnxpool.get_connection()
	cursor = cnx.cursor()
	if request.method == "GET":
		userEmail=session.get('userEmail')
		if userEmail:
			cursor.execute("SELECT * FROM payStatus WHERE orderNumber = %s",(orderNumber,))
			dataFromPayStatus=cursor.fetchone()
			if dataFromPayStatus:
				cursor.execute("SELECT attractions.id,attractions.name,attractions.address,attractions.images FROM payStatus INNER JOIN attractions ON payStatus.attractionId=attractions.id WHERE attractionId =%s",(dataFromPayStatus[7],))
				dataFromAttractionId=cursor.fetchone()
				images=json.loads( dataFromAttractionId[3])
				data={"data": {
					"number": dataFromPayStatus[1],
					"price": dataFromPayStatus[10],
					"trip": {
						"attraction": {
							"id": dataFromAttractionId[0],
							"name": dataFromAttractionId[1],
							"address": dataFromAttractionId[2],
							"image":images[0]},
						"date": dataFromPayStatus[8],
						"time": dataFromPayStatus[9]},
					"contact": {
						"name": dataFromPayStatus[3],
						"email": dataFromPayStatus[4],
						"phone": dataFromPayStatus[5],
						},
					"status": dataFromPayStatus[2]}
					}
				print(data)
				cnx.close()
				return jsonify(data),200

			else:
				cnx.close()
				return jsonify({"error":True,"message": "無此訂單"}),400
		else:
			cnx.close()
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}),403


def giveOrderNumber():
	cnx= cnxpool.get_connection()
	cursor = cnx.cursor()
	today=datetime.today().strftime('%Y%m%d')
	randomSixEndNum=random.randrange(100000, 999999, 6) 
	orderNumber=today+str(randomSixEndNum)
	cursor.execute("SELECT * FROM payStatus WHERE orderNumber = %s",(orderNumber,))
	repeat=cursor.fetchone()
	if repeat:
		giveOrderNumber()
	else:
		cnx.close()
		return orderNumber

if __name__=="__main__":
	app.run(host="0.0.0.0", port=3000)
	

