import csv
import time
from requests import request
from selenium import webdriver
from bs4 import BeautifulSoup
import requests 
from selenium.webdriver.common.by import By
start_url="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser=webdriver.Edge("C:\WHITEHAT 26-7-21\msedgedriver.exe")

browser.get(start_url)
time.sleep(15)
headers=["Name","Distance","Mass","Radius"]
planet_data=[]
def scrap():
    for i in range(1,5):
        while True:
            time.sleep(3)
            soup=BeautifulSoup(browser.page_source,"html.parser")
            pgno=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if pgno<i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif pgno>i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        for th_tag in soup.find_all("th",attrs={"class","headerSort"}):
            tr_tags=th_tag.find_all("tr")
            templist=[]
            for index,li_tag in enumerate(tr_tags):
                if index==0:
                    templist.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(li_tag.contents[0])
                    except:
                        templist.append("")
            hyperlink_tr_tag=tr_tags[0]
            templist.append("https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"+ hyperlink_tr_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(templist)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"page number {i} scrappong done")      
   
scrap()
new_planets_data=[]
def scrapmoreinfo(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        templist=[]
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags=tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    templist.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        new_planets_data.append(templist)
    except:
        time.sleep(2)
        scrapmoreinfo(hyperlink)

for index,data in enumerate(planet_data):
    scrapmoreinfo(data[5])
    print(f"Scrapping at hyperlink {index+1} is done")

print(new_planets_data[0:10])
finalplanetdata=[]
for index,data in enumerate(planet_data):
    new_planet_data_element=new_planets_data[index]
    new_planet_data_element=[elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element=new_planet_data_element[:7]

    finalplanetdata.append(data+new_planet_data_element)
with open("Planets.csv","w") as f:
        csvwriter=csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(finalplanetdata)
 

