import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '32bit'
	cpu_count = 1
	is_windows = False
	arch_string_raw = 'armv7l'
	uname_string_raw = ''

	@staticmethod
	def has_proc_cpuinfo():
		return True

	@staticmethod
	def has_cpufreq_info():
		return True

	@staticmethod
	def cat_proc_cpuinfo():
		returncode = 0
		output = r'''
processor       : 0
model name      : ARMv6-compatible processor rev 7 (v6l)
Features        : swp half thumb fastmult vfp edsp java tls
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xb76
CPU revision    : 7

Hardware        : BCM2708
Revision        : 0010
Serial          : 00000000be6d9ba0


'''
		return returncode, output

	@staticmethod
	def cpufreq_info():
		returncode = 0
		output = r'''
cpufrequtils 008: cpufreq-info (C) Dominik Brodowski 2004-2009
Report errors and bugs to cpufreq@vger.kernel.org, please.
analyzing CPU 0:
driver: generic_cpu0
CPUs which run at the same hardware frequency: 0
CPUs which need to have their frequency coordinated by software: 0
maximum transition latency: 300 us.
hardware limits: 300 MHz - 1000 MHz
available frequency steps: 300 MHz, 600 MHz, 800 MHz, 1000 MHz
available cpufreq governors: conservative, ondemand, userspace, powersave, performance
current policy: frequency should be within 300 MHz and 1000 MHz.
The governor "performance" may decide which speed to use
within this range.
current CPU frequency is 1000 MHz.
cpufreq stats: 300 MHz:0.00%, 600 MHz:0.00%, 800 MHz:0.00%, 1000 MHz:100.00%
'''
		return returncode, output


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_registry()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 4
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 0
	assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) == 3
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 14


def test_get_cpu_info_from_cpufreq_info():
	info = cpuinfo._get_cpu_info_from_cpufreq_info()

	assert info['hz_advertised_friendly'] == '1.0000 GHz'
	assert info['hz_actual_friendly'] == '1.0000 GHz'
	assert info['hz_advertised'] == (1000000000, 0)
	assert info['hz_actual'] == (1000000000, 0)


def test_get_cpu_info_from_proc_cpuinfo():
	info = cpuinfo._get_cpu_info_from_proc_cpuinfo()

	assert info['hardware_raw'] == 'BCM2708'
	assert info['brand_raw'] == 'ARMv6-compatible processor rev 7 (v6l)'

	assert info['flags'] == ['edsp', 'fastmult', 'half', 'java', 'swp', 'thumb', 'tls', 'vfp']


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['hardware_raw'] == 'BCM2708'
	assert info['brand_raw'] == 'ARMv6-compatible processor rev 7 (v6l)'
	assert info['hz_advertised_friendly'] == '1.0000 GHz'
	assert info['hz_actual_friendly'] == '1.0000 GHz'
	assert info['hz_advertised'] == (1000000000, 0)
	assert info['hz_actual'] == (1000000000, 0)
	assert info['arch'] == 'ARM_7'
	assert info['bits'] == 32
	assert info['count'] == 1

	assert info['arch_string_raw'] == 'armv7l'

	assert info['flags'] == ['edsp', 'fastmult', 'half', 'java', 'swp', 'thumb', 'tls', 'vfp']
