//data conf
extern int data_sampling_time = 1*60000; //minutes
extern unsigned long tm_data = 0; // sending data aux timer

//irrigation conf
extern int irrigation_interval = 30*60000;
extern int irrigation_time_on = 15*60000; //how long will the pump be turned on
extern unsigned long tm_irrigation = 0; //irrigation aux timer
extern bool irrigation_flag = false; //timer flag
extern bool pump_status = false; //true -> pump on

//luminaire conf
extern unsigned long tm_luminary = 0; //luminary aux timer
extern int lum_sampling_time = 1*60000; //minutes
extern bool lum_flag = false; //func aux
extern bool lum_status_on = false; //are the lights on? True:ON 
extern bool lum_status_off = false; //are the lights on? True:ON 
extern int sunrise = 8;
extern int sunset = 17; //this is how many hours the plant should be exposed
