from a2y_modbus import Master as _Modbus
from serial import Serial as _Serial
from threading import Lock as _Lock
from typing import List as _List, Tuple as _Tuple


class XCPlc:
	def __init__(self, port: str, baudrate: int = 115200):
		self._serial = _Serial(port, baudrate, timeout=0.3)
		self.__modbus = _Modbus(self._serial, timeout=0.3)
		self.__lock = _Lock()

	def set_coil(self, station: int, name: str, value: bool):
		coil_type = name[0]
		if coil_type == 'Y':
			start_address = 0x4800
		elif coil_type == 'X':
			raise TypeError(f'Writing readonly coil: "{name}".')
		else:
			raise TypeError(f'Coil type "{coil_type}" is not supported yet.')
		shift = int(name[1:], 8)
		with self.__lock:
			self.__modbus.write_coil(station=station, address=start_address + shift, value=value)

	def get_coils(self, station: int, name: str, count: int) -> _List[bool]:
		assert 0 < count <= 16
		coil_type = name[0]
		if coil_type == 'X':
			start_address = 0x4000
		elif coil_type == 'Y':
			start_address = 0x4800
		else:
			raise TypeError(f'Coil type "{coil_type}" is not supported yet.')
		shift = int(name[1:], 8)
		with self.__lock:
			values = self.__modbus.read_coils(station=station, address=start_address + shift, count=count)
		return values

	def get_coil(self, station: int, name: str) -> bool:
		return self.get_coils(station, name, 1)[0]

	@staticmethod
	def register_name_to_address(name: str) -> int:
		num_start_idx = -1
		for idx, char in enumerate(name):
			if str.isdigit(char):
				num_start_idx = idx
				break
		assert num_start_idx > 0
		register_type = name[:num_start_idx]
		if register_type != 'D':
			raise TypeError(f'Register type "{register_type}" is not supported yet.')
		address = int(name[num_start_idx:])
		return address

	def set_uint16(self, station: int, name: str, value: int):
		address = XCPlc.register_name_to_address(name)
		with self.__lock:
			self.__modbus.write_uint16(station, address, value)

	def get_uint16(self, station: int, name: str) -> int:
		address = XCPlc.register_name_to_address(name)
		with self.__lock:
			return self.__modbus.read_register(station, address)

	def get_multi_uint16(self, station: int, name: str, count: int) -> _List[int]:
		address = XCPlc.register_name_to_address(name)
		with self.__lock:
			return self.__modbus.read_registers(station, address, count)
