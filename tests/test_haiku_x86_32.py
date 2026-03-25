import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '32bit'
	cpu_count = 4
	is_windows = False
	arch_string_raw = 'BePC'
	uname_string_raw = 'x86_32'
	can_cpuid = False

	@staticmethod
	def has_sysinfo():
		return True

	@staticmethod
	def sysinfo_cpu():
		returncode = 0
		output = r'''
4 Intel Core i7, revision 46e5 running at 2928MHz (ID: 0x00000000 0x00000000)

CPU #0: "Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz"
	Type 0, family 6, model 30, stepping 5, features 0x178bfbbf
		FPU VME DE PSE TSC MSR MCE CX8 APIC SEP MTRR PGE MCA CMOV PAT PSE36
		CFLUSH MMX FXSTR SSE SSE2 HTT
	Extended Intel: 0x00000201
		SSE3 SSSE3
	Extended AMD: type 0, family 0, model 0, stepping 0, features 0x08000000
		RDTSCP
	Power Management Features:

	L2 Data cache 8-way set associative, 1 lines/tag, 64 bytes/line
	L2 cache: 0 KB, 1-way set associative, 0 lines/tag, 63 bytes/line

	Data TLB: 2M/4M-bytes pages, 4-way set associative, 32 entries
	Data TLB: 4k-byte pages, 4-way set associative, 64 entries
	Inst TLB: 2M/4M-bytes pages, fully associative, 7 entries
	L3 cache: 8192 KB, 16-way set associative, 64-bytes/line
	Inst TLB: 4K-bytes pages, 4-way set associative, 128 entries
	64-byte Prefetching
	L1 data cache: 32 KB, 8-way set associative, 64 bytes/line
	L2 cache: 256 KB (MLC), 8-way set associative, 64-bytes/line
	Shared 2nd-level TLB: 4K, 4-way set associative, 512 entries
	Unknown cache descriptor 0x09
'''
		return returncode, output


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_registry()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 0
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 0
	assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 9
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 16


def test_get_cpu_info_from_sysinfo():
	info = cpuinfo._get_cpu_info_from_sysinfo()

	assert info['brand_raw'] == 'Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz'
	assert info['hz_advertised_friendly'] == '2.9300 GHz'
	assert info['hz_actual_friendly'] == '2.9300 GHz'
	assert info['hz_advertised'] == (2930000000, 0)
	assert info['hz_actual'] == (2930000000, 0)

	assert info['stepping'] == 5
	assert info['model'] == 30
	assert info['family'] == 6
	assert info['flags'] == [
		'apic',
		'cflush',
		'cmov',
		'cx8',
		'de',
		'fpu',
		'fxstr',
		'htt',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'pat',
		'pge',
		'pse',
		'pse36',
		'rdtscp',
		'sep',
		'sse',
		'sse2',
		'sse3',
		'ssse3',
		'tsc',
		'vme',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['brand_raw'] == 'Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz'
	assert info['hz_advertised_friendly'] == '2.9300 GHz'
	assert info['hz_actual_friendly'] == '2.9300 GHz'
	assert info['hz_advertised'] == (2930000000, 0)
	assert info['hz_actual'] == (2930000000, 0)
	assert info['arch'] == 'X86_32'
	assert info['bits'] == 32
	assert info['count'] == 4

	assert info['arch_string_raw'] == 'BePC'

	assert info['stepping'] == 5
	assert info['model'] == 30
	assert info['family'] == 6
	assert info['flags'] == [
		'apic',
		'cflush',
		'cmov',
		'cx8',
		'de',
		'fpu',
		'fxstr',
		'htt',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'pat',
		'pge',
		'pse',
		'pse36',
		'rdtscp',
		'sep',
		'sse',
		'sse2',
		'sse3',
		'ssse3',
		'tsc',
		'vme',
	]
