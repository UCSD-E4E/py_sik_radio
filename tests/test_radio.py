'''Tests SiK Radio Commands
'''
from typing import Tuple

from py_sik_radio.sik_radio import SikRadio


def test_ati(test_port: Tuple[str, int]):
    """Tests the ATI commmand

    Args:
        test_port (Tuple[str, int]): Test Port information
    """
    with SikRadio(
                port=test_port[0],
                baudrate=test_port[1]
            ) as radio:
        radio_version = radio.get_radio_version()
    assert radio_version.find('SiK') != -1

def test_ati2(test_port: Tuple[str, int]):
    """Tests the ATI2 command

    Args:
        test_port (Tuple[str, int]): Test Port information
    """
    with SikRadio(*test_port) as radio:
        board_type = radio.get_board_type()
    assert board_type

def test_ati3(test_radio: SikRadio):
    """Tests the ATI3 command

    Args:
        test_radio (SikRadio): Test Port
    """
    board_freq = test_radio.get_board_frequency()
    assert board_freq

def test_ati4(test_radio: SikRadio):
    """Tests the ATI4 command

    Args:
        test_radio (SikRadio): Test device
    """
    board_version = test_radio.get_board_version()
    assert board_version

def test_ati5(test_radio: SikRadio):
    """Tests the ATI5 command

    Args:
        test_radio (SikRadio): Test device
    """
    board_params = test_radio.get_parameters()
    assert all (isinstance(key, str) for key in  board_params.keys())
    assert all (isinstance(val, int) for val in  board_params.values())

def test_atz(test_radio: SikRadio):
    """Tests the ATZ command

    Args:
        test_radio (SikRadio): Test device
    """
    version = test_radio.get_board_version()
    assert version != ''
    test_radio.reboot()
    assert test_radio.get_board_version() == version

def test_set_netid(test_radio: SikRadio):
    """Tests getting and setting the netid parameter

    Args:
        test_radio (SikRadio): Test device
    """
    net_id = test_radio.get_parameter('NETID')
    test_radio.set_parameter('NETID', net_id + 1)
    new_id = test_radio.get_parameter('NETID')
    assert new_id == net_id + 1
    test_radio.set_parameter('NETID', net_id)
    assert net_id == test_radio.get_parameter('NETID')
