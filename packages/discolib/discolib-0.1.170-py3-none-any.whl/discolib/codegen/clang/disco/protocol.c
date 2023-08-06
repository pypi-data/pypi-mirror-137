#include "attr.h"
#include "disco.h"
#include "protocol.h"
#include "command.h"

static enum PACKET_POSITION POSITION = H1;
static uint32_t bytes_processed = 0;
static uint32_t bytes_expected = 0;
static bool response_required = false;

/**
 *  @brief Reset the state machine to expect a new packet.
 */
static void protocol_reset() {
    POSITION = H1;
    bytes_expected = bytes_processed = 0;
    response_required = false;
}

/**
 *  @brief Reset the state machine to expect a new packet.
 */
bool protocol_packet_complete() { 
    if (POSITION == FIN) {
        protocol_reset();
        return true;
    }
    return false;
}

/**
 *  @brief Indicates whether a response is required for the last-processed packet.
 *  @return True if a response is required, false otherwise.
 */
bool protocol_response_required() { return response_required; }

/**
 *  @brief Gets the contructed response for a command which requires a response.
 *  @param length A pointer to the length of the response (filled in by this function).
 *  @returns A pointer to the response packet.
 */
uint8_t* protocol_get_response(size_t* length) { return command_get_response(length); }

/**
 *  @brief Parse a single byte of a protocol packet according to the state machine.
 *  @param byte - A single byte in a protocol packet.
 *  @return Returns true if the byte is valid according to the protocol, false otherwise.
 *  @note If byte is invalid, a reset occurs and the protocol starts from the beginning.
 */
bool protocol_parse_byte(uint8_t byte) {
    switch (POSITION) {
        case H1:
            if (byte != HEADER1_BYTE) {
                protocol_reset();
                return false;
            }
            POSITION = H2;
            break;
        case H2:
            if (byte != HEADER2_BYTE) {
                protocol_reset();
                return false;
            }
            POSITION = LEN;
            break;
        case LEN:
            bytes_expected = byte;
            POSITION = DATA;
            break;
        case CMD:
        case DATA:
            bytes_processed++;
            if (bytes_processed == (bytes_expected - 1)) {
                POSITION = CS;
            }
            break;
        case CS:
            // TODO: Compute checksum
            POSITION = FIN;
            break;
        case FIN:
        default:
            protocol_reset();
            return false;
    }
    return true;
}

/**
 *  @brief Respond to an entire validated packet.
 *  @param packet A packet that has been validated byte-by-byte.
 */
void protocol_parse_packet(uint8_t *packet) {
    uint8_t cmd = packet[CMD_INDEX];
    if (command_response_required(cmd)) response_required = true;
    command_handle(cmd, &packet[DATA_INDEX]);
}
