
import pandas as pd
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json



def get_date():

    input_date = datetime.now()
    input_date = input_date.strftime("%Y-%m-%d")

    return input_date

def request_wapi(api_key,query):

    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try :
        response = requests.get(url_clima).json()
    except Exception as e:
        print(e)

    return response

def get_forecast(response,i):
  fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
  hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
  condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
  temperatura = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
  lluvia = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
  probabilidad_lluvia = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

  return fecha, hora, condicion, temperatura, lluvia, probabilidad_lluvia

def create_df(data):

    col = ['Fecha','Hora','Condicion','Temperatura','Lluvia','Probabilidad lluvia']
    df = pd.DataFrame(data,columns=col)
    df = df.sort_values(by = 'Hora',ascending = True)

    df_lluvia = df[(df['Hora']>5) & (df['Hora']<23)]
    df_lluvia = df_lluvia[['Hora', 'Condicion','Temperatura']]
    #df_lluvia = pd.DataFrame(df_lluvia)
    df_lluvia.set_index('Hora', inplace=True)

    return df_lluvia

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df_lluvia,query):

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body='\nHola! \n\n\n El pronostico del tiempo hoy '+ input_date +' en ' + query +' es : \n\n\n ' + str(df_lluvia),
                        from_=PHONE_NUMBER,
                        to=''
                    )

    return message.sid
