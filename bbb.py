from six.moves import urllib
import time
import csv
from bs4 import BeautifulSoup
import validators
import requests

"""
def readCities( filename = 'cities.txt'):
  with open(filename) as cities:
    cities_list = []
    for city in cities:
      cities_list.append(city.rstrip())
  
  return cities_list TODO
"""

Businesses = ['Home','Paint','Wall','Contractor','Bathroom','Kitchen']
Cities = ['New York,NY','Los Angeles,CA','Chicago,IL','Houston,TX'
, 'Philadelphia,PA','Phoenix,AZ','San Antonio,TX', 'San Diego,CA ','Dallas,TX','San JoseCA','Sacramento,CO']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

filepath = 'unfiltered.csv'

f = csv.writer(open(filepath, "w+"),delimiter = ',')

# TODO Cities = readCities()
citynum = len(Cities)
for y,city in enumerate(Cities):
  for z,business in enumerate(Businesses):

    print '\n\n**************** :' , (y*z + z) , ' /' , citynum*6 , ' %:****************\n\n'

    try:  
      statespl = city.split(',' , 1)
      link = 'https://www.stonefabricatorsalliance.com/index.php?p=map'
      dreq = requests.get(link,headers=headers).text
      bs = BeautifulSoup(dreq,features="lxml")

      results = bs.find_all('h2', attrs={'class': 'SubTitle-sc-58v97z-0 fTMdMN'})[0]
      print '************************************'
      print results.text 
      print '************************************\n'
      number = results.find('strong').text
      maxpages = int(number)/15
      for page in range(1,maxpages):

        print ('Searching ' + business + ' , page :' + str(page))
        link = ('https://www.bbb.org/search?find_country=USA&find_loc=' + statespl[0] + '%2C%20' + statespl[1] + '&find_text=' + business + '&page=' + str(page) + '&sort=Relevance')
        dreq = requests.get(link,headers=headers).text
        bs = BeautifulSoup(dreq,features="lxml")
        listings = bs.find_all('div', attrs={'class': 'Content-sc-1g7b6fa-0 pWBSA'})
        
        if not listings:
          print 'NO MORE PLES'
          break

        print ('Link :' + link + '\n')
        for listing in listings:
          row = []

          try:
            url       = listing.find_all('a', attrs={'class': 'Name__Link-dpvfia-1 iyzkGZ'})[-1]['href']
          except:
            url       = 'Undefined'
    
          try:
            name      = listing.find_all("a", class_="Name__Link-dpvfia-1 iyzkGZ")[0].text
          except:
            name      = 'Undefined'

          try:
            phone     = listing.find_all("p", class_="MuiTypography-root MuiTypography-body1 MuiTypography-gutterBottom")[-1].text
          except:
            phone     = 'Undefined'

          try:
            location  = listing.find_all('strong')[-1].text
          except:
            location  = 'Serving the ' + city + ' area.'

          try:
            locality  = location.split(',' ,1)[1]
          except:
            locality  = 'Serving the ' + city + ' area.'

          try:
            address   = location.split(',' ,1)[0]
          except:
            address   = 'Serving the ' + city + ' area.'
        
          row.append(name)
          row.append(phone)
          row.append(address)
          row.append(locality)
          row.append(url)


          print ('====================')
          print ('Name :' + name)
          print ('Phone :' + phone)
          print ('Location :' + location)
          

          f.writerow(row)   # Write to csv


    except:
      time.sleep(3)
      print 'MOthafaukc maan'

f.close()
