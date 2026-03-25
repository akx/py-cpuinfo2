import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 4
	is_windows = True
	arch_string_raw = 'AMD64'
	uname_string_raw = 'Intel64 Family 6 Model 69 Stepping 1, GenuineIntel'
	can_cpuid = True

	@staticmethod
	def has_wmic():
		return True

	@staticmethod
	def wmic_cpu():
		returncode = 0
		output = r'''
Caption=Intel64 Family 6 Model 69 Stepping 1
CurrentClockSpeed=2494
Description=Intel64 Family 6 Model 69 Stepping 1
L2CacheSize=512
L3CacheSize=3072
Manufacturer=GenuineIntel
Name=Intel(R) Core(TM) i5-4300U CPU @ 1.90GHz

'''
		return returncode, output

	@staticmethod
	def winreg_processor_brand():
		return 'Intel(R) Core(TM) i5-4300U CPU @ 1.90GHz'

	@staticmethod
	def winreg_vendor_id_raw():
		return 'GenuineIntel'

	@staticmethod
	def winreg_arch_string_raw():
		return 'AMD64'

	@staticmethod
	def winreg_hz_actual():
		return 2494

	@staticmethod
	def winreg_feature_bits():
		return 1025196031


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	monkeypatch.setattr(cpuinfo, "CAN_CALL_CPUID_IN_SUBPROCESS", False)
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)

	helpers.monkey_patch_cpuid(
		cpuinfo,
		2494000000,
		[
			# max_extension_support
			0x80000008,
			# get_cache
			0x1006040,
			# get_info
			0x40651,
			# get_processor_brand
			0x65746E49,
			0x2952286C,
			0x726F4320,
			0x4D542865,
			0x35692029,
			0x3033342D,
			0x43205530,
			0x40205550,
			0x392E3120,
			0x7A484730,
			0x0,
			0x0,
			# get_vendor_id
			0x756E6547,
			0x6C65746E,
			0x49656E69,
			# get_flags
			0xBFEBFBFF,
			0x7FFAFBFF,
			0x27AB,
			0x0,
			0x0,
			0x21,
		],
		monkeypatch=monkeypatch,
	)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_wmic()) == 11
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
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 13
	assert len(cpuinfo._get_cpu_info_from_platform_uname()) == 3
	assert len(cpuinfo._get_cpu_info_internal()) == 21


def test_get_cpu_info_from_cpuid():
	info = cpuinfo._get_cpu_info_from_cpuid()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-4300U CPU @ 1.90GHz'
	# self.assertEqual('2.4940 GHz', info['hz_advertised_friendly'])
	assert info['hz_actual_friendly'] == '2.4940 GHz'
	# self.assertEqual((2494000000, 0), info['hz_advertised'])
	assert info['hz_actual'] == (2494000000, 0)

	assert info['stepping'] == 1
	assert info['model'] == 69
	assert info['family'] == 6

	assert info['l2_cache_size'] == (64 * 1024)
	assert info['l2_cache_line_size'] == 256
	assert info['l2_cache_associativity'] == 6

	assert info['flags'] == [
		'abm',
		'acpi',
		'aes',
		'apic',
		'avx',
		'avx2',
		'bmi1',
		'bmi2',
		'clflush',
		'cmov',
		'cx16',
		'cx8',
		'de',
		'ds_cpl',
		'dtes64',
		'dts',
		'erms',
		'est',
		'f16c',
		'fma',
		'fpu',
		'fxsr',
		'ht',
		'invpcid',
		'lahf_lm',
		'mca',
		'mce',
		'mmx',
		'monitor',
		'movbe',
		'msr',
		'mtrr',
		'osxsave',
		'pae',
		'pat',
		'pbe',
		'pcid',
		'pclmulqdq',
		'pdcm',
		'pge',
		'pni',
		'popcnt',
		'pse',
		'pse36',
		'rdrnd',
		'sep',
		'smep',
		'smx',
		'ss',
		'sse',
		'sse2',
		'sse4_1',
		'sse4_2',
		'ssse3',
		'tm',
		'tm2',
		'tsc',
		'tscdeadline',
		'vme',
		'vmx',
		'x2apic',
		'xsave',
		'xtpr',
	]


def test_get_cpu_info_from_platform_uname():
	info = cpuinfo._get_cpu_info_from_platform_uname()

	assert info['stepping'] == 1
	assert info['model'] == 69
	assert info['family'] == 6


def test_get_cpu_info_from_wmic():
	info = cpuinfo._get_cpu_info_from_wmic()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-4300U CPU @ 1.90GHz'
	assert info['hz_advertised_friendly'] == '1.9000 GHz'
	assert info['hz_actual_friendly'] == '2.4940 GHz'
	assert info['hz_advertised'] == (1900000000, 0)
	assert info['hz_actual'] == (2494000000, 0)

	assert info['stepping'] == 1
	assert info['model'] == 69
	assert info['family'] == 6

	assert info['l2_cache_size'] == (512 * 1024)
	assert info['l3_cache_size'] == (3072 * 1024)


def test_get_cpu_info_from_registry():
	info = cpuinfo._get_cpu_info_from_registry()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-4300U CPU @ 1.90GHz'
	assert info['hz_advertised_friendly'] == '1.9000 GHz'
	assert info['hz_actual_friendly'] == '2.4940 GHz'
	assert info['hz_advertised'] == (1900000000, 0)
	assert info['hz_actual'] == (2494000000, 0)

	assert info['flags'] == [
		'3dnow',
		'acpi',
		'clflush',
		'cmov',
		'de',
		'dts',
		'fxsr',
		'ia64',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'pse',
		'sep',
		'serial',
		'ss',
		'sse',
		'sse2',
		'tm',
		'tsc',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-4300U CPU @ 1.90GHz'
	assert info['hz_advertised_friendly'] == '1.9000 GHz'
	assert info['hz_actual_friendly'] == '2.4940 GHz'
	assert info['hz_advertised'] == (1900000000, 0)
	assert info['hz_actual'] == (2494000000, 0)
	assert info['arch'] == 'X86_64'
	assert info['bits'] == 64
	assert info['count'] == 4

	assert info['arch_string_raw'] == 'AMD64'

	assert info['stepping'] == 1
	assert info['model'] == 69
	assert info['family'] == 6

	assert info['l2_cache_size'] == (512 * 1024)
	assert info['l3_cache_size'] == (3072 * 1024)
	assert info['l2_cache_associativity'] == 6
	assert info['l2_cache_line_size'] == 256

	assert info['flags'] == [
		'3dnow',
		'abm',
		'acpi',
		'aes',
		'apic',
		'avx',
		'avx2',
		'bmi1',
		'bmi2',
		'clflush',
		'cmov',
		'cx16',
		'cx8',
		'de',
		'ds_cpl',
		'dtes64',
		'dts',
		'erms',
		'est',
		'f16c',
		'fma',
		'fpu',
		'fxsr',
		'ht',
		'ia64',
		'invpcid',
		'lahf_lm',
		'mca',
		'mce',
		'mmx',
		'monitor',
		'movbe',
		'msr',
		'mtrr',
		'osxsave',
		'pae',
		'pat',
		'pbe',
		'pcid',
		'pclmulqdq',
		'pdcm',
		'pge',
		'pni',
		'popcnt',
		'pse',
		'pse36',
		'rdrnd',
		'sep',
		'serial',
		'smep',
		'smx',
		'ss',
		'sse',
		'sse2',
		'sse4_1',
		'sse4_2',
		'ssse3',
		'tm',
		'tm2',
		'tsc',
		'tscdeadline',
		'vme',
		'vmx',
		'x2apic',
		'xsave',
		'xtpr',
	]
