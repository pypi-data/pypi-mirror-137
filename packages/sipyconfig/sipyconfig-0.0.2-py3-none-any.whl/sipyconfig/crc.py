"""
CRC module for communication with SIStations
"""

from typing import Union, List

def compute_crc(data: Union[bytes, List[int]]) -> 'int':
    '''compute the CRC by Spec'''
    if isinstance(data, bytes):
        data = [x for x in data]
    i_tmp, ui_tmp1, ui_val = 0, 0, 0
    i = 0
    ui_count = len(data)

    if ui_count < 2:
        return 0

    ui_tmp1 = data[i]
    i += 1
    ui_tmp1 = (ui_tmp1 << 8) + data[i]
    i += 1

    if ui_count == 2:
        return ui_tmp1

    for i_tmp in range(ui_count >> 1, 0, -1):
        if i_tmp > 1:
            ui_val = data[i]
            i += 1
            ui_val = (ui_val << 8) + data[i]
            i += 1
        else:
            if ui_count & 1:
                ui_val = data[i]
                ui_val <<= 8
            else:
                ui_val = 0

        for j in range(16): # pylint: disable=unused-variable
            if ui_tmp1 & 0x8000:
                ui_tmp1 <<= 1
                ui_tmp1 &= 0x0000FFFF
                if ui_val & 0x8000:
                    ui_tmp1 += 1
                    ui_tmp1 &= 0x0000FFFF
                ui_tmp1 ^= 0x8005
            else:
                ui_tmp1 <<= 1
                ui_tmp1 &= 0x0000FFFF
                if ui_val & 0x8000:
                    ui_tmp1 += 1
                    ui_tmp1 &= 0x0000FFFF
            ui_val <<= 1
            ui_val &= 0x0000FFFF
    return ui_tmp1
