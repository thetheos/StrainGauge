int val;
int pin = 14;
int inputBuf=0;
int modeSelect = 1; //première couche
int range=5;
int sampleRate = 100;
String buff;
int temp;
int delayTime = 50;

String inputString = "";
volatile boolean stringComplete = false;

bool set0 = true;
bool set1 = true;
bool set2 = true;
bool set3 = true;

int modeSetup = 0; //deuxième couche
int settingSelect = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pin, INPUT);
  Serial.println("Select your mode : continuous reading mode(1), triger mode(2), triger mode settings(3)");
  inputString.reserve(200);
  
}

void loop() {
  unsigned long startTime = millis();
  if(stringComplete == true && modeSetup == 0){
    temp = inputString.toInt();
    modeSelect = temp;
    inputString = "";
    stringComplete = false;
  }

  if(modeSelect==0){
  }
  else if(modeSelect==1){
    val = analogRead(pin);
    Serial.print(startTime);
    Serial.print('\t');
    Serial.println(val);
    delay(delayTime);
  }
  else if(modeSelect==2){
    triger();
  }
  else if(modeSelect == 3){
    trigerSetup();
    
  }
  else {
    Serial.println("incorect input");
    delay(500);
  }
}

void triger(){
  unsigned long startTime = millis();
  int val1 = analogRead(pin);
  delay(20);
  int val2 = analogRead(pin);
  int valf = val2-val1;

  
  if(valf>range || valf<-range){
    for(int i = 0; i<sampleRate; i++){
      int val = analogRead(pin);
      Serial.print(startTime);
      Serial.print('\t');
      Serial.println(val);
    }
  }
  else if(valf<range || valf>-range){
  
  }
  
}

void trigerSetup(){
  if(set0 && modeSetup == 0){
    Serial.println("Triger setup mode: range setup(1), sample rate setup(2),delay setup(3), quit(4)");
    set0 = false;
    modeSetup = 1;
  }
  
  if(stringComplete == true && modeSetup == 1){
    temp = inputString.toInt();
    settingSelect = temp;
    inputString = "";
    stringComplete = false;
  }
  if(settingSelect == 0){}
  else if(settingSelect == 1)
    trigerSetupRange();
  else if(settingSelect == 2)
    trigerSetupSampleRate();
  else if(settingSelect == 3)
    delayTimeSetup();
  else if(settingSelect == 4){
    modeSetup = 0;
    Serial.println("Select your mode : continuous reading mode(1), triger mode(2), triger mode settings(3)");
    settingSelect = 0;
    modeSelect = 0;
    set0 = true;
  }   
  else
    Serial.println("incorrect input");
}

void trigerSetupRange(){
   if(set1){
    Serial.print("Actual range: ");
    Serial.println(range);
    Serial.println("Set new range: "); 
    set1 = false;
    modeSetup = 2;
   }
   if(stringComplete == true && modeSetup == 2){
    temp = inputString.toInt();
    range = temp;
    Serial.print("new range: ");
    Serial.println(range);
    inputString = "";
    stringComplete = false;
    modeSetup =1;
    set0 = true;
   }
}

void trigerSetupSampleRate(){
   if(set2){
    Serial.print("Actual SampleRate: ");
    Serial.println(sampleRate);
    Serial.println("Set new sampleRate: "); 
     Serial.println("Triger setup mode: range setup(1), sample rate setup(2),delay setup(3), quit(4)");
    set2 = false;
    modeSetup = 2;
   }
   if(stringComplete == true && modeSetup == 2){
    temp = inputString.toInt();
    sampleRate = temp;
    Serial.print("new sampleRate: ");
    Serial.println(sampleRate);
     Serial.println("Triger setup mode: range setup(1), sample rate setup(2),delay setup(3), quit(4)");
    inputString = "";
    stringComplete = false;
    modeSetup =1;
    set0 = true;
   }
}

void delayTimeSetup(){
   if(set3){
    Serial.print("Actual delay: ");
    Serial.println(delayTime);
    Serial.println("Set new delay: "); 
    set3 = false;
    modeSetup = 3;
   }
   if(stringComplete == true && modeSetup == 3){
    temp = inputString.toInt();
    delayTime = temp;
    Serial.print("new delay: ");
    Serial.println(delayTime);
     Serial.println("Triger setup mode: range setup(1), sample rate setup(2),delay setup(3), quit(4)");
    inputString = "";
    stringComplete = false;
    modeSetup =1;
    set0 = true;
   }
}

void serialEvent(){
  while (Serial.available()) {
    // récupérer le prochain octet (byte ou char) et l'enlever
    char inChar = (char)Serial.read(); 
    // concaténation des octets reçus
    inputString += inChar;
    // caractère de fin pour notre chaine
    if (inChar == '\n') {  
      stringComplete = true;
    }
  }
}

