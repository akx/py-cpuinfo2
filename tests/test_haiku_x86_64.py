import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 4
	is_windows = False
	arch_string_raw = 'BePC'
	uname_string_raw = 'x86_64'
	can_cpuid = False

	@staticmethod
	def has_sysinfo():
		return True

	@staticmethod
	def sysinfo_cpu():
		returncode = 0
		output = r'''
1 Intel Core i7, revision 106e5 running at 2933MHz

CPU #0: "Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz"
        Signature: 0x0106e5; Type 0, family 6, model 30, stepping 5
        Features: 0x078bfbff
                FPU VME DE PSE TSC MSR PAE MCE CX8 APIC SEP MTRR PGE MCA CMOV PAT
                PSE36 CFLUSH MMX FXSTR SSE SSE2
        Extended Features (0x00000001): 0x00180209
                SSE3 MONITOR SSSE3 SSE4.1 SSE4.2
        Extended Features (0x80000001): 0x28100800
                SCE NX RDTSCP 64

        L2 Data cache fully associative, 1 lines/tag, 64 bytes/line
        L2 cache: 0 KB, 1-way set associative, 0 lines/tag, 63 bytes/line

        L0 Data TLB: 2M/4M-bytes pages, 4-way set associative, 32 entries
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
	assert info['hz_advertised_friendly'] == '2.9330 GHz'
	assert info['hz_actual_friendly'] == '2.9330 GHz'
	assert info['hz_advertised'] == (2933000000, 0)
	assert info['hz_actual'] == (2933000000, 0)

	assert info['stepping'] == 5
	assert info['model'] == 30
	assert info['family'] == 6
	assert info['flags'] == [
		'64',
		'apic',
		'cflush',
		'cmov',
		'cx8',
		'de',
		'fpu',
		'fxstr',
		'mca',
		'mce',
		'mmx',
		'monitor',
		'msr',
		'mtrr',
		'nx',
		'pae',
		'pat',
		'pge',
		'pse',
		'pse36',
		'rdtscp',
		'sce',
		'sep',
		'sse',
		'sse2',
		'sse3',
		'sse4.1',
		'sse4.2',
		'ssse3',
		'tsc',
		'vme',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['brand_raw'] == 'Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz'
	assert info['hz_advertised_friendly'] == '2.9330 GHz'
	assert info['hz_actual_friendly'] == '2.9330 GHz'
	assert info['hz_advertised'] == (2933000000, 0)
	assert info['hz_actual'] == (2933000000, 0)
	assert info['arch'] == 'X86_32'
	assert info['bits'] == 32
	assert info['count'] == 4

	assert info['arch_string_raw'] == 'BePC'

	assert info['stepping'] == 5
	assert info['model'] == 30
	assert info['family'] == 6
	assert info['flags'] == [
		'64',
		'apic',
		'cflush',
		'cmov',
		'cx8',
		'de',
		'fpu',
		'fxstr',
		'mca',
		'mce',
		'mmx',
		'monitor',
		'msr',
		'mtrr',
		'nx',
		'pae',
		'pat',
		'pge',
		'pse',
		'pse36',
		'rdtscp',
		'sce',
		'sep',
		'sse',
		'sse2',
		'sse3',
		'sse4.1',
		'sse4.2',
		'ssse3',
		'tsc',
		'vme',
	]
