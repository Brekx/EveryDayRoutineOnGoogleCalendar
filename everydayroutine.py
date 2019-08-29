# coding=UTF-8
import datetime
import auth_and_send_request

def everydayroutine(service, calendarId, events):
    date = raw_input("Wprowadź dzień na który chcesz ustawić codzienną rutynę (dd-mm-yyyy)\nlub nic nie wpisuj aby wybrać jutrzejszy:\n")
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

    print("Linki do wydarzeń")

    service = auth_and_send_request.auth()
    body = {"start": {"timeZone": "Europe/Warsaw", "dateTime": "2019-08-04T13:00:00+02:00"}, "colorId": "7", "end": {"timeZone": "Europe/Warsaw", "dateTime": "2019-08-04T14:00:00+02:00"}, "location": "Dom", "summary": "Testing"}
    for event in events:
        body['summary'] = event['name']
        body['start']['dateTime'] = date + event['start']
        body['end']['dateTime'] = date + event['end']
        body['colorId'] = event['color']
        print(auth_and_send_request.send(service, body)['htmlLink'])