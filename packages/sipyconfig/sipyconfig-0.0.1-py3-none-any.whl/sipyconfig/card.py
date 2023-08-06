"""
submodule for handling SI Cards and readout.
"""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from sipyconfig.comms import Command
from sipyconfig.enums import SiCardError, SiError, com, SIAC_BEEP, siac_rev
from sipyconfig.utils import bytes_to_int

if TYPE_CHECKING:
    from sipyconfig import SiUSBStation
    from typing import Dict, List, Optional, Union, Tuple


class Punch():
    """
    Information about a control punch.
    Control Number and if available time code
    """
    time: 'Optional[datetime]' = None
    control: int

    def __init__(self, control_number: int, time: 'Optional[datetime]') -> None:
        self.time = time
        self.control = control_number

    @classmethod
    def from_bytes(cls, control_number: int, raw_time: bytes, punchdate: int = None, reftime: 'datetime' = None) -> 'Punch':
        """
        construct Punch class from the byte data
        """
        punchtime = SICard.decode_time(raw_time, punchdate, reftime)
        return Punch(control_number, punchtime)

    def __str__(self) -> str:
        return f"Punch {self.control} at {self.time}"

    def __repr__(self) -> str:
        return f"Punch({self.control.__repr__()}, {self.time.__repr__()})"


class SICard():
    """
    Meta class for the different SICard types
    """
    CN2: int = -1
    CN1: int = -1
    CN0: int = -1
    STD: int = -1
    ST: int = -1
    STR: int = -1
    FTD: int = -1
    FT: int = -1
    FTR: int = -1
    CTD: int = -1
    CT: int = -1
    LTD: int = -1
    LT: int = -1
    LTR: int = -1
    RC: int = -1
    P1: int = -1
    PL: int = -1
    PTR: int = -1
    PM: int = -1
    CN: int = -1
    PTD: int = -1
    PTH: int = -1
    PTL: int = -1
    BC: int = -1
    SPD: int = -1
    EPD: int = -1

    TIME_RESET = b'\xEE\xEE'

    _number: int
    _station: 'SiUSBStation'
    _start_time: 'Optional[datetime]' = None
    _start_reserve: 'Optional[datetime]' = None
    _finish_time: 'Optional[datetime]' = None
    _finish_reserve: 'Optional[datetime]' = None
    _check_time: 'Optional[datetime]' = None
    _clear_time: 'Optional[datetime]' = None
    _clear_reserve: 'Optional[datetime]' = None

    _read_at: 'Optional[datetime]' = None

    _punches: 'List[Punch]'

    _personal_data: 'Dict[str, str]'
    _other_data: 'Dict[str, Union[float, str, datetime]]'

    @staticmethod
    def decode_number(data: 'Union[bytes, List[int]]') -> int:
        """
        Handles decoding the SICard number from bytes. With SICard 5 special case
        """
        if data[0] != 0x00:
            raise SiCardError("Unknown SI-Card!")
        num = bytes_to_int(data[1:4])
        if num < 500000:
            # SI Card 5
            num2 = bytes_to_int(data[2:4])
            if data[1] < 2:
                return num2
            return data[1]*100000 + num
        return num

    @property
    def number(self) -> int:
        """Number of the SICard"""
        return self._number

    @property
    def read_at(self) -> 'Optional[datetime]':
        """Date and time of the last read"""
        return getattr(self, "_read_at", None)

    @property
    def starttime(self) -> 'Optional[datetime]':
        """recorded start time"""
        return getattr(self, "_start_time", None)

    @property
    def starttime_reserve(self) -> 'Optional[datetime]':
        """recorded start time reserve"""
        return getattr(self, "_start_reserve", None)

    @property
    def finishtime(self) -> 'Optional[datetime]':
        """recorded finish time"""
        return getattr(self, "_finish_time", None)

    @property
    def finishtime_reserve(self) -> 'Optional[datetime]':
        """recorded finish time reserve"""
        return getattr(self, "_finish_reserve", None)

    @property
    def checktime(self) -> 'Optional[datetime]':
        """recorded check time"""
        return getattr(self, "_check_time", None)

    @property
    def cleartime(self) -> 'Optional[datetime]':
        """recorded clear time (only SI6, else see cleartime_reserve)"""
        return getattr(self, "_clear_time", None)

    @property
    def cleartime_reserve(self) -> 'Optional[datetime]':
        """recorded clear time reserve (only SI10 and up)"""
        return getattr(self, "_clear_reserve", None)

    @property
    def punches(self) -> 'List[Punch]':
        """list of recorded punches"""
        return getattr(self, "_punches", [])

    @property
    def personal_data(self) -> 'Dict[str, str]':
        """dict of the stored personal data.
        to edit data modify this dict and call write_personal_data (edit only SI10 and up)"""
        return getattr(self, "_personal_data", {})

    @property
    def other_data(self) -> 'Dict[str, str]':
        """other data stored in the SICard, such as hardware and firmware version (only SI10 and up)"""
        return getattr(self, "_other_data", {})

    def read_out_data(self, *, no_ack: bool = False) -> None:
        """read out data from SICard"""
        raise NotImplementedError

    def process_read_out(self, data: bytes, reftime: 'datetime' = None):
        """process the read out data from a SICard"""
        self._read_at = datetime.now()
        self._number = self.decode_number([0x00, data[self.CN2], data[self.CN1], data[self.CN0]])
        self._start_time = self.decode_time(data[self.ST:self.ST+2], data[self.STD] if self.STD != -1 else None, reftime)
        self._finish_time = self.decode_time(data[self.FT:self.FT+2], data[self.FTD] if self.FTD != -1 else None, reftime)
        self._check_time = self.decode_time(data[self.CT:self.CT+2], data[self.CTD] if self.CTD != -1 else None, reftime)
        if self.LT != -1:
            self._clear_time = self.decode_time(data[self.LT:self.LT+2], data[self.LTD] if self.LTD != -1 else None, reftime)
        if self.STR != -1:
            self._start_reserve = self.decode_time(data[self.STR+2:self.STR+4], data[self.STR], reftime)
        if self.FTR != -1:
            self._finish_reserve = self.decode_time(data[self.FTR+2:self.FTR+4], data[self.FTR], reftime)
        if self.LTR != -1:
            self._clear_reserve = self.decode_time(data[self.LTR+2:self.LTR+4], data[self.LTR], reftime)

        self.process_extra_data(data)

        punch_count = data[self.RC]
        if isinstance(self, SI5):
            punch_count -= 1
        if punch_count > self.PM:
            punch_count = self.PM

        self._punches = []
        if not isinstance(self, SI5):
            for punch_pointer in range(self.P1, self.P1 + data[self.RC] * self.PL, self.PL):
                punch_control = data[punch_pointer + self.CN]
                punch_time = data[punch_pointer + self.PTH:punch_pointer + self.PTL + 1]

                punch_date = None
                if self.PTD != -1:
                    punch_date = data[punch_pointer + self.PTD]
                    punch_control += (punch_date << 2) & ~0xFF

                self._punches.append(Punch.from_bytes(punch_control, punch_time, punch_date, reftime))

    def process_extra_data(self, data: bytes):
        """process any non standard data from the SICard read out"""
        raise NotImplementedError

    @classmethod
    def decode_time(cls, raw_time: bytes, punchdate: int = None, reftime: 'datetime' = None) -> 'Optional[datetime]':
        """decode date and time from bytes before reftime"""
        if raw_time == cls.TIME_RESET:
            return None

        if reftime is None:
            reftime = datetime.now() + timedelta(hours=2)

        punchtime = timedelta(seconds=bytes_to_int(raw_time))

        if punchdate is not None:
            # adjust for am or pm
            if punchdate & 0b00000001:
                punchtime += timedelta(hours=12)

            # extract day of week (%7 for sunday = -1)
            day_of_week = (((punchdate & 0b00001110) >> 1) - 1) % 7

            if reftime.weekday() == day_of_week and punchtime > timedelta(hours=reftime.hour, minutes=reftime.minute, seconds=reftime.second):
                reftime -= timedelta(days=7)
            else:
                reftime -= timedelta(days=(reftime.weekday() - day_of_week) % 7)

            ref_day = reftime.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
            return ref_day + punchtime

        # no punchdate available
        ref_day = reftime.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        ref_hour = reftime - ref_day
        t_noon = timedelta(hours=12)

        if ref_hour < t_noon:
            # reference time is before noon
            if punchtime < ref_hour:
                # t is between 0:00 and t_ref
                return ref_day + punchtime
            else:
                # t is afternoon the day before
                return ref_day - t_noon + punchtime
        else:
            # reference is after noon
            if punchtime < ref_hour - t_noon:
                # t is between noon and t_ref
                return ref_day + t_noon + punchtime
            else:
                # t is in the late morning
                return ref_day + punchtime

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.number} with {len(self.punches)} Punches"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.number} at {hex(id(self))}>"


class SI5(SICard):
    """SICard 5, numbers 4.000 - 49.999"""
    CN2 = 0x6
    CN1 = 0x4
    CN0 = 0x5
    ST = 0x13
    FT = 0x15
    CT = 0x19
    RC = 0x17
    P1 = 0x20
    PL = 0x3
    PM = 30  # punches 31-36 have no time
    CN = 0x0
    PTH = 0x1
    PTL = 0x2

    def __init__(self, data: bytes, station: 'SiUSBStation' = None):
        self._number = self.decode_number(data)
        if station:
            self._station = station
        self._read_at = datetime.now()

    def read_out_data(self, *, no_ack: bool = False) -> None:
        if not self._station:
            raise AttributeError("SICard needs to be invoked with station!")

        ret = self._station.send_command(com.GET_SI_5, [], True)
        if not isinstance(ret, Command):
            raise SiError("Can't read Si-Card!")

        self.process_read_out(ret.data[2:])
        if not no_ack:
            self._station.sendACK()

    def process_read_out(self, data: bytes, reftime: 'datetime' = None):
        super().process_read_out(data, reftime)

        no_time_punches = []

        punch_count = data[self.RC] - 1
        if punch_count > self.PM:
            punch_count = self.PM
        punch_pointer = self.P1
        for punch_counter in range(punch_count): # pylint: disable=unused-variable
            if punch_pointer % 16 == 0:
                # first byte of each block is reserved for punches 31 - 36
                if data[punch_pointer]:
                    no_time_punches.append(Punch(data[punch_pointer], None))
                punch_pointer += 1

            punch_control = data[punch_pointer + self.CN]
            punch_time = data[punch_pointer + self.PTH:punch_pointer + self.PTL + 1]
            punch_date = data[punch_pointer + self.PTD] if self.PTD != -1 else None

            self._punches.append(Punch.from_bytes(punch_control, punch_time, punch_date, reftime))
            punch_pointer += self.PL
        self.punches.extend(no_time_punches)

    def process_extra_data(self, data: bytes):
        pass


class SI6(SICard):
    """SICard 6, numbers 500.000 - 999.999"""
    CN2 = 0xb
    CN1 = 0xc
    CN0 = 0xd
    STD = 0x18
    ST = 0x1a
    FTD = 0x14
    FT = 0x16
    CTD = 0x1c
    CT = 0x1e
    LTD = 0x20
    LT = 0x22
    RC = 0x12
    P1 = 0x80
    PL = 0x4
    PM = 64
    PTD = 0x0
    CN = 0x1
    PTH = 0x2
    PTL = 0x3

    _personal_structure: 'Dict[str, Tuple[int,int]]' = {
        "last_name": (0x30, 0x43),
        "first_name": (0x44, 0x57),
        "country": (0x58, 0x5B),
        "club": (0x5C, 0x7f),
        "user_id": (0x80, 0x8f),
        "phone": (0x90, 0x9F),
        "email": (0xA0, 0xC3),
        "street": (0xC4, 0xD7),
        "city": (0xD8, 0xE7),
        "zip": (0xE8, 0xEF),
        "sex": (0xF0, 0xF3),
        "birth": (0xF4, 0xFB)
    }

    SI6_STAR = b'\x01\x01\x01\x02'

    def __init__(self, data: bytes, station: 'SiUSBStation' = None):
        self._number = bytes_to_int(data)
        if station:
            self._station = station
        self._read_at = datetime.now()

    def read_out_data(self, *, no_ack: bool = False) -> None:
        if not self._station:
            raise AttributeError("SICard needs to be invoked with station!")

        ret = self._station.send_command(com.GET_SI_6, [0x00], True)
        if not isinstance(ret, Command):
            raise SiError("Can't read Si-Card!")
        raw_data = ret.data[3:]

        for i in range(2): # pylint: disable=unused-variable
            ret2 = self._station.receive_command()
            if not isinstance(ret2, Command):
                raise SiError("Can't read Si-Card!")
            raw_data += ret2.data[3:]

        self.process_read_out(raw_data)
        if not no_ack:
            self._station.sendACK()

    def process_read_out(self, data: bytes, reftime: 'datetime' = None):
        super().process_read_out(data, reftime)

        self.process_extra_data(data)

        if data[:4] == self.SI6_STAR:
            raw_data = bytes([])

            for i in range(2,6):
                ret = self._station.send_command(com.GET_SI_6, [i], True)
                if not isinstance(ret, Command):
                    raise SiError("Can't read Si-Card!")
                raw_data += ret.data[3:]

            for punch_pointer in range(data[self.RC] - self.PM):
                punch_control = raw_data[punch_pointer + self.CN]
                punch_time = raw_data[punch_pointer + self.PTH:punch_pointer + self.PTL + 1]
                punch_date = raw_data[punch_pointer + self.PTD] if self.PTD != -1 else None

                self._punches.append(Punch.from_bytes(punch_control, punch_time, punch_date, reftime))
                punch_pointer += self.PL

    def process_extra_data(self, data: bytes):
        self._personal_data = {}
        for name, (from_, to_) in self._personal_structure.items():
            self._personal_data[name] = data[from_:to_+1].decode("ascii", "ignore")


class SI8To10(SICard):
    """meta class for all SICard 8 and up"""
    _data_name_list: 'Tuple[str, ...]' = ("first_name", "last_name")

    def __init__(self, data: bytes, station: 'SiUSBStation' = None):
        self._number = bytes_to_int(data[1:])
        if station:
            self._station = station
        self._read_at = datetime.now()

    @classmethod
    def switch_types(cls, data: bytes, station: 'SiUSBStation' = None) -> 'SI8To10':
        """switch between the SI Card Types 8 and up, via their number range"""
        num = bytes_to_int(data[1:])
        if 2000000 <= num <= 2999999:
            return SI8(data, station)
        elif 1000000 <= num <= 1999999:
            return SI9(data, station)
        elif 7000000 <= num <= 7999999:
            return SI10(data, station)
        elif 8000000 <= num <= 8999999:
            return SISIAC(data, station)
        elif 9000000 <= num <= 9999999:
            return SI11(data, station)
        else:
            raise SiCardError("Unknown SI-Card!")

    def read_out_data(self, *, no_ack: bool = False) -> None:
        if not self._station:
            raise AttributeError("SICard needs to be invoked with station!")

        raw_data = bytes([])
        for block_number in range(self.BC):
            ret = self._station.send_command(com.GET_SI_8, [block_number], True)
            if not isinstance(ret, Command):
                raise SiError("Can't read Si-Card!")
            raw_data += ret.data[3:]
            if len(raw_data) > self.P1 + self.PL * raw_data[self.RC]:
                break

        self.process_read_out(raw_data)
        if not no_ack:
            self._station.sendACK()

    def process_extra_data(self, data: bytes):
        text = data[self.SPD:self.EPD+1].decode("ascii", "ignore").split(";")

        self._personal_data = {}
        for v, k in zip(text, self._data_name_list): # pylint: disable=invalid-name
            self._personal_data[k] = v


class SI8(SI8To10):
    """SICard 8, numbers 2.000.000 - 2.999.999"""
    CN2 = 0x19
    CN1 = 0x1a
    CN0 = 0x1b
    STD = 0xc
    ST = 0xe
    FTD = 0x10
    FT = 0x12
    CTD = 0x8
    CT = 0xa
    RC = 0x16
    P1 = 0x88
    PL = 0x4
    PM = 30
    PTD = 0x0
    CN = 0x1
    PTH = 0x2
    PTL = 0x3
    BC = 2
    SPD = 0x20
    EPD = 0x87


class SI9(SI8To10):
    """SICard 9, numbers 1.000.000 - 1.999.999"""
    CN2 = 0x19
    CN1 = 0x1a
    CN0 = 0x1b
    STD = 0xc
    ST = 0xe
    FTD = 0x10
    FT = 0x12
    CTD = 0x8
    CT = 0xa
    RC = 0x16
    P1 = 0x38
    PL = 0x4
    PM = 50
    PTD = 0x0
    CN = 0x1
    PTH = 0x2
    PTL = 0x3
    BC = 2
    SPD = 0x20
    EPD = 0x37


class SI10ToSIAC(SI8To10):
    """meta class for all SICard types with the memory layout of an SICard 10 (SI10, SI11, SIAC)"""
    CN2 = 0x19
    CN1 = 0x1a
    CN0 = 0x1b
    STD = 0xc
    ST = 0xe
    STR = 0x1d8
    FTD = 0x10
    FT = 0x12
    FTR = 0x1dc
    CTD = 0x8
    CT = 0xa
    LTR = 0x1b8
    RC = 0x16
    P1 = 0x80*4
    PL = 0x4
    PM = 128
    PTD = 0x0
    CN = 0x1
    PTH = 0x2
    PTL = 0x3
    BC = 8
    SPD = 0x20
    EPD = 0x9f
    DOP_M = 0x1C
    DOP_Y = 0x1D

    _data_name_list = ("first_name", "last_name", "sex", "birth", "club", "mail", "phone", "city", "street", "zip", "country")

    def process_extra_data(self, data: bytes):
        super().process_extra_data(data)

        self._other_data = {
            "production_date": datetime(year=2000+data[self.DOP_Y], month=data[self.DOP_M], day=1)
        }

    def write_personal_data(self):
        """apply changes to personal_data dict to the SICard. Max length including separators 128"""
        if not self._station:
            raise AttributeError("SICard needs to be invoked with station!")

        text = ";".join([self._personal_data[x] for x in self._data_name_list]) + ";"
        if len(text) > 128:
            raise ValueError("Length to great maximum 128!")
        text_bytes = text.encode("ascii", "replace") + b'\xee' * (4 - len(text) % 4)
        for i in range(0, len(text), 4):
            slice_ = text_bytes[i:i+4]
            self._station.send_command(com.WRITE_SI_8, bytes([0x08 + i // 4]) + slice_)

class SI10(SI10ToSIAC):
    """SICard 10, numbers 7.000.000 - 7.999.999"""


class SI11(SI10ToSIAC):
    """SICard 11, numbers 9.000.000 - 9.999.999"""


class SISIAC(SI10ToSIAC):
    """SICard SIAC, numbers 8.000.000 - 8.999.999"""
    HW_M = 0x1C0
    HW_S = 0x1C1
    SW_M = 0x1C2
    SW_S = 0x1C3
    LOW_BAT = 0x1D5
    SIAC_MODE = 0x1CC

    def process_extra_data(self, data: bytes):
        super().process_extra_data(data)

        if not self.other_data:
            self._other_data = {}

        self._other_data["hardware_ver"] = f"{data[self.HW_M]}.{data[self.HW_S]}"
        self._other_data["software_ver"] = f"{data[self.SW_M]}.{data[self.SW_S]}"
        self._other_data["low_battery"] = data[self.LOW_BAT] == 0x6C

        if siac_rev.get(data[self.SIAC_MODE:self.SIAC_MODE+4], None):
            self._other_data["siac_mode"] = siac_rev[data[self.SIAC_MODE:self.SIAC_MODE+4]]

    def write_siac_mode(self, siac_mode: SIAC_BEEP):
        """change blinking mode of the SICard"""
        if not self._station:
            raise AttributeError("SICard needs to be invoked with station!")

        self._station.send_command(com.WRITE_SI_8, bytes([0x73]) + siac_mode.value)
