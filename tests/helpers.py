# SPDX-License-Identifier: MIT
# Copyright (c) 2014-2022 Matthew Brennan Jones <matthew.brennan.jones@gmail.com>
# Copyright (c) 2026 Aarni Koskela <akx@iki.fi>

import itertools
import platform
import time
from unittest.mock import Mock


class EmptyDataSource:
	@staticmethod
	def has_proc_cpuinfo():
		return False

	@staticmethod
	def has_lscpu():
		return False

	@staticmethod
	def has_ibm_pa_features():
		return False

	@staticmethod
	def has_wmic():
		return False

	@staticmethod
	def has_dmesg():
		return False

	@staticmethod
	def has_var_run_dmesg_boot():
		return False

	@staticmethod
	def has_cpufreq_info():
		return False

	@staticmethod
	def has_sestatus():
		return False

	@staticmethod
	def has_sysctl():
		return False

	@staticmethod
	def has_isainfo():
		return False

	@staticmethod
	def has_kstat():
		return False

	@staticmethod
	def has_sysinfo():
		return False


def get_os_type():
	os_type = 'Unknown'

	# Figure out the general OS type
	uname = platform.system().strip().strip('"').strip("'").strip().lower()
	if 'beos' in uname or 'haiku' in uname:
		os_type = 'BeOS'
	elif 'bsd' in uname or 'gnu/kfreebsd' in uname:
		os_type = 'BSD'
	elif 'cygwin' in uname:
		os_type = 'Cygwin'
	elif 'darwin' in uname:
		os_type = 'MacOS'
	elif 'linux' in uname:
		os_type = 'Linux'
	elif 'solaris' in uname or 'sunos' in uname:
		os_type = 'Solaris'
	elif 'windows' in uname:
		os_type = 'Windows'

	return os_type


_DATA_SOURCE_ATTRS = [
	'bits',
	'cpu_count',
	'is_windows',
	'arch_string_raw',
	'uname_string_raw',
	'can_cpuid',
]

_DATA_SOURCE_STATIC_METHODS = [
	'has_proc_cpuinfo',
	'has_dmesg',
	'has_var_run_dmesg_boot',
	'has_cpufreq_info',
	'has_sestatus',
	'has_sysctl',
	'has_isainfo',
	'has_kstat',
	'has_sysinfo',
	'has_lscpu',
	'has_ibm_pa_features',
	'has_wmic',
	'cat_proc_cpuinfo',
	'cpufreq_info',
	'sestatus_b',
	'dmesg_a',
	'cat_var_run_dmesg_boot',
	'sysctl_machdep_cpu_hw_cpufrequency',
	'isainfo_vb',
	'kstat_m_cpu_info',
	'lscpu',
	'ibm_pa_features',
	'wmic_cpu',
	'sysinfo_cpu',
	'winreg_processor_brand',
	'winreg_vendor_id_raw',
	'winreg_arch_string_raw',
	'winreg_hz_actual',
	'winreg_feature_bits',
]


def monkey_patch_data_source(cpuinfo, NewDataSource, monkeypatch):
	# Replace all methods with ones that return false
	_actual_monkey_patch_data_source(cpuinfo, EmptyDataSource, monkeypatch)

	# Copy any methods that are the same over
	_actual_monkey_patch_data_source(cpuinfo, NewDataSource, monkeypatch)


def _actual_monkey_patch_data_source(cpuinfo, NewDataSource, monkeypatch):
	for attr in _DATA_SOURCE_ATTRS:
		if hasattr(NewDataSource, attr):
			monkeypatch.setattr(cpuinfo.DataSource, attr, getattr(NewDataSource, attr))

	for method in _DATA_SOURCE_STATIC_METHODS:
		if hasattr(NewDataSource, method):
			monkeypatch.setattr(cpuinfo.DataSource, method, staticmethod(getattr(NewDataSource, method)))


def monkey_patch_cpuid(cpuinfo, return_hz, return_values, monkeypatch):
	class MockCPUID:
		_counter = 0
		_is_first = False

		def _asm_func(self, restype=None, argtypes=(), machine_code=[]):
			class CPUIDGetTicks:
				# NOTE: This assumes that the function returned is a get_ticks function
				def func(self):
					MockCPUID._is_first = not MockCPUID._is_first

					if MockCPUID._is_first:
						return return_hz
					else:
						return 0

				def free(self):
					pass

			return CPUIDGetTicks()

		def _run_asm(self, *machine_code):
			result = return_values[MockCPUID._counter]
			MockCPUID._counter += 1
			if MockCPUID._counter == len(return_values):
				MockCPUID._counter = 0
			return result

	monkeypatch.setattr(cpuinfo.CPUID, '_run_asm', MockCPUID.__dict__['_run_asm'])
	monkeypatch.setattr(cpuinfo.CPUID, '_asm_func', MockCPUID.__dict__['_asm_func'])
	# TODO: this doesn't feel like a great patch
	monkeypatch.setattr(time, 'monotonic', Mock(side_effect=itertools.cycle([0.0, 1.0])))


def monkey_patch_asm(cpuinfo, NewASM, monkeypatch):
	monkeypatch.setattr(cpuinfo.ASM, 'compile', NewASM.__dict__['compile'])
	monkeypatch.setattr(cpuinfo.ASM, 'run', NewASM.__dict__['run'])
	monkeypatch.setattr(cpuinfo.ASM, 'free', NewASM.__dict__['free'])
	# TODO: this doesn't feel like a great patch
	monkeypatch.setattr(time, 'monotonic', Mock(side_effect=itertools.cycle([0.0, 1.0])))
