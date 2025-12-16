    #include "multiprocessing.h"
    #include "HX711.h"

    EventGroupHandle_t syncGroup;

    void taskEven(void *param){
        HX711 *hx711 = (HX711*)param;

        while (true) {
            for (uint8_t i = 0; i < PIN_COUNT; i += 2)
                hx711[i].RESULT = read(&hx711[i]);

            xEventGroupSetBits(syncGroup, EVEN_DONE);
            vTaskDelay(1);
        }
    }

    void taskOdd(void *param){
        HX711 *hx711 = (HX711*)param;
        while (true) {
            for (uint8_t i = 1; i < PIN_COUNT; i += 2)
                hx711[i].RESULT = read(&hx711[i]);
                    
            xEventGroupSetBits(syncGroup, ODD_DONE);
            vTaskDelay(1);
        }
    }