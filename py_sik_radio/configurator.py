'''Configures the radio from a file
'''
import argparse
import json
from pathlib import Path
from typing import Dict

from serial import Serial
from serial.tools.list_ports import comports

from py_sik_radio.sik_radio import SikRadio


def main():
    """Configuration script logic
    """
    ports = comports()
    port_names = [port.name for port in ports if port.pid == 0x6015]
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=str, choices=port_names)
    parser.add_argument('--baudrate', type=int, choices=Serial.BAUDRATES, default=57600)
    parser.add_argument('file', type=Path)

    args = parser.parse_args()

    with open(args.file, 'r', encoding='ascii') as handle:
        parameters: Dict[str, int] = json.load(handle)

    with SikRadio(port=args.port, baudrate=args.baudrate, default_mode='command') as radio:
        for key, value in parameters.items():
            radio.set_parameter(key=key, value=value)
            print(f'Set {key} to {value}')

        radio.write_parameter()
        radio.reboot()


if __name__ == '__main__':
    main()
