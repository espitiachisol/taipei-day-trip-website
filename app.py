from flask import *
import mysql.connector
import json, time,secrets

app=Flask(__name__,static_folder="static", 
static_url_path="/")


app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = secrets.token_hex(16)
#connect database
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="su3cl3jo3m6@A"
)
cursor = db.cursor(buffered=True)
cursor.execute("USE taipei_web_data")
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

@app.route("/api/attractions")
def api_attractions():
	#get keyword and page query
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
		return (data,200)
		
	else:
		data={"error": True,"message": "自訂的錯誤訊息"}
		data=json.dumps(data)
		return (data,500)


@app.route("/api/attraction/<attractionId>")
def api_attraction(attractionId):
	#得到資料庫總筆數
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
			return (data,200)

		else:
			data={"error": True,"message": "自訂的錯誤訊息"}
			data=json.dumps(data)
			return (data,500)
		
	else:
		data={"error": True,"message": "自訂的錯誤訊息"}
		data=json.dumps(data)
		return (data,400)

@app.route("/api/user",methods=["GET","POST","PATCH","DELETE"])
def api_user():
	if request.method == "POST":
		username=request.json["name"]
		email=request.json["email"]
		password=request.json["password"]
		if username and email and password:
			cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
			currentUserEmail=cursor.fetchone()
			if currentUserEmail:
				return jsonify({"error": True,"message": "email重複"}),400
			else:
				print(username,email,password)
				val = (username, email, password)
				sql = "INSERT INTO users (name, email,password) VALUES (%s, %s, %s)"
				cursor.execute(sql, val)
				db.commit()
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
			 return  jsonify(data),200

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
					return jsonify({"ok": True}),200
				else:
					return jsonify({"error":True,"message": "密碼不正確"}),500
			return jsonify({"error":True,"message": "帳號或密碼不正確"}),500
		return jsonify({"error":True,"message": "輸入不完整"}),400

	elif request.method=="DELETE":
		userEmail=session.get('userEmail')
		if userEmail:
			session.pop('userEmail',None)
			return jsonify({"ok": True}),200
		else:
			return jsonify({"error":True,"message": "找不到帳號"})

@app.route("/api/booking",methods=["GET","POST","PATCH","DELETE"])
def api_booking():
	if request.method == "POST":
		userEmail=session.get('userEmail')
		if userEmail:
			attractionId=request.json["attractionId"]
			date=request.json["date"]
			time=request.json["time"]
			price=request.json["price"]
			if attractionId and date and time and price:
				val = (userEmail, attractionId, date,time,price)
				sql = "INSERT INTO orders (usermail, attractionId,date, time, price) VALUES (%s, %s, %s, %s, %s)"
				cursor.execute(sql, val)
				db.commit()
				return jsonify({"ok": True}),200

			else:
				return jsonify({"error":True,"message": "建立失敗，輸入不正確或其他原因"}),400

		else:
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}),403

	if request.method == "GET":
		userEmail=session.get('userEmail')
		if userEmail:
			 cursor.execute("SELECT * FROM orders WHERE usermail = %s ORDER BY orderId DESC",(userEmail,))
			 userOrder=cursor.fetchone()
			 if userOrder:
				 cursor.execute("SELECT * FROM attractions WHERE id = %s",(userOrder[2],))
				 userOrderattraction = cursor.fetchone()
				 images=json.loads(userOrderattraction[9])
				 data={"data":{"attraction":{"id":userOrderattraction[0],"name":userOrderattraction[1],"address":userOrderattraction[4],"image":images[0]},"date":userOrder[3],"time":userOrder[4],"price":userOrder[5]}}
				
				 print(jsonify(data))
				 return  jsonify(data),200
			 else:
				 return jsonify({"error":True,"message": "沒有您的訂購"}),500

		else:
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}),403

	if request.method == "DELETE":
		userEmail=session.get('userEmail')
		if userEmail:
			cursor.execute("DELETE FROM orders WHERE usermail = %s ",(userEmail,))
			db.commit()
			return jsonify({"ok": True}),200
		else:
			return jsonify({"error":True,"message": "未登入系統，拒絕存取"}),403
				 


if __name__=="__main__":
	app.run(host="0.0.0.0", port=3000)
	# app.run(port=3000)
db.close()
cursor.close()

