#include "attr.h"
#include "disco.h"
#include "protocol.h"

void disco_init() { attr_init(); }
bool disco_byte_handle(uint8_t byte) { return protocol_parse_byte(byte); }
bool disco_packet_complete() { return protocol_packet_complete(); }
void disco_packet_handle(uint8_t *packet) { protocol_parse_packet(packet); }
bool disco_response_required() { return protocol_response_required(); }
uint8_t* disco_get_response(size_t* length) { return protocol_get_response(length); }
