'''Connection server
'''
import argparse

from serial import Serial
from serial.tools.list_ports import comports

from py_sik_radio.sik_radio import SikRadio


def main():
    """Connection server logic
    """
    ports = [port.device for port in comports() if port.pid == 0x6015]
    parser = argparse.ArgumentParser()

    if len(ports) == 1:
        parser.add_argument('--port', type=str, choices=ports, default=ports[0], required=False)
    else:
        parser.add_argument('port', type=str, choices=ports)
    parser.add_argument('--baudrate', type=int, choices=Serial.BAUDRATES, default=57600)

    args = parser.parse_args()

    with SikRadio(port=args.port, baudrate=args.baudrate) as radio:
        radio.timeout = 1
        while True:
            radio.write(radio.readline())

if __name__ == '__main__':
    main()
