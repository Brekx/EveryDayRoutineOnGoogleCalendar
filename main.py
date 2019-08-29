# coding=UTF-8
# Główny skrypcik trzymający wszystko w jednym miejscu
try:
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

if not os.path.exists('TablicaWydarzen.py'):
    print("Pierwszy raz?\nMusisz dokonać kilku rzeczy:\n   -nadać dostęp do swojego kalendarza\n   -ustalić plan dnia.\n   -wybór lub dodanie kalendarza\n\nZacznijmy od dostępu.")
    raw_input("Naciśnij enter w celu kontynuacji...")
    service = auth_and_send_request.auth()
    a = raw_input("\n\nOkeaj, mamy dostęp. Teraz musisz wybrać kalendarz.\nDodajesz czy wybierasz jeden z posiadanych?  D/W\n")
    if(a == 'D'):
        calendarSummary = raw_input("Mhm a jak będzie się nazywał? ")
        calendar = {
            'summary': calendarSummary,
            'timeZone': 'Europe/Warsaw'
        }
        calendarId = auth_and_send_request.insertCalendar(service, calendar)['id']
        print("Okej poszło!\nGdybyś chciał zobaczyć jego id?   " + str(calendarId))
    elif(a == 'W'):
        calendarList = auth_and_send_request.getCalendarList(service)
        validCalendars = []
        print("Okay, twoje kalendarze to:")
        for calendar in calendarList['items']:
            if(calendar['accessRole']=='owner'):
                validCalendars.append(calendar)
                print(str(len(validCalendars)) + "- " + calendar['summary'])
        a = True
        while a:
            calendarId = int(input("\n\nDokonałeś wyboru?\nJeżeli zmieniłeś zdanie wpisz \'-1\' a następnie uruchom ponownie: "))-1
            try:
                calendarId == validCalendars[calendarId]['id']
            except IndexError:
                print("Lol podaj właściwy!")
                a = not a
            a = not a
            print("\n\nOkeay, teraz pozostało zdefiniować dzień.\nJeżeli chcesz użyć templatu, jako liczbę eventów wpisz -1: ")
    tablicakalendarzadnia.saveAll(calendarId)
if(raw_input("Chciałbyś coś zmienić? T/N: ") == "T"):
    a = not True
try :
    import TablicaWydarzen
    events = TablicaWydarzen.events
    calendarId = TablicaWydarzen.calendarId
except ImportError:
    print("Lol coś ci się z save-em crashnęło, usuwam...")
    os.remove("TablicaWydarzen.py")
    exit()
try:
    service = auth_and_send_request.auth()
    everydayroutine.everydayroutine(service, calendarId, events)
except ValueError:
    print("Wolololo ale coś pierdolnęło")
raw_input("\n\n Dzięki za wszytko!\nWciśnij enter aby kontynuaować...")
