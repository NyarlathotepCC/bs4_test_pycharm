import requests
from bs4 import BeautifulSoup
import json

def google_sector_report():

    url = "https://www.google.com/finance"

    basepage = requests.get(url)
    soup = BeautifulSoup(basepage.content, "lxml")

    change_list=soup.find("div", id="secperf")
    baserefs=change_list.find_all("a")
    indusnames = list()

    for linkthingy in baserefs:
        indusnames.append(linkthingy.get_text())


    # print(indusnames)                   ########################## names

    percent_changes = list()

    for percchange in change_list.find_all("span"):
        percent_changes.append(percchange.get_text()) ###indust changes

    # print(baserefs)
    links = list()

    for linkthingy2 in baserefs:
        links.append("http://google.com" + linkthingy2["href"])

    gainerlist = list()
    gainerchangelist = list()
    loserlist = list()
    loserchangelist = list()

    for link in links:
        basepage = requests.get(link)
        basesoup = BeautifulSoup(basepage.content, "lxml")
        baserefs = basesoup.find("table", class_="topmovers")
        gainerlist.append(baserefs.find("a").get_text()) ####################### industry gainer
        gainerchangelist.append(baserefs.find("span", class_="chg").get_text()) ##### change
        loserlist.append(baserefs.find_all("a")[10].get_text())  #################### industry loser
        loserchangelist.append(baserefs.find("span", class_="chr").get_text()) ##### change

    # print(gainerlist, "\n" , gainerchangelist, "\n" , loserlist, "\n" , loserchangelist) #test

    output = dict()
    output["result"] = dict()
    for i in range(10): # 10 industries of interest
        output["result"][indusnames[i]]= {"biggest_gainer": {"equity": gainerlist[i], "change": gainerchangelist[i]},
                                          "biggest_loser": {"equity": loserlist[i],"change": loserchangelist[i]},
                                          "change": percent_changes[i]}

    return(json.dumps(output))


google_sector_report()