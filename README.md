# Checking room temperature and humidity over Messenger

<br>
<br>

Technologies used in building this chatbot:

- [Messenger-Platform](https://developers.facebook.com/docs/messenger-platform/) API for chat
- [Node.js](https://nodejs.org/en/) for chatbot backend
- [Scrapy](https://scrapy.org/) for scraping

<br>

To messure room temperature i used DHT11 Arduino module which is outputing values to Serial. This values are catched using python script that is spawned using node application.

Arduino code

```C
#include <dht.h>

dht DHT;

#define DHT11_PIN 2

void setup(){
  Serial.begin(9600);
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  String msg = String(int(DHT.temperature)) + "," + String(int(DHT.humidity));
  Serial.println(msg);

  // Serial.flush();
  delay(2000);
}
```

Python script that will read values from Serial

```Python
from time import sleep
import serial
import sys

ser = serial.Serial('/dev/ttyACM0', 9600)
def Sensor():
    msg  = ser.readline()
    split = msg.split(",")

    if(len(split) == 2):
        i=0

        while i < (len(split)):
            split[i].replace("\\r\\n","")
            i=i+1
        split[1] = split[1].rstrip('\n')
    try:
        return {"temp":split[0],"hum":split[1]}
    except:
        return "Error"


while True:
    param = Sensor()
    if param != "Error":
        if sys.argv[1] == "temp":
            print(param["temp"])
            sys.stdout.flush()
            break
        elif sys.argv[1] == "hum":
            print(param["hum"])
            sys.stdout.flush()
            break


    sleep(2)

```

Inside our chatbot we will listen to keywords.

```javascript
case 'temp':
        var spawn = require("child_process").spawn;
        var pythonProcess = spawn('python',["./python/script.py","temp"]);
        pythonProcess.stdout.on('data',function (data){
            var poruka = "Room temperature is: " + data + "\xB0"+"C";
	    poruka = poruka.replace(/(\r\n|\n|\r)/gm,"");
	    sendTextMessage(senderID, poruka);
	});
        break;
```

![gif1](https://raw.githubusercontent.com/Enzzza/iot-chatbot/main/media/gif1.gif)

While we were waiting for the results of the [Red Bull](https://github.com/Enzzza/unibot) competition (which we won) I added the following function to my chatbot.

![gif2](https://raw.githubusercontent.com/Enzzza/iot-chatbot/main/media/gif2.gif)

I used Scrapy spider to scrape live results from RedBull site.

```python
# -*- coding: utf-8 -*-
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import json, ast
from pprint import pprint
import sys
from time import sleep


class RedbullSpiderSpider(scrapy.Spider):
    name = 'RedBull-spider'
    allowed_domains = ['redbull.com']
    start_urls = ['https://basement.redbull.com/university-api/entrants']

    def parse(self, response):


        result = json.loads(response.text)
        List = []
        registrations  = result["registrations"]



       	for i in range(len(registrations)):
            if(registrations[i]["country"] == "Bosnia and Herzegovina"):
                List.append(registrations[i])

        sortedList = sorted(List, key=lambda k: k['voteCount'],reverse=True)

	#newList = eval(json.dumps(sortedList))
        print(json.dumps(sortedList))
        sys.stdout.flush()
	#with open('data.json','w') as outfile:
	    #json.dump(sortedList,outfile)
                #return sortedList

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(RedbullSpiderSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished

sleep(1000)

```
