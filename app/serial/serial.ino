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

