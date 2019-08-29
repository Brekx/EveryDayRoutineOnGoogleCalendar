# coding=UTF-8
def saveAll(calendarId):
    number = int(raw_input())
    if(number == -1):
        a = "# coding=UTF-8\nevents = [\n{'name':'Spanko', 'start':'T23:00:00+02:00', 'end':'T23:59:00+02:00', 'color':'0'},\n{'name':'Spanko', 'start':'T00:00:00+02:00', 'end':'T07:00:00+02:00', 'color':'0'},\n{'name':'Poranne Ćwiczonka', 'start':'T07:00:00+02:00', 'end':'T07:30:00+02:00', 'color':'5'},\n{'name':'Modlitwa', 'start':'T22:30:00+02:00', 'end':'T23:00:00+02:00', 'color':'5'},\n{'name':'Śniadanko', 'start':'T7:30:00+02:00', 'end':'T08:00:00+02:00', 'color':'2'},\n{'name':'Obiadełko', 'start':'T14:00:00+02:00', 'end':'T15:00:00+02:00', 'color':'2'},\n{'name':'Kolacyjka', 'start':'T21:00:00+02:00', 'end':'T22:00:00+02:00', 'color':'2'},]"
    else:
        a = "# coding=UTF-8\nevents = [\n"
        nazwa = " "
        godzR = " "
        godzZ = " "
        color = " "
        for i in range(number):
            nazwa = raw_input("Nazwa: ")
            godzR = raw_input("Godzina rozpoczęcia(ggmmss): ")
            godzZ = raw_input("Godzina zakonczęnia(ggmmss): ")
            color = raw_input("Id koloru(gdybyś nie znał pisz \'-1\') : ")
            while(color == '-1'):
                color = raw_input("0 - default\n1 - Lawenda (fiolet)\n2 - Szałwia (jasno zielony)\n3 - Winogrona\n4 - Flaming\n5 - Banana\n6 - Mandarynka\n7 - Paw (jasny niebieski)\n8 - Grafit\n9 - Jagoda\n10 - Bazylia (ciemno zielony)\n11 - Pomidor\n  (jeżeli dalej nie oganisz wpisz jeszcze raz \'-1\': ")
            a += '{\'name\':\'' + nazwa + '\', \'start\':\'T' + godzR + ':00+02:00\', \'end\':\'T' + godzZ + ':00+02:00\', \'color\':\'' + str(color) + '\'},\n'
        a += ']\n'
    a += '\ncalendarId = ' + str(calendarId)
    f = open('tablicaWydarzen.py', 'w')
    f.write(a)