# OS X 10.9 Mavericks
# Darwin version 13

import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 4
	is_windows = False
	arch_string_raw = 'x86_64'
	uname_string_raw = 'x86_64'
	can_cpuid = False

	@staticmethod
	def has_sysctl():
		return True

	@staticmethod
	def sysctl_machdep_cpu_hw_cpufrequency():
		returncode = 0
		output = r'''
machdep.cpu.max_basic: 5
machdep.cpu.max_ext: 2147483656
machdep.cpu.vendor: GenuineIntel
machdep.cpu.brand_string: Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz
machdep.cpu.family: 6
machdep.cpu.model: 58
machdep.cpu.extmodel: 3
machdep.cpu.extfamily: 0
machdep.cpu.stepping: 9
machdep.cpu.feature_bits: 395049983 2147484161
machdep.cpu.leaf7_feature_bits: 832
machdep.cpu.extfeature_bits: 672139264 1
machdep.cpu.signature: 198313
machdep.cpu.brand: 0
machdep.cpu.features: FPU VME DE PSE TSC MSR PAE MCE CX8 APIC SEP MTRR PGE MCA CMOV PAT PSE36 CLFSH MMX FXSR SSE SSE2 HTT SSE3 SSSE3 VMM
machdep.cpu.leaf7_features: ENFSTRG BMI2 AVX2
machdep.cpu.extfeatures: SYSCALL XD EM64T LAHF RDTSCP
machdep.cpu.logical_per_package: 4
machdep.cpu.cores_per_package: 4
machdep.cpu.microcode_version: 25
machdep.cpu.processor_flag: 1
machdep.cpu.mwait.linesize_min: 0
machdep.cpu.mwait.linesize_max: 0
machdep.cpu.mwait.extensions: 3
machdep.cpu.mwait.sub_Cstates: 0
machdep.cpu.cache.linesize: 64
machdep.cpu.cache.L2_associativity: 8
machdep.cpu.cache.size: 256
machdep.cpu.tlb.inst.large: 8
machdep.cpu.tlb.data.small: 64
machdep.cpu.tlb.data.small_level1: 128
machdep.cpu.tlb.shared: 1024
machdep.cpu.address_bits.physical: 39
machdep.cpu.address_bits.virtual: 48
machdep.cpu.core_count: 4
machdep.cpu.thread_count: 4
hw.cpufrequency: 2890000000
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
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 11
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 18


def test_get_cpu_info_from_sysctl():
	info = cpuinfo._get_cpu_info_from_sysctl()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz'
	assert info['hz_advertised_friendly'] == '3.1000 GHz'
	assert info['hz_actual_friendly'] == '2.8900 GHz'
	assert info['hz_advertised'] == (3100000000, 0)
	assert info['hz_actual'] == (2890000000, 0)

	assert info['l2_cache_size'] == (256 * 1024)

	assert info['stepping'] == 9
	assert info['model'] == 58
	assert info['family'] == 6

	assert info['flags'] == [
		'apic',
		'avx2',
		'bmi2',
		'clfsh',
		'cmov',
		'cx8',
		'de',
		'em64t',
		'enfstrg',
		'fpu',
		'fxsr',
		'htt',
		'lahf',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'pae',
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
		'syscall',
		'tsc',
		'vme',
		'vmm',
		'xd',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz'
	assert info['hz_advertised_friendly'] == '3.1000 GHz'
	assert info['hz_actual_friendly'] == '2.8900 GHz'
	assert info['hz_advertised'] == (3100000000, 0)
	assert info['hz_actual'] == (2890000000, 0)
	assert info['arch'] == 'X86_64'
	assert info['bits'] == 64
	assert info['count'] == 4

	assert info['arch_string_raw'] == 'x86_64'

	assert info['l2_cache_size'] == (256 * 1024)

	assert info['stepping'] == 9
	assert info['model'] == 58
	assert info['family'] == 6

	assert info['flags'] == [
		'apic',
		'avx2',
		'bmi2',
		'clfsh',
		'cmov',
		'cx8',
		'de',
		'em64t',
		'enfstrg',
		'fpu',
		'fxsr',
		'htt',
		'lahf',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'pae',
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
		'syscall',
		'tsc',
		'vme',
		'vmm',
		'xd',
	]
