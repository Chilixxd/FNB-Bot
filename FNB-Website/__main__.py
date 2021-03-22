
from flask import Flask, request, render_template, redirect, session, send_file
from oauth2 import Oauth
import requests

app = Flask(__name__, static_folder='static', static_url_path='/static')


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/verify')
def verify():
   return render_template('verify.html')

@app.route('/finished')
def finished():

   botToken = "ODE1MzY0NTA5ODA3MjgwMTQw.YDrVXw.O0OtKNup1d3JQVSlQn0XFSk-pQY"
   code = request.args.get("code")
   discord_api_url = 'https://discord.com/api'

   access_token = Oauth.get_access_token(code)
   user_json = Oauth.change_role(access_token)

   user_id = user_json.get("id")
   user_username = user_json.get("username")
   avatar_hash = user_json.get("avatar")
   user_discrim = user_json.get("discriminator")

   headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': f"Bot {botToken}"
   }

   payload = {
      'access_token': access_token
   }

   unverified_role = "819285534890393600"
   verify_role = "816393113660555276"
   server_id = "815345103056797747"

   verify_change = discord_api_url + "/guilds/" + server_id + "/members/" + user_id + "/roles/" + verify_role

   unverified_change = discord_api_url + "/guilds/" + server_id + "/members/" + user_id + "/roles/" + unverified_role

   requests.put(url= verify_change, headers= headers, data= payload)
   requests.delete(url= unverified_change, headers= headers, data = payload)

   try:
      #user_discriminator = user_json.get("discriminator")
      user_image = "https://cdn.discordapp.com/avatars/" + user_id + "/" + avatar_hash + ".jpg"
      return render_template('finished.html', username = user_username, image = user_image) 

   except TypeError:
      x = user_discrim % 5
      if (x == 1):
         return render_template('finished.html', username = user_username, image = '/static/defaultdiscord/0.png') #avatar 0
      elif (x == 2):
         return render_template('finished.html', username = user_username, image = '/static/defaultdiscord/1.png') #avatar 1
      elif (x == 3):
         return render_template('finished.html', username = user_username, image = '/static/defaultdiscord/2.png') #avatar 2
      elif (x == 0):
         return render_template('finished.html', username = user_username, image = '/static/defaultdiscord/3.png') #avatar 3
      elif (x == 4):
         return render_template('finished.html', username = user_username, image = '/static/defaultdiscord/4.png') #avatar 4

@app.errorhandler(404)
def errorpage(e):
   return render_template('404.html')

if (__name__ == "__main__"):
   app.debug = True
   app.run(host = '192.168.0.116',port=5000)