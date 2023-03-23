'''Test Configuration
'''
from time import sleep
from typing import Tuple

import pytest
from serial import Serial
from serial.tools import list_ports
from py_sik_radio.sik_radio import SikRadio

baudrates = [
    9600,
    57600,
    115200,
    76800,
    38400,
    28800,
    19200,
    4800,
    2400,
    1800,
    1200,
    230400,
]

@pytest.fixture(name='test_port', scope='session')
def get_test_port() -> Tuple[str, int]:
    """Discovers the test device

    Raises:
        RuntimeError: Failed to find a test device

    Returns:
        Tuple[str, int]: Port, baudrate
    """
    ports = list_ports.comports()
    port = [port.name for port in ports if port.pid == 0x6015][0]
    with Serial(port=port) as serial:
        serial.timeout = 1
        for baudrate in baudrates:
            serial.baudrate = baudrate
            sleep(1)
            serial.write(b'+++')
            output = serial.readline()
            if output != b'':
                serial.write(b'ATO\r')
                return (port, baudrate)
    raise RuntimeError('Could not find an AT Modem')

@pytest.fixture(name='test_radio')
def get_test_radio(test_port: Tuple[str, int]) -> SikRadio:
    """Configures a test radio

    Args:
        test_port (Tuple[str, int]): Test port information

    Returns:
        SikRadio: SiK Radio instance

    Yields:
        Iterator[SikRadio]: SiK Radio instance
    """
    with SikRadio(port=test_port[0], baudrate=test_port[1]) as radio:
        yield radio
