#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include "Arduino.h"

#define PIN_COUNT 5
#define MSBFIRST 1
#define LSBFIRST 0

// #define IS_FREE_RTOS defined(ARDUINO_ARCH_ESP32)

struct HX711 {
    uint8_t DOUT;
    uint8_t SCK;
    uint8_t GAIN;
    int32_t OFFSET;
    int32_t RESULT;
};


// Check if HX711 is ready
bool is_ready(struct HX711 *hx711);

/// Set gain
/// 128, 64, 32 
/// default 128
void set_gain(struct HX711 *hx711, uint8_t new_gain);

int32_t read(struct HX711 *hx711);

void wait_ready(struct HX711 *hx711, uint32_t time);

void tare(struct HX711 *hx711, uint8_t times);

void set_offset(struct HX711 *hx711, int32_t offset);

int32_t get_offset(struct HX711 *hx711);

int32_t read_avg(struct HX711 *hx711, uint8_t times);

uint8_t shiftInSlow(uint8_t dataPin, uint8_t clockPin, uint8_t bitOrder);
