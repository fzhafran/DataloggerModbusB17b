#include <ESP8266WiFi.h>

String ClientRequest;
IPAddress staticIP311(10,22,30,203);
IPAddress gateway311(10,22,30,190);
IPAddress subnet311(255,255,255,192);

WiFiServer server(80);
int  A, B, C, D, E, F, G;


String  KONDISI1= "";
String  KONDISI2= "";
String  KONDISI3= "";
String  KONDISI4= "";
String  KONDISI5= "";
String  KONDISI6= "";
String  KONDISI7= "";


void setup(){
   ClientRequest = "";

Serial.begin(9600);
  WiFi.disconnect();
  delay(3000);
  Serial.println("START");
  WiFi.begin("ipiw","GakAdaJaringan");
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
  C = 0;
  D = 0;
  E = 0;
  F = 0;
  G = 0;  
  
pinMode(16, INPUT);
pinMode(17, INPUT);
pinMode(18, INPUT);
pinMode(19, INPUT);
pinMode(20, INPUT);
pinMode(21, INPUT);
pinMode(22, INPUT);

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
    C = digitalRead(18);
    if (C == HIGH) {
      KONDISI3 = "HIDUP";
    } 
else {
      KONDISI3 = "MATI";
      }
    D = digitalRead(19);
    if (D == HIGH) {
      KONDISI4 = "HIDUP";
    } 
else {
      KONDISI4 = "MATI";
      }
    E = digitalRead(20);
    if (E == HIGH) {
      KONDISI5 = "HIDUP";
    } 
else {
      KONDISI5 = "MATI";
      }
    F = digitalRead(21);
    if (F == HIGH) {
      KONDISI6 = "HIDUP";
    } 
else {
      KONDISI6 = "MATI";
      }
    G = digitalRead(22);
    if (G == HIGH) {
      KONDISI7 = "HIDUP";
    } 
else {
      KONDISI7 = "MATI";
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
  client.println(" , ");
  client.print(KONDISI3);
  client.println(" , ");
  client.print(KONDISI4);
  client.println(" , ");
  client.print(KONDISI5);
  client.println(" , ");
  client.print(KONDISI6);
  client.println(" , ");
  client.print(KONDISI7);
  client.println("");
  client.println("</html>");
  delay(1);
  client.flush();  
}
