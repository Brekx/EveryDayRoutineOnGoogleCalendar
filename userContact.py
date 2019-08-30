# coding=UTF-8
#Funkcje potrzebne do działania programu


#rozpoczyna pierwszą autoryzację
def firstTime():
    print("Pierwszy raz?\nMusisz dokonać kilku rzeczy:\n   -nadać dostęp do swojego kalendarza\n   -ustalić plan dnia.\n   -wybór lub dodanie kalendarza\n\nZacznijmy od dostępu.")
    raw_input("Naciśnij enter w celu kontynuacji...")
    import auth_and_send_request
    return auth_and_send_request.auth()

#zapisuje ID kalendarza i listę eventów do wykonywalnego pliku tablicaWydarzen.py
def saveAll(calendarId, events):
    a = "# coding=UTF-8\nevents = [\n"
    for event in events:
        a += "{"
        a += "'name':'" + event['name'] + "',"
        a += "'start':'" + event['start'] + "',"
        a += "'end':'" + event['end'] + "',"
        a += "'color':'" + event['color'] + "',"
        a += "},\n"
    a += "]\ncalendarId=\"" + str(calendarId) + '\"'
    f = open('tablicaWydarzen.py', 'w')
    f.write(a)

#W przypadku problemu z plikiem tablicaWydarzen.py program usuwa i wyłącza program
def tablicaWydarzenError():
    print("Lol coś ci się z save-em crashnęło, usuwam...")
    import os.remove
    os.remove("tablicaWydarzen.py")
    exit()

#Pomaga stworzyć listę eventów, a także proponuje przykład
def makeEvents():
    number = raw_input("Wpisz liczbę wydarzeń, jeżeli chcesz skorzystać z przykładu nic nie wpisuj: ")
    if(number == ''):
        events = [{'name':'Spanko', 'start':'T23:00:00+02:00', 'end':'T23:59:00+02:00', 'color':'8'},{'name':'Spanko', 'start':'T00:00:00+02:00', 'end':'T07:00:00+02:00', 'color':'8'},{'name':'Poranne Ćwiczonka', 'start':'T07:00:00+02:00', 'end':'T07:30:00+02:00', 'color':'5'},{'name':'Modlitwa', 'start':'T22:30:00+02:00', 'end':'T23:00:00+02:00', 'color':'5'},{'name':'Śniadanko', 'start':'T7:30:00+02:00', 'end':'T08:00:00+02:00', 'color':'2'},{'name':'Obiadełko', 'start':'T14:00:00+02:00', 'end':'T15:00:00+02:00', 'color':'2'},{'name':'Kolacyjka', 'start':'T21:00:00+02:00', 'end':'T22:00:00+02:00', 'color':'2'},]
    else:
        number = int(number)
        events = []
        for i in range(number):
            nazwa = raw_input("Nazwa: ")
            godzR = raw_input("Godzina rozpoczęcia(ggmmss): ")
            godzZ = raw_input("Godzina zakonczęnia(ggmmss): ")
            color = raw_input("Id koloru(gdybyś nie znał pisz \'-1\') : ")
            while(color == '-1'):
                color = raw_input("0 - default\n1 - Lawenda (fiolet)\n2 - Szałwia (jasno zielony)\n3 - Winogrona\n4 - Flaming\n5 - Banana\n6 - Mandarynka\n7 - Paw (jasny niebieski)\n8 - Grafit\n9 - Jagoda\n10 - Bazylia (ciemno zielony)\n11 - Pomidor\n  (jeżeli dalej nie oganisz wpisz jeszcze raz \'-1\': ")
            events.append( {'name': nazwa , 'start':'T' + godzR + ':00+02:00', 'end':'T' + godzZ + ':00+02:00', 'color':'' + str(color) + ''},)
    return events

#Pomaga dokonać wyboru kalendarza
def calendarSelection(service):
    import auth_and_send_request
    a = raw_input("\n\nWybierz kalendarz.\nDodajesz czy wybierasz jeden z posiadanych?  D/W\n")
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
            calendarId = int(input("\n\nDokonałeś wyboru?\n: "))-1
            try:
                calendarId = validCalendars[calendarId]['id']
            except IndexError:
                print("Lol podaj właściwy!")
                a = not a
            a = not a
    return calendarId

#Funkcja pozwalająca na dokonanie zmian w eventach lub wybranym kalendarzu
def changeSomething(service):
    if(raw_input("Co w takim razie? Kalendarz, czy eventy? K/E  ") == 'K'):
        try:
            reload(tablicaWydarzen)
            saveAll(calendarSelection(service), tablicaWydarzen.events)
        except:
            try:
                import tablicaWydarzen
                saveAll(calendarSelection(service), tablicaWydarzen.events)
            except ImportError:
                tablicaWydarzenError()
    else:
        try:
            reload(tablicaWydarzen)
            saveAll(tablicaWydarzen.calendarId, makeEvents())
        except:
            try:
                import tablicaWydarzen
                saveAll(tablicaWydarzen.calendarId, makeEvents())
            except:
                tablicaWydarzenError()

#Funkcja pobierająca datę od użytkownika i wysyłająca złożone eventy do serverów googla
def everydayroutine(service, calendarId, events, tommorow=False):
    import datetime
    import auth_and_send_request
    if not tommorow:
        date = raw_input("Wprowadź dzień na który chcesz ustawić codzienną rutynę (dd-mm-yyyy)\nlub nic nie wpisuj aby wybrać jutrzejszy:\n")
    else:
        date = ""
    if date == "":
        print("Okej biorę jutrzejszą")
        now = datetime.datetime.now()
        date = str(now.year) + '-'

        if(now.month<10):
            date += '0' + str(now.month)
        else:
            date += str(now.month)
        date += '-'

        if(now.day+1 < 10):
            date += '0' + str(now.day+1)
        else:
            date += str(now.day+1)
        
    else:
        a = date[6] + date[7] + date[8] + date[9] + '-' + date[3] + date[4] + '-' + date[0] + date[1]
        date = a

    print("Linki do wydarzeń:")
    service = auth_and_send_request.auth()
    body = {"start": {"timeZone": "Europe/Warsaw"}, "end": {"timeZone": "Europe/Warsaw"}}
    for event in events:
        body['summary'] = event['name']
        body['start']['dateTime'] = date + event['start']
        body['end']['dateTime'] = date + event['end']
        body['colorId'] = event['color']
        print(auth_and_send_request.insertEvent(service, body, calendarId)['htmlLink'])