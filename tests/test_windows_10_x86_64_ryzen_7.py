import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 16
	is_windows = True
	arch_string_raw = 'AMD64'
	uname_string_raw = 'AMD64 Family 23 Model 8 Stepping 2, AuthenticAMD'
	can_cpuid = True

	@staticmethod
	def winreg_processor_brand():
		return 'AMD Ryzen 7 2700X Eight-Core Processor         '

	@staticmethod
	def winreg_vendor_id_raw():
		return 'AuthenticAMD'

	@staticmethod
	def winreg_arch_string_raw():
		return 'AMD64'

	@staticmethod
	def winreg_hz_actual():
		return 3693

	@staticmethod
	def winreg_feature_bits():
		return 1010515455


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	monkeypatch.setattr(cpuinfo, "CAN_CALL_CPUID_IN_SUBPROCESS", False)
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)

	helpers.monkey_patch_cpuid(
		cpuinfo,
		3693000000,
		[
			# get_max_extension_support
			0x8000001F,
			# get_cache
			0x2006140,
			# get_info
			0x800F82,
			# get_processor_brand
			0x20444D41,
			0x657A7952,
			0x2037206E,
			0x30303732,
			0x69452058,
			0x2D746867,
			0x65726F43,
			0x6F725020,
			0x73736563,
			0x2020726F,
			0x20202020,
			0x202020,
			# get_vendor_id
			0x68747541,
			0x444D4163,
			0x69746E65,
			# get_flags
			0x178BFBFF,
			0x7ED8320B,
			0x209C01A9,
			0x0,
			0x20000000,
			0x35C233FF,
		],
		monkeypatch=monkeypatch,
	)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_wmic()) == 0
	assert len(cpuinfo._get_cpu_info_from_registry()) == 7
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 0
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 0
	assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 11
	assert len(cpuinfo._get_cpu_info_from_platform_uname()) == 3
	assert len(cpuinfo._get_cpu_info_internal()) == 20


def test_get_cpu_info_from_cpuid():
	info = cpuinfo._get_cpu_info_from_cpuid()

	assert info['vendor_id_raw'] == 'AuthenticAMD'
	assert info['brand_raw'] == 'AMD Ryzen 7 2700X Eight-Core Processor'
	# self.assertEqual('3.6930 GHz', info['hz_advertised_friendly'])
	assert info['hz_actual_friendly'] == '3.6930 GHz'
	# self.assertEqual((3693000000, 0), info['hz_advertised'])
	assert info['hz_actual'] == (3693000000, 0)

	assert info['stepping'] == 2
	assert info['model'] == 8
	assert info['family'] == 23

	assert info['l2_cache_size'] == (64 * 1024)
	assert info['l2_cache_line_size'] == 512
	assert info['l2_cache_associativity'] == 6

	assert info['flags'] == [
		'3dnowprefetch',
		'abm',
		'adx',
		'aes',
		'apic',
		'avx',
		'avx2',
		'bmi1',
		'bmi2',
		'clflush',
		'clflushopt',
		'cmov',
		'cmp_legacy',
		'cr8_legacy',
		'cx16',
		'cx8',
		'dbx',
		'de',
		'extapic',
		'f16c',
		'fma',
		'fpu',
		'fxsr',
		'ht',
		'lahf_lm',
		'lm',
		'mca',
		'mce',
		'misalignsse',
		'mmx',
		'monitor',
		'movbe',
		'msr',
		'mtrr',
		'osvw',
		'osxsave',
		'pae',
		'pat',
		'pci_l2i',
		'pclmulqdq',
		'perfctr_core',
		'perfctr_nb',
		'pge',
		'pni',
		'popcnt',
		'pse',
		'pse36',
		'rdrnd',
		'rdseed',
		'sep',
		'sha',
		'skinit',
		'smap',
		'smep',
		'sse',
		'sse2',
		'sse4_1',
		'sse4_2',
		'sse4a',
		'ssse3',
		'svm',
		'tce',
		'topoext',
		'tsc',
		'vme',
		'wdt',
		'xsave',
	]


def test_get_cpu_info_from_platform_uname():
	info = cpuinfo._get_cpu_info_from_platform_uname()

	assert info['stepping'] == 2
	assert info['model'] == 8
	assert info['family'] == 23


def test_get_cpu_info_from_registry():
	info = cpuinfo._get_cpu_info_from_registry()

	assert info['vendor_id_raw'] == 'AuthenticAMD'
	assert info['brand_raw'] == 'AMD Ryzen 7 2700X Eight-Core Processor'
	assert info['hz_advertised_friendly'] == '3.6930 GHz'
	assert info['hz_actual_friendly'] == '3.6930 GHz'
	assert info['hz_advertised'] == (3693000000, 0)
	assert info['hz_actual'] == (3693000000, 0)

	assert info['flags'] == [
		'3dnow',
		'clflush',
		'cmov',
		'de',
		'dts',
		'fxsr',
		'ia64',
		'mca',
		'mmx',
		'msr',
		'mtrr',
		'pse',
		'sep',
		'sepamd',
		'serial',
		'ss',
		'sse',
		'sse2',
		'tm',
		'tsc',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == 'AuthenticAMD'
	assert info['brand_raw'] == 'AMD Ryzen 7 2700X Eight-Core Processor'
	assert info['hz_advertised_friendly'] == '3.6930 GHz'
	assert info['hz_actual_friendly'] == '3.6930 GHz'
	assert info['hz_advertised'] == (3693000000, 0)
	assert info['hz_actual'] == (3693000000, 0)
	assert info['arch'] == 'X86_64'
	assert info['bits'] == 64
	assert info['count'] == 16

	assert info['arch_string_raw'] == 'AMD64'

	assert info['stepping'] == 2
	assert info['model'] == 8
	assert info['family'] == 23

	assert info['l2_cache_size'] == (64 * 1024)
	assert info['l2_cache_associativity'] == 6
	assert info['l2_cache_line_size'] == 512

	assert info['flags'] == [
		'3dnow',
		'3dnowprefetch',
		'abm',
		'adx',
		'aes',
		'apic',
		'avx',
		'avx2',
		'bmi1',
		'bmi2',
		'clflush',
		'clflushopt',
		'cmov',
		'cmp_legacy',
		'cr8_legacy',
		'cx16',
		'cx8',
		'dbx',
		'de',
		'dts',
		'extapic',
		'f16c',
		'fma',
		'fpu',
		'fxsr',
		'ht',
		'ia64',
		'lahf_lm',
		'lm',
		'mca',
		'mce',
		'misalignsse',
		'mmx',
		'monitor',
		'movbe',
		'msr',
		'mtrr',
		'osvw',
		'osxsave',
		'pae',
		'pat',
		'pci_l2i',
		'pclmulqdq',
		'perfctr_core',
		'perfctr_nb',
		'pge',
		'pni',
		'popcnt',
		'pse',
		'pse36',
		'rdrnd',
		'rdseed',
		'sep',
		'sepamd',
		'serial',
		'sha',
		'skinit',
		'smap',
		'smep',
		'ss',
		'sse',
		'sse2',
		'sse4_1',
		'sse4_2',
		'sse4a',
		'ssse3',
		'svm',
		'tce',
		'tm',
		'topoext',
		'tsc',
		'vme',
		'wdt',
		'xsave',
	]
