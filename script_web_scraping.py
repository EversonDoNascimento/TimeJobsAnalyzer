from bs4 import BeautifulSoup 
import requests
from collections import Counter
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import matplotlib.pyplot as plt
import re
import random
vacancy = ""
while re.sub(r'\s+', '', vacancy) == "":
    vacancy = input("Type it your desire vacancy: ")


# Função para retornar próxima página
def nextPage(startPage: str, sequence: str, url, search: str):
    # Parse a URL
    parsed_url = urlparse(url)
    # Obter os parâmetros da consulta
    new_search = search.replace(" ",'%')
    query_params = parse_qs(parsed_url.query)
    query_params['sequence'] = [sequence]
    query_params['startPage'] = [startPage]
    query_params['txtKeywords'] = [new_search]
    query_params['actualTxtKeywords'] = [new_search]
    # Reconstruindo nova url
    new_url = urlencode(query_params, doseq=True)
    #Criando lista
    new_url_list = list(parsed_url)
    new_url_list[4] = new_url
    new_url = urlunparse(new_url_list)
    return new_url.replace("%25","%20")
    

def scrapingJobs(end_page: str = 1, search: str = "python"):
    list_jobs = []
    for i in range(1, int(end_page)):
        url = nextPage(str(i), str(i), "https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords=react&postWeek=60&searchType=personalizedSearch&actualTxtKeywords=react&searchBy=0&rdoOperator=OR&pDate=I&sequence=4&startPage=1",search )
        response = requests.get(url)       
        soup = BeautifulSoup(response.text, "lxml")
        vacancys = soup.find_all("li", class_="clearfix")
        if(len(vacancys) == 1):           
            print("Vacancies not found!")
            break
        for vacancy in vacancys[1::]:
            temp = " ".join(vacancy.a.text.replace("\n","").replace("/","").capitalize().split())
            list_jobs.append(temp)
    counter = Counter(list_jobs)
    counter_sorted = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    return counter_sorted[0:5]
    
    


def generateGraphic(list, office):
    plt.figure(figsize=(15, 6))
    if(len(list) >= 0):
        for key, value in list:
            
            plt.bar(key, value, color="blue", edgecolor="black")
            
            plt.title('Jobs')
            plt.xlabel('Office')
            plt.ylabel(f'Quantity of Vacancies {office}')
           
        plt.savefig(f'Jobs_to_{vacancy}_{random.randint(1,100000)}.png')
        
        plt.show()
    else:
        print("Vacancies not found!")

scraping = (scrapingJobs(5, vacancy))
generateGraphic(scraping, vacancy)