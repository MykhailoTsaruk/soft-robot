#include "HX711.h"
#include "multiprocessing.h"

struct HX711 hx711[PIN_COUNT];

void setup() {
    Serial.begin(460800);
    uint8_t DOUT_PINS[PIN_COUNT] = { 26 , 25, 33, 32, 35 };
    uint8_t SCK_PINS[PIN_COUNT] = { 17, 5, 18, 19, 21 };

    for (uint8_t i = 0; i < PIN_COUNT; i++){
        pinMode(DOUT_PINS[i], INPUT);
        pinMode(SCK_PINS[i], OUTPUT);
    }
    
    for (uint8_t i = 0; i < PIN_COUNT; i++){
        hx711[i].DOUT = DOUT_PINS[i];
        hx711[i].SCK = SCK_PINS[i];
        hx711[i].GAIN = 1;
        hx711[i].OFFSET = 0;
    }

    syncGroup = xEventGroupCreate();

    xTaskCreatePinnedToCore(taskEven, "EvenTask", 4096, hx711, 1, NULL, 0);
    xTaskCreatePinnedToCore(taskOdd,  "OddTask",  4096, hx711, 1, NULL, 1);
}

void loop() {
    uint32_t start_time = millis();

    xEventGroupWaitBits(
        syncGroup,
        EVEN_DONE | ODD_DONE,
        pdTRUE,
        pdTRUE,
        portMAX_DELAY
    );
    for (int i = 0; i < PIN_COUNT; i++)
        Serial.printf("Result for sensor %d: %ld\n", i, hx711[i].RESULT);

    uint32_t end_time = millis();
    Serial.printf("Processing time: %ld millis\n", (end_time - start_time));
    Serial.println("=========================================");
}
