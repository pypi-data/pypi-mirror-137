#pragma once
#include <stdint.h>
#include <string.h>
#include <stdbool.h>
#include "attr.h"

void disco_init(void);
bool disco_byte_handle(uint8_t byte);
bool disco_packet_complete();
void disco_packet_handle(uint8_t *packet);
bool disco_response_required(void);
uint8_t* disco_get_response(size_t* length);