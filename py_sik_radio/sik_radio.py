'''SiK Radio Control
'''
import re
from collections import OrderedDict
from time import sleep
from typing import Optional

from serial import Serial


# Modem = TypeVar('Modem', Serial)
class _CommandMode:
    def __init__(self,
                 modem: Serial,
                 start_mode: str = 'normal',
                 final_mode: str = 'normal') -> None:
        self.modem = modem
        self.__start_mode = start_mode
        self.__final_mode = final_mode

    def __enter__(self) -> None:
        self.start()

    def start(self):
        """Starts command mode

        Raises:
            RuntimeError: Failed to enter command mode
        """
        if self.__start_mode == 'normal':
            timeout = self.modem.timeout
            self.modem.timeout = 2
            sleep(1)
            self.modem.write(b'+++')
            serial_response = self.modem.readline().strip().decode(encoding='ascii')
            if "OK" != serial_response:
                raise RuntimeError(f'Got "{serial_response}", expected "OK"')
            self.modem.timeout = timeout

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.stop()

    def stop(self):
        """Stops the command mode
        """
        if self.__final_mode == 'normal':
            timeout = self.modem.timeout
            self.modem.timeout = 1
            self.modem.write(b'ATO\r')
            self.modem.readline().strip().decode(encoding='ascii')
            sleep(1)
            self.modem.timeout = timeout

# class SikRadioParameters:
#     """SiK Radio Parameters
#     """
#     def __init__(self,
#                  serial_speed: int = 57,
#                  air_speed: int = 64,
#                  netid: int = 25,
#                  txpower: int = 20,
#                  ecc: bool = True,
#                  mavlink: bool = True,
#                  op_resend: bool = True,
#                  min_freq: int = 915000,
#                  max_freq: int = 928000,
#                  num_channels: int = 50,
#                  duty_cycle: int = 100,
#                  lbt_rssi: bool = False,
#                  manchester: bool = False,
#                  rtscts: bool = False):
#         self.__serial_speed = serial_speed
#         self.__air_speed = air_speed
#         self.__netid = netid
#         self.__txpower = txpower
#         self.__ecc = ecc
#         self.__mavlink = mavlink
#         self.__op_resend = op_resend
#         self.__min_freq = min_freq
#         self.__max_freq = max_freq
#         self.__num_channels = num_channels
#         self.__duty_cycle = duty_cycle
#         self.__lbt_rssi = lbt_rssi
#         self.__manchester = manchester
#         self.__rtscts = rtscts

#     @property
#     def serial_speed(self) -> int:
#         return self.__serial_speed

#     @serial_speed.setter
#     def serial_speed(self, serial_speed: int) -> None:
#         if 2 <= serial_speed <= 115:
#             self.__serial_speed = serial_speed
#         else:
#             raise RuntimeError

#     @property
#     def air_speed(self) -> int:
#         return self.__air_speed

#     @air_speed.setter
#     def air_speed(self, air_speed: int) -> None:
#         if 2 <= air_speed <= 250:
#             self.__air_speed = air_speed
#         else:
#             raise RuntimeError

#     @property
#     def netid(self) -> int:
#         return self.__netid

#     @netid.setter
#     def netid(self, netid: int) -> None:
#         if 0 <= netid <= 499:
#             self.netid = netid
#         else:
#             raise RuntimeError

#     @property
#     def txpower(self) -> int:
#         return self.__txpower

#     @txpower.setter
#     def txpower(self, txpower: int) -> None:
#         if 0 <= txpower <= 30:
#             self.txpower = txpower
#         else:
#             raise RuntimeError

#     @property
#     def ecc(self) -> bool:
#         return self.__ecc

#     @ecc.setter
#     def ecc(self, ecc: bool) -> None:
#         self.__ecc = ecc

#     @property
#     def mavlink(self) -> bool:
#         return self.__mavlink

#     @mavlink.setter
#     def mavlink(self, mavlink: bool) -> None:
#         self.__mavlink = mavlink

#     @property
#     def op_resend(self) -> bool:
#         return self.__op_resend

#     @op_resend.setter
#     def op_resend(self, op_resend: bool) -> None:
#         self.__op_resend = op_resend

#     @property
#     def min_freq(self) -> int:
#         return self.__min_freq

#     @min_freq.setter
#     def min_freq(self, min_freq: int) -> None:
#         if 902000 <= min_freq <= 927000:
#             self.__min_freq = min_freq
#         else:
#             raise RuntimeError

#     @property
#     def max_freq(self) -> int:
#         return self.__max_freq

#     @max_freq.setter
#     def max_freq(self, max_freq: int) -> None:
#         if 903000 <= max_freq <= 928000:
#             self.__max_freq = max_freq
#         else:
#             raise RuntimeError

#     @property
#     def num_channels(self) -> int:
#         return self.__num_channels

#     @num_channels.setter
#     def num_channels(self, num_channels: int) -> None:
#         if 5 <= num_channels <= 50:
#             self.__num_channels = num_channels
#         else:
#             raise RuntimeError

#     @property
#     def duty_cycle(self) -> int:
#         return self.__duty_cycle

#     @duty_cycle.setter
#     def duty_cycle(self, duty_cycle: int) -> None:
#         if 10 <= duty_cycle <= 100:
#             self.__duty_cycle = duty_cycle
#         else:
#             raise RuntimeError

#     @property
#     def lbt_rssi(self) -> bool:
#         return self.__lbt_rssi

#     @lbt_rssi.setter
#     def lbt_rssi(self, lbt_rssi: bool) -> None:
#         self.__lbt_rssi = lbt_rssi

#     @property
#     def manchester(self) -> bool:
#         return self.__manchester

#     @manchester.setter
#     def manchester(self, manchester: bool) -> None:
#         self.manchester = manchester

#     @property
#     def rtscts(self) -> bool:
#         return self.__rtscts

#     @rtscts.setter
#     def rtscts(self, rtscts: bool) -> None:
#         self.__rtscts = rtscts

class SikRadio(Serial):
# pylint: disable=too-many-ancestors
# This is meant to be a wrapper to serial.Serial to enable SiK Radio control
    """SiK Radio Controller
    """
    key_map = {
        'FORMAT': 0,
        "SERIAL_SPEED": 1,
        'AIR_SPEED': 2,
        'NETID': 3,
        'TXPOWER': 4,
        'ECC': 5,
        'MAVLINK': 6,
        'OP_RESEND': 7,
        'MIN_FREQ': 8,
        'MAX_FREQ': 9,
        'NUM_CHANNELS': 10,
        'DUTY_CYCLE': 11,
        'LBT_RSSI': 12,
        'MANCHESTER': 13,
        'RTSCTS': 14,
        "MAX_WINDOW": 15
    }
    def __init__(self,
                 port: Optional[str],
                 baudrate: int,
                 *,
                 default_mode: str = "normal") -> None:
        super().__init__(
            port,
            baudrate)
        self.__default_mode = default_mode
        self.__mode = 'normal'

    def __get_command_response(self, cmd: str) -> str:
        with _CommandMode(self, start_mode=self.__mode, final_mode=self.__default_mode):
            output = self.__get_response(cmd)
        self.__mode = self.__default_mode
        return output.decode(encoding='ascii')

    def __get_response(self, cmd: str) -> bytes:
        timeout = self.timeout
        self.timeout = 0.1
        self.write(cmd.strip().encode(encoding='ascii') + b'\r')
        self.readline() # toss echo
        output = b''
        while (line := self.readline()) != b'':
            output += line
        self.timeout = timeout
        return output

    def get_radio_version(self) -> str:
        """Gets the radio version

        Returns:
            str: Radio Version
        """
        return self.__get_command_response('ATI').strip()

    def get_board_type(self) -> str:
        """Gets the board type

        Returns:
            str: Board type
        """
        return self.__get_command_response('ATI2').strip()

    def get_board_frequency(self) -> str:
        """Gets the board frequency

        Returns:
            str: Board frequency
        """
        return self.__get_command_response('ATI3').strip()

    def get_board_version(self) -> str:
        """Gets the board version

        Returns:
            str: Board version
        """
        return self.__get_command_response('ATI4').strip()

    def get_parameters(self) -> "OrderedDict[str, int]":
        """Retrieves all parameters

        Returns:
            OrderedDict[str, int]: Ordered dictionary of parameters
        """
        parameter_output = self.__get_command_response('ATI5')
        regex = r":(.*)=(.*)"
        matches = re.finditer(regex, parameter_output, re.MULTILINE)
        output = OrderedDict()
        for match in matches:
            output[match.groups()[0]] = int(match.groups()[1].strip())
        return output

    def get_timing_report(self) -> str:
        """Gets the timing report

        Returns:
            str: Timing report
        """
        return self.__get_command_response('ATI6')

    def get_signal_report(self) -> str:
        """Gets the signal report

        Returns:
            str: Signal report
        """
        return self.__get_command_response('ATI7')

    def reboot(self) -> None:
        """Reboots the radio for changes to take effect
        """
        with _CommandMode(self, start_mode=self.__mode, final_mode=self.__default_mode):
            timeout = self.timeout
            self.timeout = 1
            self.write(b'ATZ\r')
            self.read(3) # dump echo
            sleep(1)
            self.write(b'+++')
            output = b''
            while (line := self.read()) != b'':
                output += line
                if output == b'OK\r\n':
                    break
            self.timeout = timeout
        self.__mode = self.__default_mode

    def set_parameter(self, key: str, value: int) -> None:
        """Sets the specified parameter

        Args:
            key (str): Parameter key
            value (int): Parameter value

        Raises:
            RuntimeError: Failed to set parameter
        """
        key_idx = self.key_map[key.upper()]
        cmd = f'ATS{key_idx}={value}'

        response = self.__get_command_response(cmd)
        if response.strip() != 'OK':
            raise RuntimeError

    def get_parameter(self, key: str) -> int:
        """Gets the specified parameter

        Args:
            key (str): Parameter key

        Returns:
            int: Parameter value
        """
        key_idx = self.key_map[key.upper()]
        cmd = f'ATS{key_idx}?'
        return int(self.__get_command_response(cmd).strip())

    def write_parameter(self) -> None:
        """Writes parameters to EEPROM

        Raises:
            RuntimeError: Failed to write to EEPROM
        """
        if 'OK' != self.__get_command_response('AT&W').strip():
            raise RuntimeError

    def exit_command_mode(self) -> None:
        """Exits command mode
        """
        with _CommandMode(self, start_mode=self.__mode, final_mode='normal'):
            pass
