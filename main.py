from flask import Flask,request,json,abort
import requests
from config import webhook_url,  flask_ip, flask_port, errors_route

app = Flask(__name__)

def remove_newlines(str):
    return(str.replace('\n', '\\n'))

@app.route(f'/{errors_route}', methods = ['POST'])
def post_glua_error():
    if request.method == 'POST':
        received_data = request.form.to_dict()
        to_post = f'''{{ "content": null,
                          "embeds": [
                            {{
                              "title": "{("Serverside" if received_data['realm'] == 'server' else "Clientside") + " error"}" ,
                              "color": 14648832,
                              "fields": [
                                {{
                                  "name": "Error:",
                                  "value": "{remove_newlines(received_data['error'])}"
                                }},
                                {{
                                  "name": "Stack trace:",
                                  "value": "{remove_newlines(received_data['stack'])}"
                                }},
                                {{
                                  "name": "Gamemode",
                                  "value": "{received_data['gamemode']}",
                                  "inline": true
                                }},
                                {{
                                  "name": "GM version",
                                  "value": "{received_data['gmv']}",
                                  "inline": true
                                }},
                                {{
                                  "name": "Addon workshop id",
                                  "value": "{received_data['addon']}",
                                  "inline": true
                                }}
                              ],
                              "footer": {{
                                "text": "{received_data['os'] + ' | ' + received_data['hash']}"
                              }}
                            }}
                          ],
                          "username": "Something is creating script errors",
                          "avatar_url": "https://i.redd.it/a5iykyxq3e341.jpg"
                        }}'''
        requests.post(webhook_url, json = json.loads(to_post))
        return 'success', 200
    else:
        abort(400)

app.run(host=flask_ip, port=flask_port)


