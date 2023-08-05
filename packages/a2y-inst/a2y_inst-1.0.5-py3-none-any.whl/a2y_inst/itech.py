from serial import Serial as Serial
from typing import Union as _Union
from enum import Enum


class LoadMode(Enum):
	CC = 0
	CV = 1
	CW = 2
	CR = 3


class IT8500plus:
	def __init__(self, port: str, baudrate: int = 9600):
		self.__serial = Serial(port, baudrate=baudrate, timeout=0.5)

	@staticmethod
	def checksum(data: _Union[bytearray, bytes]) -> int:
		assert len(data) >= 25
		crc = 0
		for i in range(25):
			crc += data[i]
		return crc & 0xFF

	def read_frame(self):
		frame = self.__serial.read(26)
		if len(frame) != 26:
			raise IOError('Communicate with IT8500plus timeout.')
		if frame[0] != 0xAA:
			raise IOError('IT8500plus frame header invalid.')
		if IT8500plus.checksum(frame) != frame[25]:
			raise IOError('IT8500plus frame checksum error.')

		return frame

	def read_setting_feedback_frame(self):
		frame = self.read_frame()
		if frame[2] != 0x12:
			raise IOError(f'IT8500plus Setting Feedback frame format invalid: command byte is not 0x12: {frame[2]}.')
		if frame[3] != 0x80:
			raise IOError(f'IT58500plus says that you have make some mistakes on your command: {frame[3]:02X}H.')
		return frame

	def __set_something(self, frame):
		self.__serial.write(frame)
		self.read_setting_feedback_frame()

	def read_getting_multi_bytes_feedback_frame(self, cmd: int, count: int):
		frame = self.read_frame()
		if frame[2] != cmd:
			raise IOError(f'IT8500plus feedback command byte is not matched. Send: {cmd:02X}H, Recf: {frame[2]:02X}H.')
		return frame[3:3+count]

	def read_getting_one_bye_feedback_frame(self, cmd: int) -> int:
		frame = self.read_frame()
		if frame[2] != cmd:
			raise IOError(f'IT8500plus feedback command byte is not matched. Send: {cmd:02X}H, Recf: {frame[2]:02X}H.')
		return frame[3]

	def __get_one_byte(self, frame) -> int:
		self.__serial.write(frame)
		return self.read_getting_one_bye_feedback_frame(frame[2])

	def read_getting_u16int_feedback_frame(self, cmd: int) -> int:
		frame = self.read_frame()
		if frame[2] != cmd:
			raise IOError(f'IT8500plus feedback command byte is not matched. Send: {cmd:02X}H, Recf: {frame[2]:02X}H.')
		return (frame[4] << 8) | frame[3]

	def __get_uint16(self, frame) -> int:
		self.__serial.write(frame)
		return self.read_getting_u16int_feedback_frame(frame[2])

	def read_getting_u32int_feedback_frame(self, cmd: int) -> int:
		frame = self.read_frame()
		if frame[2] != cmd:
			raise IOError(f'IT8500plus feedback command byte is not matched. Send: {cmd:02X}H, Recf: {frame[2]:02X}H.')
		return frame[3] | (frame[4] << 8) | (frame[5] << 16) | (frame[6] << 24)

	def __get_uint32(self, frame) -> int:
		self.__serial.write(frame)
		return self.read_getting_u32int_feedback_frame(frame[2])

	@staticmethod
	def build_frame(station: int, cmd: int, data: _Union[bytearray, bytes, list]):
		assert len(data) <= 22
		frame = bytearray(26)
		frame[0] = 0xAA
		frame[1] = station
		frame[2] = cmd
		for idx, byte in enumerate(data):
			frame[idx+3] = byte
		frame[-1] = IT8500plus.checksum(frame)
		return frame

	def set_control_mode(self, station: int, mode: _Union[str, bool, int]):
		"""
		设置负载仪的控制模式：通过本地面板控制的本地模式，或者是通过通信端口控制的远程模式（remote mode）。
		"""
		if isinstance(mode, str):
			mode_value = 1 if mode == 'remote' else 0
		elif isinstance(mode, bool):
			mode_value = 1 if mode else 0
		elif isinstance(mode, int):
			mode_value = 0 if mode == 0 else 1
		else:
			raise ValueError(f'Unknown mode: {mode} with type {type(mode)}.')
		frame = IT8500plus.build_frame(station, 0x20, [mode_value])
		self.__set_something(frame)

	def set_remote_mode(self, station: int):
		"""
		设置负载仪为远程模式。只有在远程模式下，负载仪才会响应从通信端口传入的其他的设置、控制命令。
		"""
		self.set_control_mode(station, mode=1)

	def set_load_mode(self, station: int, mode: LoadMode):
		frame = IT8500plus.build_frame(station, 0x28, [mode.value])
		self.__set_something(frame)

	def get_load_mode(self, station: int):
		frame = IT8500plus.build_frame(station, 0x29, [])
		feedback = self.__get_one_byte(frame)
		return LoadMode(feedback)

	def set_cc_current(self, station: int, current: float):
		cur = int(current * 10000)
		data = [0] * 4
		data[0] = cur & 0xFF
		data[1] = (cur >> 8) & 0xFF
		data[2] = (cur >> 16) & 0xFF
		data[3] = (cur >> 24) & 0xFF
		frame = IT8500plus.build_frame(station, 0x2A, data)
		self.__set_something(frame)

	def get_cc_current(self, station: int) -> float:
		frame = IT8500plus.build_frame(station, 0x2B, [])
		current = self.__get_uint32(frame)
		return current / 10000

	def get_load_status(self, station: int) -> dict:
		status = dict()
		frame = IT8500plus.build_frame(station, 0x5F, [])
		self.__serial.write(frame)
		data = self.read_getting_multi_bytes_feedback_frame(0x5F, 26-3-1)
		for idx, name in enumerate(['voltage', 'current', 'power']):
			start = idx * 4
			value = data[start] | (data[start+1] << 8) | (data[start+2] << 16) | (data[start+3] << 24)
			status[name] = value
		status['operation_status'] = data[12]
		status['query_status'] = data[13] | (data[14] << 8)
		# TODO: 保存其他那些“散热器温度”等数据
		return status

	def get_real_current(self, station: int) -> float:
		status = self.get_load_status(station)
		return status['current'] / 10000

	def get_real_voltage(self, station: int) -> float:
		status = self.get_load_status(station)
		return status['voltage'] / 1000

	def get_real_power(self, station: int) -> float:
		status = self.get_load_status(station)
		return status['power'] / 1000

	def set_input_state(self, station: int, state: _Union[bool, str]):
		if isinstance(state, str):
			if state.upper() in ['ON', '1']:
				i_state = 1
			else:
				i_state = 0
		else:
			i_state = 1 if state else 0
		frame = IT8500plus.build_frame(station, 0x21, [i_state])
		self.__set_something(frame)

	def turn_on(self, station: int):
		self.set_input_state(station, True)

	def turn_off(self, station: int):
		self.set_input_state(station, False)

	def close(self):
		self.__serial.close()
