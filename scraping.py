import requests
from bs4 import BeautifulSoup
import pandas

urls= ["https://www.nobroker.in/property/sale/mumbai/Bandra%20West?searchParam=W3sibGF0IjoxOS4wNTk1NTk2LCJsb24iOjcyLjgyOTUyODcsInBsYWNlSWQiOiJDaElKZTlMNEktSEk1enNSZUdvam1yU1dlVU0iLCJwbGFjZU5hbWUiOiJCYW5kcmEgV2VzdCJ9XQ==&radius=2.0&city=mumbai&locality=Bandra%20West&type=BHK2,BHK3","https://www.nobroker.in/property/sale/chennai/Pallavaram?searchParam=W3sibGF0IjoxMi45Njc1MDY5LCJsb24iOjgwLjE0OTA5NTUsInBsYWNlSWQiOiJDaElKczJ5N0VEVmVVam9SdkplX1UweTdXWTQiLCJwbGFjZU5hbWUiOiJQYWxsYXZhcmFtIn1d&radius=2.0&city=chennai&locality=Pallavaram&type=BHK2,BHK3","https://www.nobroker.in/property/sale/bangalore/Madanayakana%20Halli?searchParam=W3sibGF0IjoxMy4wNjA5NzMsImxvbiI6NzcuNDYxODM4LCJwbGFjZUlkIjoiQ2hJSjlVRVdDNjhrcmpzUm9ndVRJN2piWFU0IiwicGxhY2VOYW1lIjoiTWFkYW5heWFrYW5hIEhhbGxpIn1d&radius=2.0&city=bangalore&locality=Madanayakana%20Halli&type=BHK2,BHK3","https://www.nobroker.in/property/sale/delhi/Chandni%20Chowk?searchParam=W3sibGF0IjoyOC42NTA1MzMxLCJsb24iOjc3LjIzMDMzNjk5OTk5OTk5LCJwbGFjZUlkIjoiQ2hJSldjWGNpQnI5RERrUlViNGRDRHlrVHdJIiwicGxhY2VOYW1lIjoiQ2hhbmRuaSBDaG93ayJ9XQ==&radius=2.0&city=delhi&locality=Chandni%20Chowk&type=BHK2,BHK3"]


location = []
name = []
pricelist =[]
sqft = []
total_words = []
state = []
    
for i in urls:
    
    print(i,'\n' '\033[1m S c r a p i n g   D o n e . .  F O R  A B O V E  L I N K  . . . . \033[0m')
    

    url = i
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    req = requests.get(url,headers=agent)   
    soup = BeautifulSoup(req.text,'html.parser')

#collecting data according to the tags given -----------------------\

    nameof = soup.find_all('a',class_="nb__U5JyW")
    for x in nameof:

      if urls.index(i)==0:
        state.append('Mumbai')
      elif urls.index(i)==1:
        state.append('Chennai')
      elif urls.index(i)==2:
        state.append('Banglore')
      else:
        state.append('Delhi')

      name.append(x.getText())
        
    sqfet = soup.find_all("div","nb__FfHqA")
    for k in sqfet:
        sqft.append(k.getText())
    
    
    price_persq = soup.find_all("div",id = "minDeposit")
    for price in price_persq:
        pricelist.append(price.contents[1].getText())

    price_persq = soup.find_all("div",id = "minDeposit")
    for price in price_persq:
        total_words.append(price.contents[0].getText())

    
    lk = soup.find_all("div","nb__jvFlz")
  
    for loca in lk:
        location.append(loca.contents[0])


#creating dataframe to store scraped data in a readable manner -----------------\

    df = pandas.DataFrame(name,columns=["Names"])
    df["Location"]=location 
    df['State']=state
    df["Total_Sqft"]=sqft
    df["Price_perSqft"]=pricelist
    df["Total_price_Words"]=total_words


#converting price from words to float type for further analytics ----------------\
    
total=[]
for x in df['Total_price_Words']:
  
  if 'Crores' in x:
    x = x.replace('â\x82¹',"")
    x = x.replace('Crores','')
    
    x = float(x)*10**7
  elif 'Crore' in x:
    x = x.replace('â\x82¹',"")
    x = x.replace('Crore','')
    x = float(x)*10**7

  else:
    x = x.replace('â\x82¹',"")
    x = x.replace('Lacs','')
    x = float(x)*10**5
    
  total.append(x)

df["Total_price"]=total




  

print('\n\n\n' '\033[1m D A T A   F R A M E   C R E A T E D  \033[0m''\n')
print(df,'\n')
print('\n' '\033[1m D A T A   F R A M E   C O L U M N S   \033[0m''\n')
print(df.columns)


print('\n\n\033[91m \033[1m N O T E  : - - \n\033[0m \t\t\t\t I TRIED TO PLOAT A GRAPH BUT REPLIT DOSNT SUPPORT HEAVY WORKING ')

newdf = df.groupby(['State'], as_index=False)['Total_price'].sum()

newdf.plot(y ='Total_price', x='State',kind = 'bar')
