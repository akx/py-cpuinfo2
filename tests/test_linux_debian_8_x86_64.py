import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 1
	is_windows = False
	arch_string_raw = 'x86_64'
	uname_string_raw = 'x86_64'
	can_cpuid = False

	@staticmethod
	def has_proc_cpuinfo():
		return True

	@staticmethod
	def cat_proc_cpuinfo():
		returncode = 0
		output = r'''
processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 30
model name	: Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz
stepping	: 5
microcode	: 0x616
cpu MHz		: 2928.283
cache size	: 6144 KB
physical id	: 0
siblings	: 4
core id		: 0
cpu cores	: 4
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 5
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl pni ssse3 lahf_lm
bogomips	: 5856.56
clflush size	: 64
cache_alignment	: 64
address sizes	: 36 bits physical, 48 bits virtual
power management:


'''
		return returncode, output


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_registry()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 0
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 0
	assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) == 11
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 18


def test_get_cpu_info_from_proc_cpuinfo():
	info = cpuinfo._get_cpu_info_from_proc_cpuinfo()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz'
	assert info['hz_advertised_friendly'] == '2.9300 GHz'
	assert info['hz_actual_friendly'] == '2.9283 GHz'
	assert info['hz_advertised'] == (2930000000, 0)
	assert info['hz_actual'] == (2928283000, 0)

	assert info['l3_cache_size'] == (6144 * 1024)

	assert info['stepping'] == 5
	assert info['model'] == 30
	assert info['family'] == 6
	assert info['flags'] == [
		'apic',
		'clflush',
		'cmov',
		'constant_tsc',
		'cx8',
		'de',
		'fpu',
		'fxsr',
		'ht',
		'lahf_lm',
		'lm',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'nopl',
		'nx',
		'pae',
		'pat',
		'pge',
		'pni',
		'pse',
		'pse36',
		'rdtscp',
		'rep_good',
		'sep',
		'sse',
		'sse2',
		'ssse3',
		'syscall',
		'tsc',
		'vme',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Core(TM) i7 CPU         870  @ 2.93GHz'
	assert info['hz_advertised_friendly'] == '2.9300 GHz'
	assert info['hz_actual_friendly'] == '2.9283 GHz'
	assert info['hz_advertised'] == (2930000000, 0)
	assert info['hz_actual'] == (2928283000, 0)
	assert info['arch'] == 'X86_64'
	assert info['bits'] == 64
	assert info['count'] == 1

	assert info['arch_string_raw'] == 'x86_64'

	assert info['l3_cache_size'] == (6144 * 1024)

	assert info['stepping'] == 5
	assert info['model'] == 30
	assert info['family'] == 6
	assert info['flags'] == [
		'apic',
		'clflush',
		'cmov',
		'constant_tsc',
		'cx8',
		'de',
		'fpu',
		'fxsr',
		'ht',
		'lahf_lm',
		'lm',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'nopl',
		'nx',
		'pae',
		'pat',
		'pge',
		'pni',
		'pse',
		'pse36',
		'rdtscp',
		'rep_good',
		'sep',
		'sse',
		'sse2',
		'ssse3',
		'syscall',
		'tsc',
		'vme',
	]
