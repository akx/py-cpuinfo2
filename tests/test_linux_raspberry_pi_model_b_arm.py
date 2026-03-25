import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '32bit'
	cpu_count = 1
	is_windows = False
	arch_string_raw = 'armv6l'
	uname_string_raw = ''

	@staticmethod
	def has_proc_cpuinfo():
		return True

	@staticmethod
	def has_lscpu():
		return True

	@staticmethod
	def cat_proc_cpuinfo():
		returncode = 0
		output = r'''
Processor	: ARMv6-compatible processor rev 7 (v6l)
BogoMIPS	: 697.95
Features	: swp half thumb fastmult vfp edsp java tls
CPU implementer	: 0x41
CPU architecture: 7
CPU variant	: 0x0
CPU part	: 0xb76
CPU revision	: 7

Hardware	: BCM2708
Revision	: 000d
Serial		: 0000000066564a8f


'''
		return returncode, output

	@staticmethod
	def lscpu():
		returncode = 0
		output = r'''
Architecture:          armv6l
Byte Order:            Little Endian
CPU(s):                1
On-line CPU(s) list:   0
Thread(s) per core:    1
Core(s) per socket:    1
Socket(s):             1
CPU max MHz:           700.0000
CPU min MHz:           700.0000


'''
		return returncode, output


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_registry()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 0
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 4
	assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) == 3
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 14


def test_get_cpu_info_from_lscpu():
	info = cpuinfo._get_cpu_info_from_lscpu()

	assert info['hz_advertised_friendly'] == '700.0000 MHz'
	assert info['hz_actual_friendly'] == '700.0000 MHz'
	assert info['hz_advertised'] == (700000000, 0)
	assert info['hz_actual'] == (700000000, 0)


def test_get_cpu_info_from_proc_cpuinfo():
	info = cpuinfo._get_cpu_info_from_proc_cpuinfo()

	assert info['hardware_raw'] == 'BCM2708'
	assert info['brand_raw'] == 'ARMv6-compatible processor rev 7 (v6l)'

	assert info['flags'] == ['edsp', 'fastmult', 'half', 'java', 'swp', 'thumb', 'tls', 'vfp']


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['hardware_raw'] == 'BCM2708'
	assert info['brand_raw'] == 'ARMv6-compatible processor rev 7 (v6l)'
	assert info['hz_advertised_friendly'] == '700.0000 MHz'
	assert info['hz_actual_friendly'] == '700.0000 MHz'
	assert info['hz_advertised'] == (700000000, 0)
	assert info['hz_actual'] == (700000000, 0)
	assert info['arch'] == 'ARM_7'
	assert info['bits'] == 32
	assert info['count'] == 1

	assert info['arch_string_raw'] == 'armv6l'

	assert info['flags'] == ['edsp', 'fastmult', 'half', 'java', 'swp', 'thumb', 'tls', 'vfp']
