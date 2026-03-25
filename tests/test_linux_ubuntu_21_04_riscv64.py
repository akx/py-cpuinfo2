import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 4
	is_windows = False
	arch_string_raw = 'riscv64'
	uname_string_raw = 'riscv64'
	can_cpuid = False

	@staticmethod
	def has_proc_cpuinfo():
		return True

	@staticmethod
	def has_dmesg():
		return True

	@staticmethod
	def has_lscpu():
		return True

	@staticmethod
	def has_ibm_pa_features():
		return False

	@staticmethod
	def cat_proc_cpuinfo():
		returncode = 0
		output = r'''
processor       : 0
hart            : 2
isa             : rv64imafdc
mmu             : sv39
uarch           : sifive,u74-mc

processor       : 1
hart            : 1
isa             : rv64imafdc
mmu             : sv39
uarch           : sifive,u74-mc

processor       : 2
hart            : 3
isa             : rv64imafdc
mmu             : sv39
uarch           : sifive,u74-mc

processor       : 3
hart            : 4
isa             : rv64imafdc
mmu             : sv39
uarch           : sifive,u74-mc

'''
		return returncode, output

	@staticmethod
	def dmesg_a():
		returncode = 1
		output = r'''
dmesg: read kernel buffer failed: Operation not permitted

'''
		return returncode, output

	@staticmethod
	def lscpu():
		returncode = 0
		output = r'''
Architecture:        riscv64
Byte Order:          Little Endian
CPU(s):              4
On-line CPU(s) list: 0-3
Thread(s) per core:  4
Core(s) per socket:  1
Socket(s):           1
L1d cache:           32 KiB
L1i cache:           32 KiB
L2 cache:            2 MiB


'''
		return returncode, output


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_registry()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 0
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 3
	assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) == 1
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 11


def test_get_cpu_info_from_lscpu():
	info = cpuinfo._get_cpu_info_from_lscpu()
	assert info['l1_instruction_cache_size'] == (32 * 1024)
	assert info['l1_data_cache_size'] == (32 * 1024)
	assert info['l2_cache_size'] == ((2 * 1024) * 1024)
	assert len(info) == 3


def test_get_cpu_info_from_proc_cpuinfo():
	info = cpuinfo._get_cpu_info_from_proc_cpuinfo()
	assert info['brand_raw'] == 'sifive,u74-mc'
	assert len(info) == 1


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['brand_raw'] == 'sifive,u74-mc'
	assert info['arch'] == 'RISCV_64'
	assert info['bits'] == 64
	assert info['count'] == 4
	assert info['l1_instruction_cache_size'] == (32 * 1024)
	assert info['l1_data_cache_size'] == (32 * 1024)
	assert info['l2_cache_size'] == ((2 * 1024) * 1024)
	assert info['arch_string_raw'] == 'riscv64'
