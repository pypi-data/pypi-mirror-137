"""
utility functions for the library
"""

from typing import TYPE_CHECKING, List, Union

from sipyconfig.enums import stationmode

if TYPE_CHECKING:
    from sipyconfig.card import SICard

def log2(number: int) -> int:
    """returns length of number in binary without leading zeros"""
    return len(format(number, "b"))

def apply_bit_mask(number: int, mask: int, value: int) -> int:
    """sets number to value if mask (works bitwise)"""
    length = max(log2(x) for x in [number, mask, value])
    num_bin = format(number, f"0{length}b")
    mask_bin = format(mask, f"0{length}b")
    value_bin = format(value, f"0{length}b")
    result = "".join(v if int(m) else n for n, m,
                     v in zip(num_bin, mask_bin, value_bin))
    return int(result, 2)

def array_or(array: List[int]) -> int:
    """return bitwise or of all elements of the list"""
    result = 0
    for num in array:
        result |= num
    return result

def is_siac_special_mode(station_mode: int) -> bool:
    """returns True if mode is a SIAC special mode"""
    return station_mode in [stationmode.SIAC_BATTERY_TEST, stationmode.SIAC_ON, stationmode.SIAC_OFF, stationmode.SIAC_RADIO_READOUT, stationmode.SIAC_TEST]

def is_siac_mode(station_mode: int) -> bool:
    """returns True if mode is a SIAC mode"""
    return is_siac_special_mode(station_mode) or station_mode in [stationmode.SIAC_CONTROL, stationmode.SIAC_START,
                                                                stationmode.SIAC_FINISH, stationmode.SIAC_TEST, stationmode.SIAC_SPECIAL]

def evenhex(num: int) -> str:
    """return hex() of num with leading zeros to make len() even"""
    hex_text = hex(num)[2:]
    if len(hex_text) % 2 != 0:
        return f"0x0{hex_text}"
    return f"0x{hex_text}"

def hextoascii(num: int) -> str:
    """return ascii of num if num between 32 and 126 ('normal' character)"""
    if 32 <= num <= 126:
        return chr(num)
    return evenhex(num)

def bytes_to_int(data: Union[bytes, List[int]]) -> int:
    """return int of bytes"""
    value = 0
    for offset, byte in enumerate([x for x in data][::-1]):
        value += byte << offset*8
    return value

def print_si_card(card: 'SICard'):
    """pretty print data stored in an SICard Object"""
    print(f"""
{card}
clear:  {card.cleartime}
check:  {card.checktime}
start:  {card.starttime}
finish: {card.finishtime}

clear_res:  {card.cleartime_reserve}
start_res:  {card.starttime_reserve}
finish_res: {card.finishtime_reserve}

personal data: {card.personal_data}
other data:    {card.other_data}

{len(card.punches)} punches:""")

    for i, punch in enumerate(card.punches):
        print(f"{i+1:03d} - {punch}")
