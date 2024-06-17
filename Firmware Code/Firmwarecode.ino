#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <EEPROM.h>

Adafruit_ADS1115 ads;

#define EEPROM_ADDR 0x50
#define EEPROM_SIZE 16384

unsigned int eeprom_address = 0;

// Function to write a single byte to EEPROM
void writeEEPROM(int deviceAddress, unsigned int eeAddress, byte data) {
  Wire.beginTransmission(deviceAddress);
  Wire.write((int)(eeAddress >> 8)); // MSB
  Wire.write((int)(eeAddress & 0xFF)); // LSB
  Wire.write(data);
  Wire.endTransmission();
  delay(5);
}

// Function to read a single byte from EEPROM
byte readEEPROM(int deviceAddress, unsigned int eeAddress) {
  byte rdata = 0xFF;
  Wire.beginTransmission(deviceAddress);
  Wire.write((int)(eeAddress >> 8)); // MSB
  Wire.write((int)(eeAddress & 0xFF)); // LSB
  Wire.endTransmission();
  Wire.requestFrom(deviceAddress, 1);
  if (Wire.available()) rdata = Wire.read();
  return rdata;
}

void setup(void) {
  Serial.begin(9600);
  Wire.begin();
  ads.begin();
}

void loop(void) {
  int16_t adc0, adc1;

  // Read ADC values
  adc0 = ads.readADC_SingleEnded(0);
  adc1 = ads.readADC_SingleEnded(1);

  // Store ADC0 value in EEPROM
  writeEEPROM(EEPROM_ADDR, eeprom_address++, 0x00); // Prefix byte
  writeEEPROM(EEPROM_ADDR, eeprom_address++, (byte)(adc0 >> 8)); // MSB of adc0
  writeEEPROM(EEPROM_ADDR, eeprom_address++, (byte)(adc0 & 0xFF)); // LSB of adc0

  // Store ADC1 value in EEPROM
  writeEEPROM(EEPROM_ADDR, eeprom_address++, 0x01); // Prefix byte 
  writeEEPROM(EEPROM_ADDR, eeprom_address++, (byte)(adc1 >> 8)); // MSB of adc1
  writeEEPROM(EEPROM_ADDR, eeprom_address++, (byte)(adc1 & 0xFF)); // LSB of adc1

  if (eeprom_address >= EEPROM_SIZE) {
    eeprom_address = 0;
  }

  unsigned int read_address = eeprom_address;

  for (int i = 0; i < 2; i++) { // We know we stored 2 sets of 3 bytes
    byte channel = readEEPROM(EEPROM_ADDR, read_address++);
    byte adc_MSB = readEEPROM(EEPROM_ADDR, read_address++);
    byte adc_LSB = readEEPROM(EEPROM_ADDR, read_address++);
    int16_t adc_value = (adc_MSB << 8) | adc_LSB;

    Serial.print("Channel: "); Serial.print(channel);
    Serial.print(" ADC Value: "); Serial.println(adc_value);
  }

  delay(1000);
}
