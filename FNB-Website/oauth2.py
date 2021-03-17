import requests

class Oauth(object):
    client_id = "815364509807280140"
    client_secret = "tVnDqywkBAvB8lQ2_yjTuDQTrHiHy1TX"
    scope = "identify%20guilds"
    redirect_url = "http://192.168.0.116:5000/finished"       #redirect uri
    discord_login_url = "https://discord.com/api/oauth2/authorize?client_id=815364509807280140&redirect_uri=http%3A%2F%2F192.168.0.116%3A5000%2Ffinished&response_type=code&scope=identify%20guilds%20guilds.join"   #redirect uri
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = 'https://discord.com/api'

    @staticmethod
    def get_access_token(code):
        payload = {
            'client_id': Oauth.client_id,
            'client_secret': Oauth.client_secret,
            'grant_type': "authorization_code",
            'code': code,
            'redirect_uri': Oauth.redirect_url,
            'scope': Oauth.scope
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        access_token = requests.post(url=Oauth.discord_token_url, data=payload,headers = headers)
        json = access_token.json()
        return json.get("access_token")
    
    @staticmethod
    def change_role(access_token):
        url = Oauth.discord_api_url + "/users/@me"

        headers = {
            "Authorization": "Bearer {}".format(access_token)
        }
    
        user_object = requests.get(url= url, headers = headers)
        user_json = user_object.json()
        return user_json
