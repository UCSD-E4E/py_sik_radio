'''Connection server
'''
import argparse

from serial import Serial
from serial.tools.list_ports import comports

from py_sik_radio.sik_radio import SikRadio


def main():
    """Connection server logic
    """
    ports = [port.name for port in comports() if port.pid == 0x6015]
    parser = argparse.ArgumentParser()

    parser.add_argument('port', type=str, choices=ports)
    parser.add_argument('--baudrate', type=int, choices=Serial.BAUDRATES, default=57600)

    args = parser.parse_args()

    with SikRadio(port=args.port, baudrate=args.baudrate) as radio:
        radio.timeout = 5
        while True:
            radio.write(radio.readline())

if __name__ == '__main__':
    main()
