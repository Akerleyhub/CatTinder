"""Seed to get the cat pics from the api and add it to start
    15posts are being made to start"""

#API: https://thecatapi.com/
API_BASE_URL = "https://api.thecatapi.com/v1/images"
from app import db
from models import User, Post, Rating
#from secrets import API_SECRET_KEY
import requests
from flask import request


db.drop_all()
db.create_all()

res = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res2 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res3 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res4 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res5 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res6 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res7 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res8 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res9 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res10 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res11 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res12 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res13 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res14 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
res15 = requests.get(f"{API_BASE_URL}/search", headers={"'x-api-key":API_SECRET_KEY})
data = res.json()
data2 = res2.json()
data3=res3.json()
data4=res4.json()
data5=res5.json()
data6=res6.json()
data7=res7.json()
data8=res8.json()
data9=res9.json()
data10=res10.json()
data11=res11.json()
data12=res12.json()
data13=res13.json()
data14=res14.json()
data15=res15.json()
#print(data[0]["url"])
    
#signup adds them already and encrypts ther passwords
u1 = User.signup("Synthia", "waffle", "chacha@gmail.com", "catcrazy:)", "/static/cat.jpg", "/static/background.jpg")
u2 = User.signup("Sam", "beefjermy", "channel@gmail.com", "cateatter", "/static/cat.jpg", "/static/background.jpg")
u3 = User.signup("Paul", "obama223", "ruler@gmail.com", "thebestpresident", "/static/cat.jpg", "/static/background.jpg")
u4 = User.signup("Chad", "dragonslayer123", "chadwack@gmail.com", "cats r my lyfe", "/static/cat.jpg", "/static/background.jpg")
u5 = User.signup("Abigal", "runner234", "runnergirl@gmail.com", "need cat not husband", "/static/cat.jpg", "/static/background.jpg")

db.session.commit()

p1 = Post(title = "MYCAT", text = "My silly silly cat", postimg = data[0]["url"], user_id = 1)
p2 = Post(title = "MEOW XD", text = "My fav chub cat", postimg = data2[0]["url"],user_id = 4)
p3 = Post(title = "Cat", text = "My cat is very strange", postimg = data3[0]["url"],user_id = 2)
p4 = Post(title = "Kitty", text = "My kat",postimg = data4[0]["url"], user_id = 3)
p5 = Post(title = "Tom", text = "Real life tom n jerry",postimg = data5[0]["url"], user_id = 1)
p6 = Post(title = "Datacat", text = "Cats ate my data",postimg = data6[0]["url"], user_id = 1)
p7 = Post(title = "RAWR", text = "Better watch out for this cranky lady",postimg = data7[0]["url"], user_id = 1)
p8 = Post(title = "Lisp", text = "pspsspspsppspspspspsspsps",postimg = data8[0]["url"], user_id = 1)
p9 = Post(title = "Friskys", text = "My cat love friskys food",postimg = data9[0]["url"], user_id = 1)
p10 = Post(title = "Househog", text = "Lorem ipsum",postimg = data11[0]["url"], user_id = 1)
p11 = Post(title = "Ruffle", text = "Galhode zonde forma",postimg = data12[0]["url"], user_id = 5)
p12 = Post(title = "Blueberry", text = "Meato de gleetyo",postimg = data13[0]["url"], user_id = 5)
p13 = Post(title = "Zhang", text = "Rawrrawrmeowroar",postimg = data14[0]["url"], user_id = 5)
p14 = Post(title = "Mrs.Kitty", text = "KaneKat",postimg = data15[0]["url"], user_id = 2)
p15 = Post(title = "Glactic version", text = "Meowth pokemon",postimg = data10[0]["url"], user_id = 3)

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(p6)
db.session.add(p7)
db.session.add(p8)
db.session.add(p9)
db.session.add(p10)
db.session.add(p11)
db.session.add(p12)
db.session.add(p13)
db.session.add(p14)
db.session.add(p15)

db.session.commit()


r = Rating(like = 1, dislike = None, comment = None, user_idd = 1, post_idd = 2)
r2 = Rating(like = 1, dislike = None, comment = None, user_idd = 2, post_idd = 4)
r3 = Rating(like = 1, dislike = None, comment = None, user_idd = 2, post_idd = 8)
r4 = Rating(like = None, dislike = 1, comment = None, user_idd = 3, post_idd = 5)

db.session.add(r)
db.session.add(r2)
db.session.add(r3)
db.session.add(r4)
db.session.commit()