// ESP32 will make post requests to server on local network
// ESP32 has to be on same network

//  including wifi library
#include<WiFi.h>

//  including httpclient library
#include<HTTPClient.h>

//  wifi credentials
const char ssid[] = "SKYT2I1W";
const char password[] = "9gj91php1egL";

//  API url
String api = "http://192.168.0.5:5000/add-data";

//  creating http client
HTTPClient http;

//  potpin
const int potpin = 34;

void setup()
{
  Serial.begin(115200);
  Serial.print("Connecting to : ");
  Serial.println(ssid);
  WiFi.begin(ssid , password);
  while (WiFi.status()  !=  WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.println("Connected with Wifi !");
}

void loop()
{

  //  reading potentiometer
  int pot = analogRead(potpin);
  Serial.println(pot);

  //  check if wifi is still connected
  if (WiFi.status()  ==  WL_CONNECTED)
  {
        
    //  connect with server on that particular API
    http.begin(api);
    //  type of data to be shared : JSON
    http.addHeader("Content-Type","application/json");
    
    //  Write the data to be sent [ JSON format ]
    //  Example -->  String info = "{\"key_name\" : " + value in string format + "}";
    String info = "{\"potentiometer\":"+String(pot)+"}";
    //  hit the POST request
    int http_code = http.POST(info);
    //  check for response
    //  if response code > 0 : get the response message body

    if (http_code > 0){
      String response = http.getString();
      Serial.print("Response code");
      Serial.println(http_code);
      Serial.println("\t");
      Serial.print("Message from the server...");
      Serial.println(response);
      }
    //  if response code < 0, error occured
    else {
      Serial.println("Error code");
      Serial.println(http_code);
      }
    

    //  end the connection with server to free up the resources
    http.end();
    
  }

  //  if wifi not connected
  else
  {
    Serial.print("Not connected with : ");
    Serial.println(ssid);
  }


  //  wait for 1 seconds before hittng a POST request again
  delay(1000);

}
