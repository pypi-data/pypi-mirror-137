'''
Date: 2022.02.04 21:36
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.02.04 21:36
'''
import io
import struct
from typing import BinaryIO


class FixedVHDWriter(object):
    # Hard Disk Footer Format
    _cookie: bytes = b''  # 8
    _features: bytes = b''  # 4
    _file_format_version: bytes = b''  # 4
    _data_offset: bytes = b''  # 8
    _time_stamp: bytes = b''  # 4
    _creator_application: bytes = b''  # 4
    _creator_version: bytes = b''  # 4
    _creator_host_os: bytes = b''  # 4
    _original_size: int = 0  # 8
    _current_size: int = 0  # 8
    _disk_geometry: bytes = b''  # 4
    _dist_type: int = 0  # 4
    _checksum: bytes = b''  # 4
    _unique_id: bytes = b''  # 16
    _saved_state: bytes = b''  # 1
    _reserved: bytes = b''  # 427

    # Disk Geometry
    _cylinder: int = 0  # 柱面
    _heads: int = 0  # 磁头
    _sectors_per_cylinder: int = 0  # 扇区

    _valid = False
    _sector_size: int = 512

    def __init__(self, file):
        self._file = file

        self._read_footer()

    def _read_footer(self):
        with open(self._file, 'rb') as fp:
            if fp.seek(-self._sector_size, io.SEEK_END) < self._sector_size:
                return

            footer = fp.read(self._sector_size)

            (
                self._cookie,  # 8
                self._features,  # 4
                self._file_format_version,  # 4
                self._data_offset,  # 8
                self._time_stamp,  # 4
                self._creator_application,  # 4
                self._creator_version,  # 4
                self._creator_host_os,  # 4
                self._original_size,  # 8
                self._current_size,  # 8
                self._disk_geometry,  # 4
                self._dist_type,  # 4
                self._checksum,  # 4
                self._unique_id,  # 16
                self._saved_state,  # 1
                self._reserved,  # 427
            ) = struct.unpack('>8s4s4s8si4s4s4sqq4si4s16sc427s', footer)

            self._cylinder, self._heads, self._sectors_per_cylinder = struct.unpack('>hBB', self._disk_geometry)

            self._valid = True

    @property
    def valid(self) -> bool:
        return self._valid and self._cookie == 'conectix'

    @property
    def fixed(self) -> bool:
        return self._dist_type == 2

    @property
    def original_size(self) -> int:
        return self._original_size >> 20  # MB

    @property
    def current_size(self) -> int:
        return self._current_size >> 20  # MB

    @property
    def total_sectors(self) -> int:
        return self._original_size // 512

    @property
    def geometry(self) -> str:
        return f'Original Size: {self.original_size}MB\n' \
               f'Cylinder: {self._cylinder}\n' \
               f'Heads: {self._heads}\n' \
               f'Sectors Per Cylinder: {self._sectors_per_cylinder}'

    def _write_one_sector(self, writer: BinaryIO, raw: bytes, sector_offset: int = 0):
        if len(raw) > 512:
            raise ValueError('raw size exceeds maximum')

        writer.seek(sector_offset * self._sector_size, io.SEEK_SET)

        return writer.write(raw)

    def write_from_binary_file(self, file, sector_offset: int = 0) -> int:
        if sector_offset >= self.total_sectors or sector_offset < 0:
            raise ValueError('sector_offset exceeds maximum')

        total_bytes_written = 0

        with open(self._file, 'rb+') as fw:
            with open(file, 'rb') as fr:
                while sector_offset < self.total_sectors:
                    raw = fr.read(self._sector_size)

                    if not raw:
                        break

                    total_bytes_written += self._write_one_sector(fw, raw, sector_offset)
                    sector_offset += 1

        return total_bytes_written
