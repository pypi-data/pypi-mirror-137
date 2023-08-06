#pragma once

#include <stdint.h>
#include <string.h>

#define HEADER1_BYTE 0x42
#define HEADER2_BYTE 0x42

#define CMD_INDEX 3
#define DATA_INDEX 4


enum PACKET_POSITION{H1, H2, LEN, CMD, DATA, CS, FIN};

bool protocol_parse_byte(uint8_t byte);
bool protocol_packet_complete();
void protocol_parse_packet(uint8_t *packet);
bool protocol_response_required();
uint8_t* protocol_get_response(size_t* length);
