import pydub
from bs4 import BeautifulSoup 
from urllib.request import Request, urlopen
import requests
import re
import os
import time
import csv

print("Establishing connection with doc num")

urlToOpen = "https://freemusicarchive.org/search?adv=1&search-genre=Blues%2CHip-Hop%2CJazz%2CRock%2CClassical%2CCountry%2CFolk%2CPop%2CElectronic&music-filter-CC-attribution-only=1&music-filter-CC-attribution-sharealike=1&music-filter-CC-attribution-noncommercial=1&music-filter-CC-attribution-noncommercial-sharealike=1&pageSize=200&page=1"

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

req = Request(
    url=urlToOpen, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
)

with urlopen(req) as webPageResponse: 
    contents = webPageResponse.read() 
    
webPageResponse.close()  

print("Connection established and HTML copied")


beautifulSoupText = BeautifulSoup(contents, 'lxml') 


tmp = beautifulSoupText.find_all("div", attrs={"class": ["play-item", "justify-center", "items-center", "relative", "bg-[#F8F8F8]", "gcol", "grid", 
                                                  "grid-cols-3", "md:grid-cols-10", "pl-16", "pr-2", "py-3", "w-full", "gid-electronic"]})

print(len(tmp))
print("\n")


specific_row = ['songName', 'artistName', 'windowsPath', 'unixPath', 'genres']

# This cycle is good
for i in range(20, len(tmp) - 3):
    # print( tmp[i].find("span", attrs={"class": ["ptxt-track"]}).find("a").text )
    
    songName = tmp[i].find("span", attrs={"class": ["ptxt-track"]}).find("a").text.replace("\n", "").replace("|", "")
    artistName = tmp[i].find("span", attrs={"class": ["ptxt-artist", "truncate", "text-ellipsis", "overflow-hidden"]}).find_all("span")[1].find("a").text.replace("\n", "").replace("|", "")
    trackLink = tmp[i].find("span", attrs={"class": ["ptxt-track"]}).find("a").get("href")
    
    songGenres = []
    songGenres.clear()
    
    print(songName)
    print(artistName)
    for row in tmp[i].find("span", attrs={"class": ["ptxt-genre"]}).find_all("a"):
        songGenres.append(row.text)
    
    for genre in songGenres:
        print(genre)
    
    print(trackLink)
    
    print("\n")
    
    fileSongName = songName + " - " + artistName + ".mp3"
    
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    
    
    
    trackPage = Request(
        url=trackLink, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'},
        )
    
    with urlopen(trackPage) as webPageResponse: 
        trackPageContent = webPageResponse.read() 
        
    webPageResponse.close()  
    
    beautifulSoupTrackPage = BeautifulSoup(trackPageContent, 'lxml') 
    
    # print(beautifulSoupTrackPage )
    
    fileNameDiv = beautifulSoupTrackPage.select("div.flex.items-center.gap-4.px-4.py-2.bg-gray-light.py-4.rounded.mx-auto.w-full.gcol.gid-electronic")[0].get("data-track-info")
    downloadLink = re.search('"fileUrl":"(.*)"', fileNameDiv).group(1).replace("\\", "") + "?download=1"
    
    
    
    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        s.headers = headers
        tokenPage = s.get("https://freemusicarchive.org/login")
        token = re.search('value="(.*)"> ', tokenPage.text[tokenPage.text.find("_token"):]).group(1)
        
    
        payload = {
            '_token': token,
            'email': 'zarkon92@hotmail.it',
            'password': 'F7kWWi/5v2-RbSb'
        }
        
        p = s.post('https://freemusicarchive.org/login', data=payload)
        
        if p.history:
            print("Request was redirected")
            for resp in p.history:
                print(resp.status_code, resp.url)
            print("Final destination:")
            print(p.status_code, p.url)
        else:
            print("Request was not redirected")
            
    
    
        r = s.get(
            url=downloadLink, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'},
            allow_redirects=True
            )
        
        
        with open(".\\songs\\" + songName + " - " + artistName + " - toTrim.mp3", 'wb') as f:
            f.write(r.content)
            
        
            
        audio = pydub.AudioSegment.from_mp3(".\\songs\\" + songName + " - " + artistName + " - toTrim.mp3")
        startTime = audio.duration_seconds / 2
        endTime = startTime + 5
        
        centralPart = audio[startTime * 1000 : endTime * 1000]
        
        centralPart.export(".\\songs\\" + songName + " - " + artistName + ".mp3", format="mp3")
        
        if os.path.exists(".\\songs\\" + songName + " - " + artistName + " - toTrim.mp3") and os.path.exists(".\\songs\\" + songName + " - " + artistName + ".mp3"):
            os.remove(".\\songs\\" + songName + " - " + artistName + " - toTrim.mp3")
            
        windowsPath = ".\\songs\\" + songName + " - " + artistName + ".mp3"


        songData = [songName, artistName, windowsPath, "./songs/" + songName + " - " + artistName + ".mp3", songGenres]

        print(songData)

        # Open our existing CSV file in append mode
        # Create a file object for this file
        with open(r"C:\Users\kryas\Desktop\DatasetDeepLearning\songsTrimmed.csv", 'r', newline='',  encoding='utf-8') as f_object:
            reader = csv.reader(f_object)
            rows = list(reader)
        
        try:
            index = rows.index(specific_row)
        except ValueError:
            print("Specific row not found.")
            exit(0)
            
        rows.insert(index + 1, songData)

        # Write the modified data back to the CSV file
        with open(r"C:\Users\kryas\Desktop\DatasetDeepLearning\songsTrimmed.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        time.sleep(0.5)
