'''Connection server
'''
import argparse
import datetime as dt

from serial import Serial
from serial.tools.list_ports import comports

from py_sik_radio.sik_radio import SikRadio


def main():
    """Connection client logic
    """
    ports = [port.device for port in comports() if port.pid == 0x6015]
    parser = argparse.ArgumentParser()

    parser.add_argument('port', type=str, choices=ports)
    parser.add_argument('--baudrate', type=int, choices=Serial.BAUDRATES, default=57600)

    args = parser.parse_args()

    with SikRadio(port=args.port, baudrate=args.baudrate) as radio:
        while True:
            now = dt.datetime.now()
            radio.write(now.isoformat().encode() + b"\r\n")
            line = radio.readline()
            rx_time = dt.datetime.fromisoformat(line.strip().decode())
            delay = (rx_time - now).total_seconds()
            print(f'Delay: {delay}')

if __name__ == '__main__':
    main()
