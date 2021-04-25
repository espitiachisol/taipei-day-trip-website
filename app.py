from flask import *
import mysql.connector
import json
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["DEBUG"] = True

#connect database
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="su3cl3jo3m6"
)
cursor = db.cursor(buffered=True)
cursor.execute("USE taipei_web_data")
#attractions count 
cursor.execute("SELECT COUNT(id) FROM attractions")
attractions_counts= cursor.fetchone()

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
		keyword_data=[]
		page_keyword_data=[]
		page_data=[]
		if keyword:
			cursor.execute(f"SELECT * FROM attractions WHERE category LIKE '%{keyword}%'")
			category=cursor.fetchall()
			if(len(category)-(page*12+12))>0:
				nextPage=page+1
			else:
				nextPage=None

			for each_category in category:
				# print(each_category)
				images=json.loads(each_category[9])
				each_data={
				"id":each_category[0],
				"name":each_category[1],
				"category":each_category[2],
				"description":each_category[3],
				"address":each_category[4],
				"transport":each_category[5],
				"mrt":each_category[6],
				"latitude":each_category[7],
				"longitude":each_category[8],
				"images":images}
				# print(each_data)
				keyword_data.append(each_data)
			
			if(len(category)-(page*12))<12:
				for i in range(page*12,page*12+(len(category)-(page*12))):
					page_keyword_data.append(keyword_data[i])
			else:
				for i in range(page*12,page*12+11+1):
					page_keyword_data.append(keyword_data[i])
			print(len(keyword_data))
		else:
			cursor.execute(f"SELECT * FROM attractions")
			category=cursor.fetchall()
			if(len(category)-(page*12+12))>0:
				nextPage=page+1
			else:
				nextPage=None
			
			for each_category in category:
				images=json.loads(each_category[9])
				each_data={
				"id":each_category[0],
				"name":each_category[1],
				"category":each_category[2],
				"description":each_category[3],
				"address":each_category[4],
				"transport":each_category[5],
				"mrt":each_category[6],
				"latitude":each_category[7],
				"longitude":each_category[8],
				"images":images}
				page_data.append(each_data)
				
			if(len(category)-(page*12))<12:
				for i in range(page*12,page*12+(len(category)-(page*12))):
					page_keyword_data.append(page_data[i])
			else:
				for i in range(page*12,page*12+11+1):
					page_keyword_data.append(page_data[i])

		#return json format data
		data={"nextPage": nextPage,
		"data":page_keyword_data
		}
		data=json.dumps(data)
		return (data,200)

	else:
		data={"error": True,"message": "自訂的錯誤訊息"}
		data=json.dumps(data)
		return (data,500)


@app.route("/api/attraction/<attractionId>")
def api_attraction(attractionId):
	
	if attractionId.isnumeric() and (int(attractionId)<attractions_counts[0]): 
		cursor.execute(f"SELECT * FROM attractions WHERE id={attractionId}")
		api_attraction=cursor.fetchone()
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
			data=json.dumps(data)
			# print(api_attraction)
			
			return (data,200)
		else:
			data={"error": True,"message": "自訂的錯誤訊息"}
			data=json.dumps(data)
			return (data,500)
		
	else:
		data={"error": True,"message": "自訂的錯誤訊息"}
		data=json.dumps(data)
		return (data,400)


if __name__=="__main__":
	app.run(host="0.0.0.0", port=3000)





