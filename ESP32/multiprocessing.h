#pragma once
#include <Arduino.h>

extern EventGroupHandle_t syncGroup;

#define EVEN_DONE  (1 << 0)
#define ODD_DONE   (1 << 1)

void taskEven(void *param);

void taskOdd(void *param);