import re
import pickle
import deepdiff
import requests
import datetime
from download import *
from urllib.request import urlopen


def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def webhook():
    weburl = ""

    url = "<your url>" #webhook url, from here: https://i.imgur.com/f9XnAew.png

    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        "content" : "RFB Atualizada! Iniciando Download.",
        "username" : "Receita Bot"
    }

    result = requests.post(weburl, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def verifica():

    URL_BASE_RFB = 'http://200.152.38.155/CNPJ/'

    data = str(urlopen(URL_BASE_RFB).read(), encoding='utf8')

    # Pega todas as urls
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', data)

    dates = re.findall("[0-9]{1,4}[\_|\-|\/|\|][0-9]{1,2}[\_|\-|\/|\|][0-9]{1,4}", data)

    parsed = dict(list(zip(urls,dates)))

    urls = {url:date for (url,date) in parsed.items() if url.endswith('.zip')}

    lista = load_obj(name='data')

    result = deepdiff.DeepDiff(urls,lista)

    if result != {}:
        webhook()
        start_threads(path='../download/{}'.format(datetime.datetime.now()))
        save_obj(urls, name='data')


if __name__ == '__main__':
     verifica()
