# OS X 10.12 Sierra
# Darwin version 16

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
machdep.cpu.tsc_ccc.denominator: 0
machdep.cpu.tsc_ccc.numerator: 0
machdep.cpu.thread_count: 4
machdep.cpu.core_count: 2
machdep.cpu.address_bits.virtual: 48
machdep.cpu.address_bits.physical: 36
machdep.cpu.tlb.shared: 512
machdep.cpu.tlb.data.large: 32
machdep.cpu.tlb.data.small: 64
machdep.cpu.tlb.inst.large: 8
machdep.cpu.tlb.inst.small: 64
machdep.cpu.cache.size: 256
machdep.cpu.cache.L2_associativity: 8
machdep.cpu.cache.linesize: 64
machdep.cpu.arch_perf.fixed_width: 48
machdep.cpu.arch_perf.fixed_number: 3
machdep.cpu.arch_perf.events: 0
machdep.cpu.arch_perf.events_number: 7
machdep.cpu.arch_perf.width: 48
machdep.cpu.arch_perf.number: 4
machdep.cpu.arch_perf.version: 3
machdep.cpu.xsave.extended_state1: 1 0 0 0
machdep.cpu.xsave.extended_state: 7 832 832 0
machdep.cpu.thermal.energy_policy: 1
machdep.cpu.thermal.hardware_feedback: 0
machdep.cpu.thermal.package_thermal_intr: 1
machdep.cpu.thermal.fine_grain_clock_mod: 1
machdep.cpu.thermal.core_power_limits: 1
machdep.cpu.thermal.ACNT_MCNT: 1
machdep.cpu.thermal.thresholds: 2
machdep.cpu.thermal.invariant_APIC_timer: 1
machdep.cpu.thermal.dynamic_acceleration: 1
machdep.cpu.thermal.sensor: 1
machdep.cpu.mwait.sub_Cstates: 135456
machdep.cpu.mwait.extensions: 3
machdep.cpu.mwait.linesize_max: 64
machdep.cpu.mwait.linesize_min: 64
machdep.cpu.processor_flag: 4
machdep.cpu.microcode_version: 40
machdep.cpu.cores_per_package: 8
machdep.cpu.logical_per_package: 16
machdep.cpu.extfeatures: SYSCALL XD EM64T LAHF RDTSCP TSCI
machdep.cpu.features: FPU VME DE PSE TSC MSR PAE MCE CX8 APIC SEP MTRR PGE MCA CMOV PAT PSE36 CLFSH DS ACPI MMX FXSR SSE SSE2 SS HTT TM PBE SSE3 PCLMULQDQ DTES64 MON DSCPL VMX SMX EST TM2 SSSE3 CX16 TPR PDCM SSE4.1 SSE4.2 x2APIC POPCNT AES PCID XSAVE OSXSAVE TSCTMR AVX1.0
machdep.cpu.brand: 0
machdep.cpu.signature: 132775
machdep.cpu.extfeature_bits: 4967106816
machdep.cpu.feature_bits: 2286390448420027391
machdep.cpu.stepping: 7
machdep.cpu.extfamily: 0
machdep.cpu.extmodel: 2
machdep.cpu.model: 42
machdep.cpu.family: 6
machdep.cpu.brand_string: Intel(R) Core(TM) i5-2557M CPU @ 1.70GHz
machdep.cpu.vendor: GenuineIntel
machdep.cpu.max_ext: 2147483656
machdep.cpu.max_basic: 13
hw.cpufrequency: 1700000000
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
	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-2557M CPU @ 1.70GHz'
	assert info['hz_advertised_friendly'] == '1.7000 GHz'
	assert info['hz_actual_friendly'] == '1.7000 GHz'
	assert info['hz_advertised'] == (1700000000, 0)
	assert info['hz_actual'] == (1700000000, 0)

	assert info['l2_cache_size'] == (256 * 1024)

	assert info['stepping'] == 7
	assert info['model'] == 42
	assert info['family'] == 6

	assert info['flags'] == [
		'acpi',
		'aes',
		'apic',
		'avx1.0',
		'clfsh',
		'cmov',
		'cx16',
		'cx8',
		'de',
		'ds',
		'dscpl',
		'dtes64',
		'em64t',
		'est',
		'fpu',
		'fxsr',
		'htt',
		'lahf',
		'mca',
		'mce',
		'mmx',
		'mon',
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
		'popcnt',
		'pse',
		'pse36',
		'rdtscp',
		'sep',
		'smx',
		'ss',
		'sse',
		'sse2',
		'sse3',
		'sse4.1',
		'sse4.2',
		'ssse3',
		'syscall',
		'tm',
		'tm2',
		'tpr',
		'tsc',
		'tsci',
		'tsctmr',
		'vme',
		'vmx',
		'x2apic',
		'xd',
		'xsave',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-2557M CPU @ 1.70GHz'
	assert info['hz_advertised_friendly'] == '1.7000 GHz'
	assert info['hz_actual_friendly'] == '1.7000 GHz'
	assert info['hz_advertised'] == (1700000000, 0)
	assert info['hz_actual'] == (1700000000, 0)
	assert info['arch'] == 'X86_64'
	assert info['bits'] == 64
	assert info['count'] == 4

	assert info['arch_string_raw'] == 'x86_64'

	assert info['l2_cache_size'] == (256 * 1024)

	assert info['stepping'] == 7
	assert info['model'] == 42
	assert info['family'] == 6

	assert info['flags'] == [
		'acpi',
		'aes',
		'apic',
		'avx1.0',
		'clfsh',
		'cmov',
		'cx16',
		'cx8',
		'de',
		'ds',
		'dscpl',
		'dtes64',
		'em64t',
		'est',
		'fpu',
		'fxsr',
		'htt',
		'lahf',
		'mca',
		'mce',
		'mmx',
		'mon',
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
		'popcnt',
		'pse',
		'pse36',
		'rdtscp',
		'sep',
		'smx',
		'ss',
		'sse',
		'sse2',
		'sse3',
		'sse4.1',
		'sse4.2',
		'ssse3',
		'syscall',
		'tm',
		'tm2',
		'tpr',
		'tsc',
		'tsci',
		'tsctmr',
		'vme',
		'vmx',
		'x2apic',
		'xd',
		'xsave',
	]
