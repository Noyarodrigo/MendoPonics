/******************************************************************************
 * Copyright 2018 Google
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *****************************************************************************/

#if defined(ARDUINO_SAMD_MKR1000) or defined(ESP32)
#define __SKIP_ESP8266__
#endif

#if defined(ESP8266)
#define __ESP8266_MQTT__
#endif

#ifdef __SKIP_ESP8266__

#include <Arduino.h>

void setup(){
  Serial.begin(115200);
}

void loop(){
  Serial.println("Hello World");
}

#endif

#ifdef __ESP8266_MQTT__
#include <CloudIoTCore.h>
#include "esp8266_mqtt.h"

static const uint8_t D0   = 16;
static const uint8_t D1   = 5;
static const uint8_t D2   = 4;
static const uint8_t D3   = 0;
static const uint8_t D4   = 2;
static const uint8_t D5   = 14;
static const uint8_t D6   = 12;
static const uint8_t D7   = 13;
static const uint8_t D8   = 15;
static const uint8_t D9   = 3;
static const uint8_t D10  = 1;

//dht libraries and conf
#include "DHT.h"
#define DHTPIN D3     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);

//DS18B20 libraries and conf
#include <OneWire.h>
#include <DallasTemperature.h>
const int oneWireBus = D4;
OneWire oneWire(oneWireBus);
DallasTemperature DS18B20(&oneWire);

//BH1850 libraries and conf
#include <Wire.h>
#include <BH1750.h>
BH1750 lightMeter;

//relay conf
#define rele_bomba D5
#define rele_luz D6

//wifi led
#define wifiled D7

bool flow_check();


void setup(){
 
  Serial.begin(9600);
  
  delay(10000);
  pinMode(LED_BUILTIN, OUTPUT); //internal led to visualize data being sent
  pinMode(wifiled, OUTPUT);
  dht.begin(); //initialize ambience temperature and humidity sensor
  DS18B20.begin();//initialize water temp sensor
  
  /*Initialize I2C communication protocol. It will start an I2C communication on the microcontroller’s default I2C pins
  If you want to use different I2C pins, pass them to the begin() method 
  like this Wire.begin(SDA, SCL).*/
  Wire.begin();
  lightMeter.begin();
  
  setupCloudIoT(); // Creates globals for MQTT

  //relays conf
  pinMode(rele_bomba,OUTPUT);
  pinMode(rele_luz,OUTPUT);
  digitalWrite(rele_bomba,HIGH);
  digitalWrite(rele_luz,HIGH);

  /*
  alerts logic
  the test n1 is on the msgrecieved func on wap8266_mqtt.h
    1- check if the device got a configuration, if it didn't send an alert (on the topic) and stop the microcontroler (enabled flag -> false)
    2- check pump relay: starts the pump and reads de flow sensor, if there's no flow then send an alert (topic) and stop de microcontroler.
    3- visual check for the user as the next sequence shows, the user just need to watch if the lights and pump turn on
  */
   
  delay(2000);
  digitalWrite(rele_luz,LOW);
  delay(2000);
  digitalWrite(rele_luz,HIGH);
  delay(1000);
  digitalWrite(rele_bomba,LOW);
  delay(2000);
  digitalWrite(rele_bomba,HIGH);
    
  Serial.println("Setup complete");

}

void loop(){
  
  if (!mqtt->loop())
  {
    mqtt->mqttConnect();
  }
  delay(10); // <- fixes some issues with WiFi stability
  
  if (enabled == true){
    //data sequence
    if (millis() - tm_data > data_sampling_time){
      tm_data = millis();
      //send_data();
    }
  
    //irrigation sequence
    if (millis() - tm_irrigation > irrigation_interval){
      tm_irrigation = millis();
      //irrigation_flag = true; //if the flag is set to true, irrigation control func will turn on the pump
    }
  
    //luminaire sequence
    if (millis() - tm_luminary > lum_sampling_time){
      tm_luminary = millis();
      //lum_flag = true;
    }
    irrigation_flag = true;
    irrigation_control();
    luminaire_control();
  
    //check connection
    if (WiFi.isConnected()){
      digitalWrite(wifiled,HIGH);
    }else{
      digitalWrite(wifiled,LOW);
      Serial.println("Restarting WiFi");
      setupWifi();
    }
  }
}

void send_data(){
  //get sensor data
  DS18B20.requestTemperatures();
  float tmpagua = DS18B20.getTempCByIndex(0); 
  float humedad = dht.readHumidity();
  float tmpambiente = dht.readTemperature();
  float luz = lightMeter.readLightLevel();

  //format the message to send it over MQTT and iot core library (Google)
  String payload = String("{\"timestamp\":") + time(nullptr) +
                   String(",\"email\":") + email +
                   String(",\"tmpambiente\":") + tmpambiente +
                   String(",\"tmpagua\":") + tmpagua +
                   String(",\"humedad\":") + humedad +
                   String(",\"luz\":") + luz +
                   String("}");
  Serial.println("publicando: ");
  Serial.println(payload);
  publishTelemetry(payload);
}

void irrigation_control(){
  if (irrigation_flag){ //timer flag if it's true then waiting time has finished
    if (pump_status == false){ //false -> pump is off, if it's off then turn on
      digitalWrite(rele_bomba,LOW); //LOW -> ON  
      pump_status = true; 
      Serial.println("Pump: ON");
      
      flow_status = flow_check(); //function to check if there's flow when the pump is on
      if (flow_status == false){ //false means that there's no flow -> turn the pump off and send the alert
        digitalWrite(rele_bomba,HIGH);  //HIGH -> OFF
        pump_status = false;
        Serial.println("ALERT (Pump: OFF)");
        return;
      }
      
      //format the message to send it over MQTT and iot core library (Google)
      String payload = String("{\"timestamp\":") + time(nullptr) +
                   String(",\"email\":") + email +
                   String(",\"pump\":") + 1 +
                   String("}");
      Serial.println("publicando: ");
      Serial.println(payload);
      publishTelemetry(payload);
    }
    if (millis() - tm_irrigation > irrigation_time_on){
      digitalWrite(rele_bomba,HIGH);  //HIGH -> OFF
      pump_status = false;
      irrigation_flag = false;
      Serial.println("Pump: OFF");
      
      //format the message to send it over MQTT and iot core library (Google)
      String payload = String("{\"timestamp\":") + time(nullptr) +
                   String(",\"email\":") + email +
                   String(",\"pump\":") + 0 +
                   String("}");
      Serial.println("publicando: ");
      Serial.println(payload);
      publishTelemetry(payload);
    }   
  }
}

void luminaire_control(){
  if (lum_flag){
    time_t now;
    struct tm * timeinfo;
    time(&now);
    timeinfo = localtime(&now); 
    int time_hr = timeinfo->tm_hour;
    //time hr is been used to stablish a time window between sunrise and sunset, sunset may be moved if the plant need more light hours
    //for example it could be set to 8am to 8pm to get 12 hrs of light, after that the counter is reseted and the lights are turned off
    //sunrise = 8am
    //expected = 10hrs
    //interval -> [8,8+10] -> [8,18]
    if (time_hr > sunrise && time_hr < sunset){
      Serial.println("Verificando luces, dentro del intervalo");
      if (lum_status_on == false){
        digitalWrite(rele_luz,LOW); //LOW -> ON      
        Serial.println("Lights: ON");
        lum_status_on = true;
        lum_status_off = false;
        
        //format the message to send it over MQTT and iot core library (Google)
        String payload = String("{\"timestamp\":") + time(nullptr) +
                     String(",\"email\":") + email +
                     String(",\"estadoluces\":") + 1 +
                     String("}");
        Serial.println("publicando: ");
        Serial.println(payload);
        publishTelemetry(payload);
      }
     }else{
       if (lum_status_off == false){
          digitalWrite(rele_luz,HIGH); //HIGH -> OFF
          Serial.println("Lights: OFF");
          lum_status_on = false;
          lum_status_off = true;
  
          //format the message to send it over MQTT and iot core library (Google)
          String payload = String("{\"timestamp\":") + time(nullptr) +
                       String(",\"email\":") + email +
                       String(",\"estadoluces\":") + 0 +
                       String("}");
          Serial.println("publicando: ");
          Serial.println(payload);
          publishTelemetry(payload);
        }
      }
    }
    lum_flag = false;
  }

bool flow_check(){
  if (pump_status){ //true -> pump: ON
    send_alert("no_flow_err",3);
    enabled = false;
    return false;
    /*if theres flow
        print pump ok
        enabled = true;
        return true;
      else
        send_alert("no_flow_err",3);
        enabled = false;
        return false;
    */
  }
}

#endif
