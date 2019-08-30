# coding=UTF-8
# Główny skrypcik trzymający wszystko w jednym miejscu
try:
    import argparse
    import time
    import datetime
    import pickle
    import os.path
    import auth_and_send_request
    import tablicakalendarzadnia
    import userContact
    import everydayroutine
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except ImportError:
    print("Lol nie masz wszystkich bibliotek")
    exit()

#informacje dla użykownika nieinteraktywnego
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-t', '--tommorow',help='fast setting tommorow events', action='store_true')
args = parser.parse_args()

if args.tommorow:
    try :
        import tablicaWydarzen
        events = tablicaWydarzen.events
        calendarId = tablicaWydarzen.calendarId
        service = auth_and_send_request.auth()
        userContact.everydayroutine(service, calendarId, events)
    except ImportError:
        userContact.tablicaWydarzenError()
    except :
        print("Wolololo ale coś pierdolnęło")
    finally:
        exit()

if not os.path.exists('tablicaWydarzen.py'):
    service = userContact.firstTime()
    print("Okeaj, mamy dostęp.")
    userContact.saveAll(userContact.calendarSelection(service), userContact.makeEvents())

service = auth_and_send_request.auth()

while(raw_input("Chciałbyś coś zmienić? T/N: ") != "N"):
    userContact.changeSomething(service)
    
try :
    import tablicaWydarzen
    events = tablicaWydarzen.events
    calendarId = tablicaWydarzen.calendarId
    userContact.everydayroutine(service, calendarId, events)
except ImportError:
    userContact.tablicaWydarzenError()
except:
    print("Wolololo ale coś pierdolnęło")
raw_input("\n\n Dzięki za wszytko!\nWciśnij enter aby kontynuaować...")
