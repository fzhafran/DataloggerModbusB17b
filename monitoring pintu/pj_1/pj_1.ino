#include <ESP8266WiFi.h>

String ClientRequest;
IPAddress staticIP311(10,22,29,52);
IPAddress gateway311(10,22,30,190);
IPAddress subnet311(255,255,255,192);

WiFiServer server(80);
int  A, B;


String  KONDISI1= "";
String  KONDISI2= "";


void setup(){
   ClientRequest = "";

Serial.begin(9600);
  WiFi.disconnect();
  delay(3000);
  Serial.println("START");
  WiFi.begin("Medion","Medioncare123");
  while ((!(WiFi.status() == WL_CONNECTED))){
  delay(300);
  Serial.print("..");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
   
  }
  Serial.println("Connected");
  WiFi.config(staticIP311, gateway311, subnet311);
  Serial.println("Your IP is");
  Serial.println((WiFi.localIP().toString()));
  server.begin();
  A = 0;
  B = 0;
  
pinMode(16, INPUT);
pinMode(17, INPUT);

}


void loop(){
    A = digitalRead(16);
    if (A == HIGH) {
      KONDISI1 = "HIDUP";
    } 
else {
      KONDISI1 = "MATI";
      }
    B = digitalRead(17);
    if (B == HIGH) {
      KONDISI2 = "HIDUP";
    } 
else {
      KONDISI2 = "MATI";
      }

  WiFiClient client = server.available();
  if (!client){ return; }
  while(!client.available()){ delay(1); }
  ClientRequest = (client.readStringUntil('\r'));
  ClientRequest.remove(0,5);
  ClientRequest.remove(ClientRequest.length()-9,9);
  Serial.println("new request");
  Serial.println(ClientRequest);
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println("");
  client.println("<!DOCYTYPE HTML>");
  client.println("<html>");
  client.print(KONDISI1);
  client.print(" , ");
  client.print(KONDISI2);
  client.println("");
  client.println("</html>");
  delay(1);
  client.flush();  
}
