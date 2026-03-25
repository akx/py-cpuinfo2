import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 6
	is_windows = False
	arch_string_raw = 'aarch64'
	uname_string_raw = ''
	can_cpuid = False

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
processor       : 90
BogoMIPS        : 200.00
Features        : fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics
CPU implementer : 0x43
CPU architecture: 8
CPU variant     : 0x1
CPU part        : 0x0a1
CPU revision    : 0

processor       : 91
BogoMIPS        : 200.00
Features        : fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics
CPU implementer : 0x43
CPU architecture: 8
CPU variant     : 0x1
CPU part        : 0x0a1
CPU revision    : 0

processor       : 92
BogoMIPS        : 200.00
Features        : fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics
CPU implementer : 0x43
CPU architecture: 8
CPU variant     : 0x1
CPU part        : 0x0a1
CPU revision    : 0

processor       : 93
BogoMIPS        : 200.00
Features        : fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics
CPU implementer : 0x43
CPU architecture: 8
CPU variant     : 0x1
CPU part        : 0x0a1
CPU revision    : 0

processor       : 94
BogoMIPS        : 200.00
Features        : fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics
CPU implementer : 0x43
CPU architecture: 8
CPU variant     : 0x1
CPU part        : 0x0a1
CPU revision    : 0

processor       : 95
BogoMIPS        : 200.00
Features        : fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics
CPU implementer : 0x43
CPU architecture: 8
CPU variant     : 0x1
CPU part        : 0x0a1
CPU revision    : 0


'''
		return returncode, output

	@staticmethod
	def lscpu():
		returncode = 0
		output = r'''
Architecture:          aarch64
Byte Order:            Little Endian
CPU(s):                96
On-line CPU(s) list:   0-95
Thread(s) per core:    1
Core(s) per socket:    48
Socket(s):             2
NUMA node(s):          2
L1d cache:             32K
L1i cache:             78K
L2 cache:              16384K
NUMA node0 CPU(s):     0-47
NUMA node1 CPU(s):     48-95
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

	assert info['l1_instruction_cache_size'] == (78 * 1024)
	assert info['l1_data_cache_size'] == (32 * 1024)

	assert info['l2_cache_size'] == (16384 * 1024)

	assert len(info) == 3


def test_get_cpu_info_from_proc_cpuinfo():
	info = cpuinfo._get_cpu_info_from_proc_cpuinfo()

	assert info['flags'] == ['aes', 'asimd', 'atomics', 'crc32', 'evtstrm', 'fp', 'pmull', 'sha1', 'sha2']


@pytest.mark.skip("FIXME: This fails because it does not have a way to get CPU brand string and Hz.")
def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == ''
	assert info['hardware_raw'] == 'FIXME'
	assert info['brand_raw'] == 'FIXME'
	assert info['hz_advertised_friendly'] == 'FIXME'
	assert info['hz_actual_friendly'] == 'FIXME'
	assert info['hz_advertised'] == (1000000000, 0)
	assert info['hz_actual'] == (1000000000, 0)
	assert info['arch'] == 'ARM_8'
	assert info['bits'] == 64
	assert info['count'] == 6

	assert info['arch_string_raw'] == 'aarch64'

	assert info['l1_instruction_cache_size'] == (78 * 1024)
	assert info['l1_data_cache_size'] == (32 * 1024)

	assert info['l2_cache_size'] == (16384 * 1024)
	assert info['l2_cache_line_size'] == 0
	assert info['l2_cache_associativity'] == 0

	assert info['l3_cache_size'] == 0

	assert info['stepping'] == 0
	assert info['model'] == 0
	assert info['family'] == 0
	assert info['processor_type'] == 0
	assert info['flags'] == ['aes', 'asimd', 'atomics', 'crc32', 'evtstrm', 'fp', 'pmull', 'sha1', 'sha2']
