"""
submodule for the serial communication with the SI Station
"""

from typing import Union, List
from serial import Serial, SerialTimeoutException

from sipyconfig.crc import compute_crc
from sipyconfig.enums import com, proto, CRCError

class ACK():
    """class representing a ACK response"""


class NOACK():
    """class representing a NOACK response"""


class Command():
    """class representing a received Command or a Command about to be sent"""
    START_SEQUENCE = [proto.WAKEUP, proto.STX, proto.STX]

    _command_code: int
    _data: List[int]
    _crc: bytes
    _is_extended_command: bool
    _is_receiving_command: bool

    def __init__(self, command_code: int, data: Union[bytes, List[int]] = None, *, receiving: bool = False) -> None:
        self._is_receiving_command = receiving
        self.command_code = command_code
        if data is not None:
            if isinstance(data, bytes):
                self._data = [x for x in data]
            else:
                self._data = data
            if not self._is_receiving_command:
                self.compute_crc()

    @property
    def command_code(self) -> int:
        """command code of the command"""
        return self._command_code

    @command_code.setter
    def command_code(self, command_code: int) -> None:
        self._command_code = command_code
        self._is_extended_command = not self.is_basic_protocol(command_code)

    @property
    def is_extended_command(self) -> bool:
        """whether this command is part of the extended protocol"""
        return self._is_extended_command

    @property
    def data(self) -> bytes:
        """data of the command"""
        return bytes(self._data)

    @data.setter
    def data(self, data: List[int]) -> None:
        if len(data) > 255:
            raise ValueError("Datastream to big, can only send up to 255 bytes at a time.")
        self._data = data
        if not self._is_receiving_command:
            self.compute_crc()

    def add_data(self, data: Union[int, List[int]]) -> None:
        """append data to this command"""
        if not getattr(self, "_data", None):
            self._data = []
        if isinstance(data, int):
            if self.length + 1 > 255:
                raise ValueError("Datastream to big, can only send up to 255 bytes at a time.")
            self._data.append(data)
        else:
            if self.length + len(data) > 255:
                raise ValueError("Datastream to big, can only send up to 255 bytes at a time.")
            self._data.extend(data)
        if not self._is_receiving_command:
            self.compute_crc()

    def compute_crc(self) -> bytes:
        """compute the crc of the currently stored data"""
        self._crc = compute_crc(self.content).to_bytes(2, "big")
        return self.crc

    @property
    def content(self) -> bytes:
        """return [command_code, length, <data>] as bytes"""
        return bytes([self.command_code, self.length]) + self.data

    @property
    def crc(self) -> bytes:
        """currently stored crc"""
        return self._crc

    @crc.setter
    def crc(self, crc: bytes) -> None:
        if not self._is_receiving_command:
            raise TypeError("Setting CRC is only possible when command is set receiving!")
        self._crc = crc

    @property
    def length(self) -> int:
        """length of the stored data"""
        return len(self._data)

    @property
    def packet(self) -> 'bytes':
        """the full byte sequence to be sent to the station, (content + crc / data with DLE)"""
        if self.is_extended_command:
            packet = bytes([self.command_code, self.length]) + bytes(self.data) + self.crc
        else:
            packet = bytes([self.command_code]) + bytes(sum([[proto.DLE, x] for x in self.data], []))
        return bytes(self.START_SEQUENCE) + packet + bytes([proto.ETX])

    def check_crc(self, crc: 'Union[int, bytes]' = None, content: bytes = None) -> bool:
        """check crc of content, omitted parameters are taken from stored values"""
        if content is None:
            content = self.content
        if crc is None:
            crc = compute_crc(content).to_bytes(2, "big")
        if isinstance(crc, int):
            crc = crc.to_bytes(2, "big")
        return self.crc == crc

    @staticmethod
    def is_basic_protocol(command_code: int) -> bool:
        '''command_code < 0x80 or 0xC4'''
        return command_code < 0x80 or command_code == 0xC4

    @staticmethod
    def is_extended_protocol(command_code: int) -> bool:
        '''command_code >= 0x80 and not 0xC4'''
        return command_code >= 0x80 and not command_code == 0xC4

    @staticmethod
    def strip_data_of_dle(data: Union[bytes, List[int]]) -> List[int]:
        """remove DLE from a data stream so it can be processed further"""
        ret = []
        seen_dle = False
        for dat in data:
            if not seen_dle and dat == proto.DLE:
                seen_dle = True
                continue
            ret.append(dat)
            seen_dle = False
        return ret



def receive_basic_command(command_code: int, dev: 'Serial') -> 'Command':
    '''receive command part of the basic protocol,
    structure: STX | command code | parameter/data with DLE | ETX'''
    command = Command(command_code, receiving=True)
    while True:
        byte = dev.read(1)[0]
        if byte == proto.DLE:
            command.add_data(dev.read(1))
        elif byte == proto.ETX:
            return command


def receive_extended_command(command_code: int, dev: 'Serial') -> 'Command':
    '''receive command part of the extended protocol,
    structure: STX | command code | length byte | parameter/data | CRC1 | CRC0 | ETX'''
    command = Command(command_code, receiving=True)
    length = dev.read(1)[0]
    command.data = dev.read(length)
    command.crc= dev.read(2)
    if not command.check_crc():
        raise CRCError("CRC does not match!")
    while dev.read(1)[0] != proto.ETX:
        pass
    return command


def receive_command(dev: 'Serial') -> 'Union[Command, ACK, NOACK]':
    """receive a command, switches internally between receive_basic_command and receive_extended_command, depending on the command code"""
    try:
        have_seen_stx = False
        while True:
            byte = dev.read(1)
            if len(byte) == 0:
                raise SerialTimeoutException
            byte = byte[0]
            if byte == proto.STX:
                have_seen_stx = True
            elif have_seen_stx:
                if Command.is_basic_protocol(byte):
                    return receive_basic_command(byte, dev)
                elif Command.is_extended_protocol(byte):
                    return receive_extended_command(byte, dev)
            elif not have_seen_stx and byte == proto.NAK:
                return NOACK()
    except SerialTimeoutException:
        return NOACK()


def send_command(command_code: com, data: Union[bytes, List[int]], dev: Serial) -> int:
    '''sends given data to the station via the extended or basic protocoll, depending on the command code'''
    command = Command(command_code, data)
    return dev.write(command.packet)
