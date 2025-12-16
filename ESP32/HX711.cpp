#include "HX711.h"

bool is_ready(struct HX711 *hx711){
    return digitalRead(hx711->DOUT) == 0;
}

void set_gain(struct HX711 *hx711, uint8_t new_gain){
    uint8_t gain = 1;
    switch (new_gain) {
        case 128:
            gain = 1;
            break;
        case 64:
            gain = 3;
            break;
        case 32:
            gain = 2;
            break;
    }

    hx711->GAIN = gain;
}

void wait_ready(struct HX711 *hx711, uint32_t time){
    while (!is_ready(hx711)) delay(time);
}

uint8_t shiftInSlow(uint8_t dataPin, uint8_t clockPin, uint8_t bitOrder) {
    uint8_t value = 0;
    uint8_t i;

    for (i = 0; i < 8; ++i) {
        digitalWrite(clockPin, HIGH);
        delayMicroseconds(1);
        if (bitOrder == LSBFIRST)   
            value |= digitalRead(dataPin) << i;
        else
            value |= digitalRead(dataPin) << (7 - i);
        digitalWrite(clockPin, LOW);
        delayMicroseconds(1);
    }
    return value;
}


int32_t read(struct HX711 *hx711){
    wait_ready(hx711, 1);

    uint32_t value = 0;
    uint8_t data[3] = { 0 };
    uint8_t filler = 0x00;

	portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;
	portENTER_CRITICAL(&mux);

    for (uint8_t i = 0; i < 3; i++)
        data[2 - i] = shiftInSlow(hx711->DOUT, hx711->SCK, MSBFIRST);

    for (uint8_t i = 0; i < hx711->GAIN; i++){
        digitalWrite(hx711->SCK, HIGH);
        delayMicroseconds(1);
        digitalWrite(hx711->SCK, LOW);
        delayMicroseconds(1);
    }

	portEXIT_CRITICAL(&mux);

    filler = data[2] & 0x80 ? 0xFF : 0x00;

    value = ((uint32_t)filler << 8*3)
          | ((uint32_t)data[2] << 8*2) 
          | ((uint32_t)data[1] << 8)
          | ((uint32_t)data[0]);

    return (int32_t)value;
}

int32_t read_avg(struct HX711 *hx711, uint8_t times){
    int32_t sum = 0;
    for (uint8_t i = 0; i < times; i++)
        sum += read(hx711);

    return sum;
}

void tare(struct HX711 *hx711, uint8_t times){
    int32_t sum = read_avg(hx711, times);
    // set_offset(sum);
}

// void set_offset(int32_t offset){
//     return;
// }