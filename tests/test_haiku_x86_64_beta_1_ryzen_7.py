import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '32bit'
	cpu_count = 2
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
2 AMD Ryzen 7, revision 800f82 running at 3693MHz

CPU #0: "AMD Ryzen 7 2700X Eight-Core Processor         "
	Signature: 0x800f82; Type 0, family 23, model 8, stepping 2
	Features: 0x178bfbff
		FPU VME DE PSE TSC MSR PAE MCE CX8 APIC SEP MTRR PGE MCA CMOV PAT
		PSE36 CFLUSH MMX FXSTR SSE SSE2 HTT
	Extended Features (0x00000001): 0x56d82203
		SSE3 PCLMULDQ SSSE3 CX16 SSE4.1 SSE4.2 MOVEB POPCNT AES XSAVE AVX RDRND
	Extended Features (0x80000001): 0x2bd3fb7f
		SCE NX AMD-MMX FXSR FFXSR RDTSCP 64
	Extended Features (0x80000007): 0x00000100
		ITSC
	Extended Features (0x80000008): 0x00000000

	Inst TLB: 2M/4M-byte pages, 64 entries, fully associative
	Data TLB: 2M/4M-byte pages, 64 entries, fully associative
	Inst TLB: 4K-byte pages, 64 entries, fully associative
	Data TLB: 4K-byte pages, 64 entries, fully associative
	L1 inst cache: 32 KB, 8-way set associative, 1 lines/tag, 64 bytes/line
	L1 data cache: 64 KB, 4-way set associative, 1 lines/tag, 64 bytes/line
	L2 cache: 512 KB, 8-way set associative, 1 lines/tag, 64 bytes/line

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

	assert info['brand_raw'] == 'AMD Ryzen 7 2700X Eight-Core Processor'
	assert info['hz_advertised_friendly'] == '3.6930 GHz'
	assert info['hz_actual_friendly'] == '3.6930 GHz'
	assert info['hz_advertised'] == (3693000000, 0)
	assert info['hz_actual'] == (3693000000, 0)

	assert info['stepping'] == 2
	assert info['model'] == 8
	assert info['family'] == 23
	assert info['flags'] == [
		'64',
		'aes',
		'amd-mmx',
		'apic',
		'avx',
		'cflush',
		'cmov',
		'cx16',
		'cx8',
		'de',
		'ffxsr',
		'fpu',
		'fxsr',
		'fxstr',
		'htt',
		'mca',
		'mce',
		'mmx',
		'moveb',
		'msr',
		'mtrr',
		'nx',
		'pae',
		'pat',
		'pclmuldq',
		'pge',
		'popcnt',
		'pse',
		'pse36',
		'rdrnd',
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
		'xsave',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['brand_raw'] == 'AMD Ryzen 7 2700X Eight-Core Processor'
	assert info['hz_advertised_friendly'] == '3.6930 GHz'
	assert info['hz_actual_friendly'] == '3.6930 GHz'
	assert info['hz_advertised'] == (3693000000, 0)
	assert info['hz_actual'] == (3693000000, 0)
	assert info['arch'] == 'X86_32'
	assert info['bits'] == 32
	assert info['count'] == 2

	assert info['arch_string_raw'] == 'BePC'

	assert info['stepping'] == 2
	assert info['model'] == 8
	assert info['family'] == 23
	assert info['flags'] == [
		'64',
		'aes',
		'amd-mmx',
		'apic',
		'avx',
		'cflush',
		'cmov',
		'cx16',
		'cx8',
		'de',
		'ffxsr',
		'fpu',
		'fxsr',
		'fxstr',
		'htt',
		'mca',
		'mce',
		'mmx',
		'moveb',
		'msr',
		'mtrr',
		'nx',
		'pae',
		'pat',
		'pclmuldq',
		'pge',
		'popcnt',
		'pse',
		'pse36',
		'rdrnd',
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
		'xsave',
	]
