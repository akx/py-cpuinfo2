# macOS on Apple Silicon (ARM64)
# Apple M2 Max

import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 12
	is_windows = False
	arch_string_raw = 'arm64'
	uname_string_raw = 'arm64'
	can_cpuid = False

	@staticmethod
	def has_sysctl():
		return True

	@staticmethod
	def sysctl_machdep_cpu_hw_cpufrequency():
		returncode = 0
		output = r'''
machdep.cpu.cores_per_package: 12
machdep.cpu.core_count: 12
machdep.cpu.logical_per_package: 12
machdep.cpu.thread_count: 12
machdep.cpu.brand_string: Apple M2 Max
hw.l1icachesize: 131072
hw.l1dcachesize: 65536
hw.l2cachesize: 4194304
hw.cachelinesize: 128
hw.optional.arm.FEAT_CRC32: 1
hw.optional.arm.FEAT_FlagM: 1
hw.optional.arm.FEAT_FlagM2: 1
hw.optional.arm.FEAT_FHM: 1
hw.optional.arm.FEAT_DotProd: 1
hw.optional.arm.FEAT_SHA3: 1
hw.optional.arm.FEAT_RDM: 1
hw.optional.arm.FEAT_LSE: 1
hw.optional.arm.FEAT_SHA256: 1
hw.optional.arm.FEAT_SHA512: 1
hw.optional.arm.FEAT_SHA1: 1
hw.optional.arm.FEAT_AES: 1
hw.optional.arm.FEAT_PMULL: 1
hw.optional.arm.FEAT_SPECRES: 0
hw.optional.arm.FEAT_SB: 1
hw.optional.arm.FEAT_FRINTTS: 1
hw.optional.arm.FEAT_PACIMP: 1
hw.optional.arm.FEAT_LRCPC: 1
hw.optional.arm.FEAT_LRCPC2: 1
hw.optional.arm.FEAT_FCMA: 1
hw.optional.arm.FEAT_JSCVT: 1
hw.optional.arm.FEAT_PAuth: 1
hw.optional.arm.FEAT_PAuth2: 1
hw.optional.arm.FEAT_FPAC: 1
hw.optional.arm.FEAT_FPACCOMBINE: 0
hw.optional.arm.FEAT_DPB: 1
hw.optional.arm.FEAT_DPB2: 1
hw.optional.arm.FEAT_BF16: 1
hw.optional.arm.FEAT_I8MM: 1
hw.optional.arm.FEAT_ECV: 1
hw.optional.arm.FEAT_LSE2: 1
hw.optional.arm.FEAT_CSV2: 1
hw.optional.arm.FEAT_CSV3: 1
hw.optional.arm.FEAT_DIT: 1
hw.optional.arm.AdvSIMD: 1
hw.optional.arm.AdvSIMD_HPFPCvt: 1
hw.optional.arm.FEAT_FP16: 1
hw.optional.arm.FEAT_SSBS: 1
hw.optional.arm.FEAT_BTI: 1
hw.optional.arm.FEAT_SME: 0
hw.optional.arm.FEAT_SME2: 0
hw.optional.arm.FP_SyncExceptions: 1
hw.optional.floatingpoint: 1
hw.optional.neon: 1
hw.optional.neon_hpfp: 1
hw.optional.neon_fp16: 1
hw.optional.armv8_crc32: 1
hw.optional.armv8_gpi: 1
hw.optional.armv8_1_atomics: 1
hw.optional.armv8_2_fhm: 1
hw.optional.armv8_2_sha512: 1
hw.optional.armv8_2_sha3: 1
hw.optional.armv8_3_compnum: 1
hw.optional.ucnormal_mem: 1
hw.optional.arm64: 1
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
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 6
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0


def test_get_cpu_info_from_sysctl():
	info = cpuinfo._get_cpu_info_from_sysctl()

	assert info['brand_raw'] == 'Apple M2 Max'

	assert info['l1_data_cache_size'] == 65536
	assert info['l1_instruction_cache_size'] == 131072
	assert info['l2_cache_size'] == 4194304
	assert info['l2_cache_line_size'] == 128

	assert 'vendor_id_raw' not in info
	assert 'hz_advertised_friendly' not in info
	assert 'stepping' not in info

	assert info['flags'] == [
		'advsimd',
		'advsimd_hpfpcvt',
		'arm64',
		'armv8_1_atomics',
		'armv8_2_fhm',
		'armv8_2_sha3',
		'armv8_2_sha512',
		'armv8_3_compnum',
		'armv8_crc32',
		'armv8_gpi',
		'feat_aes',
		'feat_bf16',
		'feat_bti',
		'feat_crc32',
		'feat_csv2',
		'feat_csv3',
		'feat_dit',
		'feat_dotprod',
		'feat_dpb',
		'feat_dpb2',
		'feat_ecv',
		'feat_fcma',
		'feat_fhm',
		'feat_flagm',
		'feat_flagm2',
		'feat_fp16',
		'feat_fpac',
		'feat_frintts',
		'feat_i8mm',
		'feat_jscvt',
		'feat_lrcpc',
		'feat_lrcpc2',
		'feat_lse',
		'feat_lse2',
		'feat_pacimp',
		'feat_pauth',
		'feat_pauth2',
		'feat_pmull',
		'feat_rdm',
		'feat_sb',
		'feat_sha1',
		'feat_sha256',
		'feat_sha3',
		'feat_sha512',
		'feat_ssbs',
		'floatingpoint',
		'fp_syncexceptions',
		'neon',
		'neon_fp16',
		'neon_hpfp',
		'ucnormal_mem',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['brand_raw'] == 'Apple M2 Max'
	assert info['arch'] == 'ARM_8'
	assert info['bits'] == 64
	assert info['count'] == 12
	assert info['arch_string_raw'] == 'arm64'

	assert info['l1_data_cache_size'] == 65536
	assert info['l1_instruction_cache_size'] == 131072
	assert info['l2_cache_size'] == 4194304
	assert info['l2_cache_line_size'] == 128

	assert 'feat_aes' in info['flags']
	assert 'neon' in info['flags']
	assert 'arm64' in info['flags']
