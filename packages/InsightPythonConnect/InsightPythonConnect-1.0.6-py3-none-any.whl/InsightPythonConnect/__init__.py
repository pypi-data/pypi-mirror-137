# 31 / 01 / 22        -- WORKING -- 

from IPython.display import display, clear_output
import ipywidgets as widgets
import requests 
import json

def login():
    def clickEvent(a):
        try:
            global tokenId, appId, serverUrl, cookie, session
            session= requests.Session()
            uid = login_uid.value
            pwd = login_pwd.value
            appId = login_app_id.value
            serverUrl = login_server_url.value 
            if not (uid.strip() and pwd.strip() and appId.strip() and serverUrl.strip()):
                print('All input fields are required.')
            else:  
                formParam = {'USER_CODE': uid, 'PASSWORD': pwd, 'IS_PWD_ENCRYPT' : 'false', 'INPUT_STR' :'', 'DATA_FORMAT':'JSON', 'IS_DESTROY_SESSION':'false','APP_ID': appId }
                response = session.post(serverUrl + '/ibase/rest/E12ExtService/login?', formParam)

                if str(response.status_code) == '200':
                    cookie = response.cookies
                    status = (json.loads(response.text))['Response']['status']
                    if status == 'success':
                        clear_output()
                        print('Login Successful')
                        responseStr = (json.loads(response.text))['Response']['status'], json.loads(response.text) 
                        tokenId = json.loads((responseStr[1])['Response']['results'])['TOKEN_ID'] 
                    elif status == 'error':
                        print (json.loads(response.text)['Response']['results'])
                    else:
                        pass
        except Exception as e:
            print(e)

    login_uid = widgets.Text(value='', placeholder='Enter Username',description='Username')
    login_pwd = widgets.Password(value='',placeholder='Enter Password', description='Password')
    login_app_id = widgets.Text(value='',placeholder='Enter APPID', description='App ID')
    login_server_url = widgets.Text(value='',placeholder='Enter Server URL', description='Server Url')
    login_btn = widgets.Button(description='Login')
    display(widgets.VBox([login_uid, login_pwd, login_server_url, login_app_id, login_btn]))
    login_btn.on_click(clickEvent)

def send_request(url, formParam):
    try:
        response = session.post(url, formParam, cookies=cookie)  
        if str(response.status_code) == '200':
            status = (json.loads(response.text))['Response']['status']
            if status == 'success':
                return (json.loads(response.text))['Response']['status'], json.loads(response.text) 
            elif status == 'error':
                print (json.loads(response.text)['Response']['results'])
            else:
                pass
        else : 
            print( response.text)
    except Exception as e:
        print(e)

def getVisual(visualId, outputType=''):  
    try:
        formParam = {'VISUAL_ID': visualId, 'OUTPUT_TYPE':outputType, 'APP_ID': appId , 'TOKEN_ID':tokenId , 'DATA_FORMAT':'JSON'}
        visualData = send_request(serverUrl +'/ibase/rest/GenProcessPreviewService/getVisual?' , formParam)
        return visualData
    except NameError:
        print('Invalid Session. Please relogin and then try to access visual.')
    except Exception as e:
        print(e)
