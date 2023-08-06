"""
main submodule, implementing / handling the SI Station
"""

import time
from datetime import datetime, timedelta
from typing import List, Optional, Union

from serial import Serial, SerialException

from sipyconfig.card import SI5, SI6, SI8To10, SICard
from sipyconfig.comms import ACK, NOACK, Command, receive_command, send_command
from sipyconfig.enums import (CPC, SETTINGS, SiCardInserted, SiCardRemoved,
                              SiError, com, memaddr, memlen, misc, mode_rev,
                              proto, stationmode)
from sipyconfig.utils import (apply_bit_mask, array_or, bytes_to_int, is_siac_mode,
                              is_siac_special_mode, log2)

STANDARD_PORT = "/dev/ttyUSB{0:d}"
STANDARD_SERIAL_TIMEOUT = 5
BAUDRATE_EXTENDED = 38400
BAUDRATE_STANDARD = 4800
STANDARD_MAX_COMMAND_TRIES = 32

class SiUSBStation():
    """main class for interfacing with the SI Station
    NOTE: only stations with extended protocol are currently supported"""
    _dev: 'Serial' = None
    _device_port: str
    _extended_protocol: bool = True
    _direct_mode: Optional[bool] = None

    _mem_size: int = -1
    _sys_data: List[int]

    _cpc: int = -1
    _cpc_ext_protocol: bool
    _auto_send: bool
    _handshake: bool
    _access_password: bool
    _read_after_punch: bool

    _setting: int = -1
    _optical_feedback: bool
    _acoustic_feedback: bool
    _control_number_high_bit: bool

    _operating_time: int = -1

    _control_number: int = -1
    _mode: stationmode = stationmode.UNKNOWN
    _mode_str: str = "UNKNOWN"

    _si_card: Optional[SICard] = None
    _time: 'datetime'
    _time_read_at: 'datetime'

    _command_tries: int = 0
    _serial_timeout: float = STANDARD_SERIAL_TIMEOUT
    _max_command_tries: int = STANDARD_MAX_COMMAND_TRIES
    _currently_waiting: bool = False

    def __init__(self, device: str = None, mode_direct: bool = True) -> None:
        self._sys_data = []

        self._init_serial(device)
        self._station_detect_procedure()
        self.set_mode_direct(mode_direct)
        self.get_system_info()

    def _init_serial(self, device: str = None, baudrate: int = BAUDRATE_EXTENDED) -> None:
        if self._dev:
            self._dev.close()
        if device:
            self._dev = Serial(device, baudrate=baudrate, timeout=self._serial_timeout)
            if self._dev is None:
                raise SiError("Could not open device!")
            self._device_port = device
            self.flush()
            return
        for i in range(128):
            try:
                self._dev = Serial(STANDARD_PORT.format(i), baudrate, timeout=self._serial_timeout)
                self._device_port = STANDARD_PORT.format(i)
                self.flush()
                return
            except SerialException:
                continue
        raise SiError("Could not open device!")

    def _station_detect_procedure(self) -> bool:
        self._extended_protocol = True
        if self.set_mode_direct():
            return True
        self._init_serial(self._device_port, BAUDRATE_STANDARD)
        if self.set_mode_direct():
            self.set_baudrate()
            self._init_serial(self._device_port, BAUDRATE_EXTENDED)
            self.set_mode_direct()
            return True
        self._extended_protocol = False
        self.set_mode_direct()
        if isinstance(self.receive_command(), NOACK):
            raise ConnectionError("Could not connect to SI-Station!")
        return True

    def set_mode_direct(self, set_mode_direct: bool = True) -> bool:
        """set the station into direct (True) or remote (False) mode"""
        command = com.SET_MS_MODE if self.support_extended_protocol else com.SET_MS_MODE_BASIC
        mode = misc.MODE_DIRECT if set_mode_direct else misc.MODE_REMOTE
        ret = self.send_command(command, [mode], False)
        if isinstance(ret, NOACK):
            self._direct_mode = None
            return False
        if isinstance(ret, Command):
            if ret.is_extended_command:
                self._direct_mode = ret.data[2] == misc.MODE_DIRECT
                self._control_number = (ret.data[0] << 8) + ret.data[1]
            else:
                self._direct_mode = ret.data[1] == misc.MODE_DIRECT
                self._control_number = ret.data[0]
        return True

    def set_baudrate(self, high_baudrate: bool = True) -> None:
        """set the baudrate of the station to the defined lower (False) or higher (True) baudrate"""
        self.send_command(com.SET_BAUDRATE, [int(high_baudrate)], True)

    def get_system_info(self) -> None:
        """retreive the system info from the station"""
        ret = self.send_command(com.GET_SYS_DATA, [memaddr.MEM_SIZE, memlen.MEM_SIZE], True)
        if isinstance(ret, Command):
            self._mem_size = ret.data[misc.DATA_COMMAND_OFFSET]
            ret = self.send_command(com.GET_SYS_DATA, [0x00, self._mem_size], True)
            if isinstance(ret, Command):
                self._sys_data = [x for x in ret.data[misc.DATA_COMMAND_OFFSET:]]

                cn1, cn0 = ret.data[0], ret.data[1]
                self._control_number = (cn1 << 8) + cn0

                self._mode = stationmode(self._sys_data[memaddr.MODE])
                if self._mode == stationmode.SIAC_SPECIAL:
                    self._control_number = self._sys_data[memaddr.CONTROL_NUMBER]
                    self._mode_str = mode_rev.get(self._control_number, "UNKNOWN")
                else:
                    self._mode_str = mode_rev.get(self._mode, "UNKNOWN")

                self._setting = self._sys_data[memaddr.SETTINGS_FLAG]
                self._optical_feedback = bool(self._setting & SETTINGS.OPTICAL_FEEDBACK)
                self._acoustic_feedback = bool(self._setting & SETTINGS.ACOUSTIC_FEEDBACK)
                self._control_number_high_bit = bool(self._setting & SETTINGS.NUMBER_HIGH_BIT)

                self._cpc = self._sys_data[memaddr.PROTOCOL_MODE_FLAG]
                self._cpc_ext_protocol = bool(self._cpc & CPC.EXTENDED_PROTCOL)
                self._auto_send = bool(self._cpc & CPC.AUTO_SEND)
                self._handshake = bool(self._cpc & CPC.HANDSHAKE)
                self._access_password = bool(self._cpc & CPC.ACCESS_PASSWORD)
                self._read_after_punch = bool(self._cpc & CPC.READ_AFTER_PUNCH)

                self._operating_time = bytes_to_int(self._sys_data[memaddr.ACTIVE_TIME:memaddr.ACTIVE_TIME+memlen.ACTIVE_TIME])
        self.get_time()

    def get_time(self) -> None:
        """get the current time of the station"""
        ret = self.send_command(com.GET_TIME, [], True)
        if isinstance(ret, Command):
            self._time = self._decode_time(ret.data[2:])
            self._time_read_at = datetime.now()

    def _decode_time(self, raw_data: bytes) -> 'datetime':
        year = 2000 + raw_data[0]
        month = raw_data[1]
        day = raw_data[2]
        month = month if 1 <= month <= 12 else 1
        day = day if 1 <= day <= 31 else 1
        seconds = bytes_to_int(raw_data[4:6])
        hour = seconds // 3600
        seconds -= hour * 3600
        minute = seconds // 60
        seconds -= minute * 60
        microseconds = int(raw_data[6] * (1e6 / 256))

        ret_time = datetime(year, month, day, hour, minute, seconds, microseconds)

        if (raw_data[3] << 7) & 0xFF:
            ret_time += timedelta(hours=12)
        return ret_time

    def set_time(self, time_: 'datetime' = None) -> None:
        """set the current time of the station, if time_ is omitted the current computer time will be set"""
        if time_ is None:
            time_ = datetime.now()
        self.send_command(com.SET_TIME, self._encode_time(time_), True)

    def _encode_time(self, time_: 'datetime') -> 'bytes':
        data = [
            time_.year - 2000,
            time_.month,
            time_.day,
            ((time_.weekday() + 1) % 7) << 1
        ]
        if time_.hour >= 12:
            data[3] |= 0x01
            time_ -= timedelta(hours=12)
        seconds = time_.hour * 3600 + time_.minute * 60 + time_.second
        data.extend([x for x in seconds.to_bytes(2, "big")])
        data.append(0x00)
        return bytes(data)

    def set_operating_time(self, operating_time: int) -> None:
        """set the operating time span of the station in minutes, (2-5759)"""
        self.send_command(com.SET_SYS_DATA, bytes([memaddr.ACTIVE_TIME]) + operating_time.to_bytes(2, "big"))
        self.get_system_info()

    def _splice_control_number(self, sys_data: List[int], num: int) -> List[int]:
        sys_data[memaddr.CONTROL_NUMBER] = num & 0xFF
        sys_data[memaddr.SETTINGS_FLAG] = self._setting | SETTINGS.NUMBER_HIGH_BIT if num > 255 else self._setting & ~SETTINGS.NUMBER_HIGH_BIT
        return sys_data

    def set_control_number(self, num: int) -> None:
        """set the control number of the station, supported range (1-511). IMPORTANT: some older SI Chip only support numbers till 255!"""
        if not 0 < num < 512:
            raise ValueError("Only supports values between 1 and 511")
        sys_data = self._splice_control_number(self._sys_data.copy(), num)
        self.send_command(com.SET_SYS_DATA, [int(memaddr.CONTROL_NUMBER)] + sys_data[memaddr.CONTROL_NUMBER:memaddr.SETTINGS_FLAG+1], True)
        self.get_system_info()

    def set_mode(self, mode: stationmode) -> None:
        """set the operating mode of the station"""
        sys_copy = self._sys_data.copy()
        if mode == stationmode.SIAC_TEST:
            sys_copy = self._splice_control_number(sys_copy, stationmode.SIAC_ON)
        elif is_siac_special_mode(mode):
            sys_copy = self._splice_control_number(sys_copy, mode)
            mode = stationmode.SIAC_SPECIAL
        sys_copy[memaddr.SIAC] = misc.SIAC_ON if is_siac_mode(mode) else misc.SIAC_OFF
        sys_copy[memaddr.MODE] = mode
        self.send_command(com.SET_SYS_DATA, [int(memaddr.SIAC)] + sys_copy[memaddr.SIAC:memaddr.SETTINGS_FLAG+1], True)
        self.get_system_info()

    def set_protocol_setting(self, setting: CPC, set_val: bool):
        """set a single setting of the protocol settings byte"""
        sett = apply_bit_mask(self._cpc, setting, set_val)
        if setting in [CPC.AUTO_SEND, CPC.HANDSHAKE]:
            setting = CPC.AUTO_SEND if setting == CPC.HANDSHAKE else CPC.HANDSHAKE
            sett = apply_bit_mask(sett, setting, set_val)
        self.send_command(com.SET_SYS_DATA, [memaddr.PROTOCOL_MODE_FLAG, sett], True)

    def set_protocol_settings(self, settings: List[CPC], values: List[int]) -> None:
        """set multiple settings of the protocol settings byte at once. length of settings and values has to be equal"""
        values = [val << log2(sett - 1) for sett, val in zip(settings, values)]
        self.send_command(com.SET_SYS_DATA,
                        [memaddr.PROTOCOL_MODE_FLAG, apply_bit_mask(self._cpc, array_or([int(x) for x in settings]), array_or(values))], True)
        self.get_system_info()

    def set_setting(self, setting: SETTINGS, set_val: bool):
        """set a single setting of the settings byte"""
        self.send_command(com.SET_SYS_DATA, [memaddr.SETTINGS_FLAG, apply_bit_mask(self._setting, setting, set_val << setting)], True)

    def set_settings(self, settings: List[SETTINGS], values: List[int]) -> None:
        """set multiple settings of the settings byte at once. length of settings and values has to be equal"""
        values = [val << log2(sett - 1) for sett, val in zip(settings, values)]
        self.send_command(com.SET_SYS_DATA,
                        [memaddr.SETTINGS_FLAG, apply_bit_mask(self._setting, array_or([int(x) for x in settings]), array_or(values))], True)
        self.get_system_info()

    def turn_off(self) -> None:
        """Turn off the connected station, is only effective in remote mode (mode_direct = False)"""
        self.send_command(com.TURN_OFF, [], True)

    def trigger_feedback(self, num: int = 1) -> bool:
        """Trigger acoustic and/or visual feedback of the station <num> times"""
        self.send_command(com.FEEDBACK, [num])
        return not isinstance(self.receive_command(), NOACK)

    def ensure_readout(self) -> None:
        """ensures that the station is set to direct mode and is in mode READOUT"""
        self.flush()
        self.set_mode_direct(True)
        self.set_mode(stationmode.READOUT)

    def wait_for_si_card(self, timeout: float = None, *, no_ack: bool = False) -> Optional[SICard]:
        """waits for an SiCard to be inserted, waits a maximum of timeout (infinite if unset),
        returns a SICard object or None if timeout
        if no_ack is set True, no ACK packet will be sent to the station"""
        invoke_time = time.time()
        if self._currently_waiting:
            return None
        while True:
            self._currently_waiting = True
            try:
                self.receive_command()
            except SiCardInserted:
                if self._si_card:
                    self._si_card.read_out_data(no_ack=no_ack)
                return self._si_card
            except SiCardRemoved:
                pass
            finally:
                self._currently_waiting = False
            if timeout is not None and time.time() - invoke_time >= timeout:
                return None

    def sendACK(self): # pylint: disable=invalid-name
        """send a ACK packet to the station"""
        self._dev.write([proto.ACK])

    def sendNAK(self): # pylint: disable=invalid-name
        """send a NOACK packet to the station"""
        self._dev.write([proto.NAK])

    def send_command(self, command_code: com, data: Union[bytes, List[int]], retry: bool = True) -> Union[ACK, NOACK, Command]:
        """send a command to the station with data, if retry = True the command is retried a maximum of max_command_tries if receiving a NOACK response"""
        send_command(command_code, data, self._dev)
        ret = self.receive_command()
        if not retry:
            return ret
        if isinstance(ret, Command) and ret.command_code != command_code:
            return NOACK()
        if isinstance(ret, NOACK):
            self._command_tries += 1
            if self._command_tries > self.max_command_tries:
                self._command_tries = 0
                raise SiError("Max tries for command reached!")
            return self.send_command(command_code, data)
        self._command_tries = 0
        return ret

    def receive_command(self) -> Union[Command, ACK, NOACK]:
        """receive a command from the station, might raise SiCardEventError if SICard is inserted or removed while waiting on a response."""
        ret = receive_command(self._dev)
        if isinstance(ret, Command):
            if ret.command_code == com.DETECT_SI_5:
                self._si_card = SI5(ret.data[2:], self)
                raise SiCardInserted("SI-Card insert during command.")
            elif ret.command_code == com.DETECT_SI_6:
                self._si_card = SI6(ret.data[2:], self)
                raise SiCardInserted("SI-Card insert during command.")
            elif ret.command_code == com.DETECT_SI_8:
                self._si_card = SI8To10.switch_types(ret.data[2:], self)
                raise SiCardInserted("SI-Card insert during command.")
            elif ret.command_code == com.SI_REMOVED:
                raise SiCardRemoved("SI-Card removed during command.")
        return ret

    def flush(self, flush_input: bool = True, flush_output: bool = True):
        """flush input and output buffer of the serial interface"""
        if flush_input:
            self._dev.flushInput()
        if flush_output:
            self._dev.flushOutput()

    @property
    def memory_size(self) -> Optional[int]:
        """system memory size of the station in bytes"""
        return getattr(self, "_mem_size", None)

    @property
    def max_command_tries(self) -> int:
        """maximum number of command retries if receiving NOACK as response"""
        return self._max_command_tries

    @max_command_tries.setter
    def max_command_tries(self, tries: int):
        self.set_max_command_tries(tries)

    def set_max_command_tries(self, tries: int):
        """set max_command_tries"""
        self._max_command_tries = tries

    @property
    def direct_mode(self) -> Optional[bool]:
        "whether the station operates in direct (True) or remote (False) mode"
        return getattr(self, "_direct_mode", None)

    @direct_mode.setter
    def direct_mode(self, set_mode_direct: bool):
        self.set_mode_direct(set_mode_direct)

    @property
    def support_extended_protocol(self) -> Optional[bool]:
        """whether the station supports the extended protocol, note that only those station are currently supported"""
        return getattr(self, "_extended_protocol", None)

    @property
    def cpc_extended_prototcol(self) -> Optional[bool]:
        """whether the extended protocol flag is set"""
        return getattr(self, "_cpc_ext_protocol", None)

    @property
    def auto_send(self) -> Optional[bool]:
        """whether autosend for readout is enabled, currently this is not supported"""
        return getattr(self, "_auto_send", None)

    @auto_send.setter
    def auto_send(self, autosend: bool) -> None:
        self.set_protocol_setting(CPC.AUTO_SEND, autosend)

    @property
    def handshake(self) -> Optional[bool]:
        """whether handshake mode for readout is enabled, currently this is the only mode supported"""
        return getattr(self, "_handshake", None)

    @handshake.setter
    def handshake(self, handshake: bool):
        self.set_protocol_setting(CPC.HANDSHAKE, handshake)

    @property
    def access_with_password(self) -> Optional[bool]:
        """the the access with password flag is set"""
        return getattr(self, "_access_password", None)

    @property
    def read_after_punch(self) -> Optional[bool]:
        """whether the read after punch flag is set"""
        return getattr(self, "_read_after_punch", None)

    @read_after_punch.setter
    def read_after_punch(self, read_after_punch: bool):
        self.set_protocol_setting(CPC.READ_AFTER_PUNCH, read_after_punch)

    @property
    def optical_feedback(self) -> Optional[bool]:
        """whether optical feedback is enabled"""
        return getattr(self, "_optical_feedback", None)

    @optical_feedback.setter
    def optical_feedback(self, optical_feedback: bool):
        self.set_setting(SETTINGS.OPTICAL_FEEDBACK, optical_feedback)

    @property
    def acoustic_feedback(self) -> Optional[bool]:
        """whether acoustic feedback is enabled"""
        return getattr(self, "_acoustic_feedback", None)

    @acoustic_feedback.setter
    def acoustic_feedback(self, acoustic_feedback: bool):
        self.set_setting(SETTINGS.ACOUSTIC_FEEDBACK, acoustic_feedback)

    @property
    def operating_time(self) -> int:
        """currently configurate operating time in minutes"""
        return self._operating_time

    @operating_time.setter
    def operating_time(self, operating_time: int):
        self.set_operating_time(operating_time)

    @property
    def control_number(self) -> Optional[int]:
        """current control number"""
        return getattr(self, "_control_number", None)

    @control_number.setter
    def control_number(self, control_number: int):
        self.set_control_number(control_number)

    @property
    def mode(self) -> stationmode:
        """current operating mode"""
        return self._mode

    @mode.setter
    def mode(self, mode: stationmode) -> None:
        self.set_mode(mode)

    @property
    def mode_string(self) -> str:
        """string name of the current operating mode"""
        return self._mode_str

    @property
    def time(self) -> Optional[datetime]:
        """current time of the station, calculated with the read out time and the timedelta since the readout"""
        if self._time and self._time_read_at:
            return self._time + (datetime.now() - self._time_read_at)
        return None
