from urllib.request import urlopen
from urllib.parse import quote
import json

# Data details
url_text = "https://app.ticketmaster.com/discovery/v2/events.json?countryCode=AU&classificationName=music&dmaId=703&apikey=cCeZP8CSZLVdhoQD1ny8VXlGLyWbX3ts"


class import_data:
    def __init__(self, __dbName__, url_text):
        self.url_text = url_text
        self.__dbName__ = __dbName__
        
    def update_json(self):
        with urlopen(self.url_text) as url:
            data = json.loads(url.read().decode())
            # w clears the file
            with open("data.json", "w") as file:
                file.write(json.dumps(data))
impdata = import_data("", url_text)
# impdata.update_json()


with open("data.json", "r") as d:
    data = json.load(d)
    events = data["_embedded"]["events"]
    for event in events:
        venues = event['_embedded']['venues']
        for venue in venues: # you can also use venue = venues[0]
            address = venue['address']['line1']
            print(address)









# https://stpetersqldedu.sharepoint.com/sites/DigitalSolutions2022-23/_layouts/OneNote.aspx?id=%2Fsites%2FDigitalSolutions2022-23%2FSiteAssets%2FDigital%20Solutions%202022-23%20Notebook&wd=target%28_Content%20Library%2FAssessment.one%7CAC36FA0F-C5A0-4499-93E0-4A61E3C37BA3%2FJSON%20and%20Python%7CF325A1AE-4BB7-460A-82E9-77D43FED6B92%2F%29
# onenote:https://stpetersqldedu.sharepoint.com/sites/DigitalSolutions2022-23/SiteAssets/Digital%20Solutions%202022-23%20Notebook/_Content%20Library/Assessment.one#JSON%20and%20Python&section-id={AC36FA0F-C5A0-4499-93E0-4A61E3C37BA3}&page-id={F325A1AE-4BB7-460A-82E9-77D43FED6B92}&end