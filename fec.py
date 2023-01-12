import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from clint.textui import colored, puts
from tqdm import *
import re
import time
from datetime import timedelta, datetime, tzinfo, timezone
import sys
import pytz
import json
import os
    
def unixTime():
    dt = datetime.now(tz=pytz.utc)
    return str(int(dt.timestamp() * 1000))


#start
try:
    if len(sys.argv) < 8:
        print('Utilizzo: fec.py(fec.exe) CodiceFiscale/CodiceEntratel PIN Password PartitaIVA DataDal DataAl FOL/ENT')
        print('Esempio: MRNNCC65P05G273H 797182834 MySecrePwd 04454850823 01012023 31012023 FOL')
        sys.exit()
        
    CF = sys.argv[1]
    PIN = sys.argv[2]
    Password  = sys.argv[3]
    PIVA  = sys.argv[4]
    Dal = sys.argv[5]
    Al = sys.argv[6]
    Tipo = sys.argv[7]

    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'})
    s.headers.update({'Connection': 'keep-alive'})

    cookie_obj1 = requests.cookies.create_cookie(domain='ivaservizi.agenziaentrate.gov.it',name='LFR_SESSION_STATE_20159',value=unixTime())
    s.cookies.set_cookie(cookie_obj1)
    cookie_obj2 = requests.cookies.create_cookie(domain='ivaservizi.agenziaentrate.gov.it',name='LFR_SESSION_STATE_10811916',value=unixTime())
    s.cookies.set_cookie(cookie_obj2)
    r = s.get('https://ivaservizi.agenziaentrate.gov.it/portale/web/guest', verify=False)

    if r.status_code == 200:
        puts(colored.yellow('Collegamento alla homepage. Avvio.'))
    else:
        puts(colored.red('Collegamento alla homepage non riuscito: uscita.'))
        sys.exit()
    
    cookieJar = s.cookies

    print('Effettuo il login')
    payload = {'_58_saveLastPath': 'false', '_58_redirect' : '', '_58_doActionAfterLogin': 'false', '_58_login': CF , '_58_pin': PIN, '_58_password': Password}    
    r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/home?p_p_id=58&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=3&p_p_col_count=4&_58_struts_action=%2Flogin%2Flogin', data=payload)
    cookieJar = s.cookies

    liferay = re.findall(r"Liferay.authToken = '.*';", r.text)[0]
    p_auth = liferay.replace("Liferay.authToken = '","")
    p_auth = p_auth.replace("';", "")

    r = s.get('https://ivaservizi.agenziaentrate.gov.it/dp/api?v=' + unixTime())

    if r.status_code == 200:
        puts(colored.yellow('Login riuscito.'))
    else:
        puts(colored.red('Login non riuscito: uscita.')) 
        sys.exit()

    cookieJar = s.cookies
    
    if Tipo == "FOL":
        accesso = "-FOL"
    elif Tipo == "ENT":
        accesso = "-000"
    else:
        puts(colored.red('Tipo incarico deve essere FOL per FiscoOnLine e ENT per Entratel: uscita.')) 
        sys.exit()
 
    print('Seleziono il tipo di incarico per la PIVA ' + PIVA)
    payload = {'sceltaincarico': PIVA + accesso, 'tipoincaricante' : 'incDiretto'}    
    r = s.post('https://ivaservizi.agenziaentrate.gov.it/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=incarichiAction', data=payload)

    if r.status_code == 200:
        puts(colored.yellow('Selezione incarico riuscita.'))
    else:
        puts(colored.red('Selezione incarico non riuscita: uscita.')) 
        sys.exit()

                           
    print('Aderisco al servizio')
    r = s.get('https://ivaservizi.agenziaentrate.gov.it/ser/api/fatture/v1/ul/me/adesione/stato/')

    if r.status_code == 200:
        puts(colored.yellow('Adesione riuscita ai servizi AdE.'))
    else:
        puts(colored.red('Adesione ai servizi AdE non riuscita: uscita.')) 
        sys.exit()

    cookieJar = s.cookies


    headers_token = {'x-xss-protection': '1; mode=block',
           'strict-transport-security': 'max-age=16070400; includeSubDomains',
           'x-content-type-options': 'nosniff',
           'x-frame-options': 'deny'}
    r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/sc/tokenB2BCookie/get?v='+unixTime() , headers = headers_token )

    if r.status_code == 200:
        puts(colored.yellow('B2B Cookie ottenuto'))
    else:
        puts(colored.red('B2B Cookie non ottenuto: uscita.')) 
        sys.exit()

    cookieJar = s.cookies
    tokens = r.headers

    xb2bcookie = r.headers.get('x-b2bcookie')
    xtoken = r.headers.get('x-token')
 

    s.headers.update({'Host': 'ivaservizi.agenziaentrate.gov.it'})
    s.headers.update({'Referer': 'https://ivaservizi.agenziaentrate.gov.it/cons/cons-web/?v=' + unixTime()})
    s.headers.update({'Accept': 'application/json, text/plain, */*'})
    s.headers.update({'Accept-Encoding': 'gzip, deflate, br'})
    s.headers.update({'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6'})
    s.headers.update({'DNT': '1'})
    s.headers.update({'X-XSS-Protection': '1; mode=block'})
    s.headers.update({'Strict-Transport-Security': 'max-age=16070400; includeSubDomains'})
    s.headers.update({'X-Content-Type-Options': 'nosniff'})
    s.headers.update({'X-Frame-Options': 'deny'})
    s.headers.update({'x-b2bcookie': xb2bcookie})
    s.headers.update({'x-token': xtoken})

    headers = {'Host': 'ivaservizi.agenziaentrate.gov.it',
           'referer': 'https://ivaservizi.agenziaentrate.gov.it/cons/cons-web/?v=' + unixTime(),
           'accept': 'application/json, text/plain, */*',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
           'DNT': '1',
           'x-xss-protection': '1; mode=block',
           'strict-transport-security': 'max-age=16070400; includeSubDomains',
           'x-content-type-options': 'nosniff',
           'x-frame-options': 'deny',
           'x-b2bcookie': xb2bcookie,
           'x-token': xtoken,
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}


    cookieJar = s.cookies

    print('Scarico la lista (json) delle fatture ricevute.')
    r = s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/fe/ricevute/dal/'+Dal+'/al/'+Al+'/ricerca/ricezione?v=' + unixTime(), headers = headers)

    if r.status_code == 200:
        puts(colored.yellow('Lista ottenuta.'))
    else:
        puts(colored.red('Lista non ottenuta: uscita.')) 
        sys.exit()


    with open('fe_ricevute_' + PIVA + '.json', 'wb') as f:
        f.write(r.content)
 
    
    path = r'Ricevute_' + PIVA
    if not os.path.exists(path):
        os.makedirs(path)
    with open('fe_ricevute_'+ PIVA +'.json') as data_file:    
        data = json.load(data_file)
        print('Inizio a scaricare ' + str(data['totaleFatture']) + ' fatture dal ' + data['dataRicercaDa'] + ' al ' + data['dataRicercaA'] + ' per un massimo di ' + str(data['limiteBloccoTotaleFatture']) + ' fatture scaricabili.')
        for fattura in data['fatture']:
            fatturaFile = fattura['tipoInvio']+fattura['idFattura']
            with s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/fatture/file/'+fatturaFile+'?tipoFile=FILE_FATTURA&download=1&v='+unixTime(), headers = headers_token , stream = True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                d = r.headers['content-disposition']
                fname = re.findall("filename=(.+)", d)
                with open(path + '/' + fname[0], 'wb') as f:
                    pbar = tqdm(total=total_size, unit='B', unit_divisor=1024, unit_scale=True, ascii=True)
                    pbar.set_description('Scaricando ' + fname[0])
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  
                            f.write(chunk)
                            pbar.update(len(chunk))
                    pbar.close()
            with s.get('https://ivaservizi.agenziaentrate.gov.it/cons/cons-services/rs/fatture/file/'+fatturaFile+'?tipoFile=FILE_METADATI&download=1&v='+unixTime(), headers = headers_token , stream = True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                d = r.headers['content-disposition']
                fname = re.findall("filename=(.+)", d)
                with open(path + '/' + fname[0], 'wb') as f:
                    pbar = tqdm(total=total_size, unit='B', unit_divisor=1024, unit_scale=True, ascii=True)
                    pbar.set_description('Scaricando ' + fname[0])
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  
                            f.write(chunk)
                            pbar.update(len(chunk))
                    pbar.close()                
except KeyboardInterrupt:
       print("Programma terminato manualmente!")
       sys.exit()
#end            
sys.exit()
