from plyer import notification
import requests
import socket
from bs4 import BeautifulSoup
import time


def getData(url):
    '''for getting data from url'''
    r=requests.get(url)
    return  r.text

def convert(sub_li):
    '''This is used to convert string to integer of numerical data'''
    l = len(sub_li)
    m=len(sub_li[0])
    for i in range(0, l):
        for j in range(0, m):
            if j in range(1,m):
                if sub_li[i][j].isnumeric():
                    sub_li[i][j]=int(sub_li[i][j])
    return sub_li

def Sort(sub_li):
    '''to sort the list of list of cases of various states according to their no. of confirmed cases '''

    convert(sub_li)
    sub_li.sort(key=lambda x: x[1])
    return sub_li

def createDict(sub_list):
    '''To create dictionary of cases of each states'''

    dictStates={}
    for i in range(len(sub_list)-1,-1,-1):
        dictStates[sub_list[i][0]]=[sub_list[i][1],sub_list[i][2],sub_list[i][3]]

    return dictStates

def notifyMe(dictStates,listStates,yourState):
    '''To display the notification'''

    title1="COVID-19 cases (Top state)"
    message1=f"State: {listStates[len(listStates)-1][0]}\n" \
        f"Confirmed: {listStates[len(listStates)-1][1]}\n" \
        f"Recovered: {listStates[len(listStates)-1][2]}\n" \
        f"Deaths: {listStates[len(listStates)-1][3]}\n\n" \

    notification.notify(
        title=title1,
        message=message1,
        app_icon="icon.ico",
        timeout=15)

    title2="COVID-19 cases (My state)"
    message2 = f"Your State: {yourState}\n" \
        f"Confirmed: {dictStates[yourState][0]}\n" \
        f"Recovered: {dictStates[yourState][1]}\n" \
        f"Deaths: {dictStates[yourState][2]}"

    notification.notify(
        title=title2,
        message=message2,
        app_icon="icon.ico",
        timeout=15)


if __name__=='__main__':

    IPaddress = socket.gethostbyname(socket.gethostname())
    if IPaddress == "127.0.0.1":
        notification.notify(
            title="No Internet",
            message="Please check your internet connection.",
            app_icon= "icon1.ico",
            timeout=10
        )
        exit()
    while True:
        try:
            myHtmlData = getData("https://covidindia.org/")
            soup = BeautifulSoup(myHtmlData, 'html.parser')
            listStates = []
            for tr in soup.find_all('tbody')[0].find_all('tr'):
                tempLi = []
                for td in tr.find_all('td'):
                    tempLi.append(td.get_text())
                listStates.append(tempLi)
            listS = Sort(listStates)

            dictStates = createDict(listS)
            yourState = "Jharkhand"
            notifyMe(dictStates, listStates, yourState)
            time.sleep(60 * 60 * 6)
        except Exception as e:
            print("Data Fetching Unsuccessful!!")

    # else:
    #     myHtmlData = getData("https://covidindia.org/")
    #     soup = BeautifulSoup(myHtmlData, 'html.parser')
    #     listStates = []
    #     for tr in soup.find_all('tbody')[0].find_all('tr'):
    #         tempLi = []
    #         for td in tr.find_all('td'):
    #             tempLi.append(td.get_text())
    #         listStates.append(tempLi)
    #     listS = Sort(listStates)
    #
    #     dictStates = createDict(listS)
    #     yourState = "Jharkhand"
    #     notifyMe(dictStates, listStates, yourState)

