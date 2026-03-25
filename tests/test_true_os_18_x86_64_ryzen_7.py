import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 8
	is_windows = False
	arch_string_raw = 'amd64'
	uname_string_raw = 'amd64'
	can_cpuid = False

	@staticmethod
	def has_dmesg():
		return True

	@staticmethod
	def dmesg_a():
		retcode = 0
		output = r'''Copyright (c) 1992-2018 The FreeBSD Project.
Copyright (c) 1979, 1980, 1983, 1986, 1988, 1989, 1991, 1992, 1993, 1994
	The Regents of the University of California. All rights reserved.
FreeBSD is a registered trademark of The FreeBSD Foundation.
FreeBSD 12.0-CURRENT #26 fa797a5a3(trueos-stable-18.03): Mon Mar 26 00:24:47 UTC 2018
    root@chimera:/usr/obj/usr/src/amd64.amd64/sys/GENERIC amd64
FreeBSD clang version 6.0.0 (branches/release_60 324090) (based on LLVM 6.0.0)
VT(vga): text 80x25
CPU: AMD Ryzen 7 2700X Eight-Core Processor          (3693.15-MHz K8-class CPU)
  Origin="AuthenticAMD"  Id=0x800f82  Family=0x17  Model=0x8  Stepping=2
  Features=0x1783fbff<FPU,VME,DE,PSE,TSC,MSR,PAE,MCE,CX8,APIC,SEP,MTRR,PGE,MCA,CMOV,PAT,PSE36,MMX,FXSR,SSE,SSE2,HTT>
  Features2=0x5ed82203<SSE3,PCLMULQDQ,SSSE3,CX16,SSE4.1,SSE4.2,MOVBE,POPCNT,AESNI,XSAVE,OSXSAVE,AVX,RDRAND>
  AMD Features=0x2a500800<SYSCALL,NX,MMX+,FFXSR,RDTSCP,LM>
  AMD Features2=0x1f3<LAHF,CMP,CR8,ABM,SSE4A,MAS,Prefetch>
  Structured Extended Features=0x40021<FSGSBASE,AVX2,RDSEED>
  TSC: P-state invariant

 '''
		return retcode, output


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
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 10
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 17


def test_get_cpu_info_from_dmesg():
	info = cpuinfo._get_cpu_info_from_dmesg()

	assert info['vendor_id_raw'] == 'AuthenticAMD'
	assert info['brand_raw'] == 'AMD Ryzen 7 2700X Eight-Core Processor'
	assert info['hz_advertised_friendly'] == '3.6932 GHz'
	assert info['hz_actual_friendly'] == '3.6932 GHz'
	assert info['hz_advertised'] == (3693150000, 0)
	assert info['hz_actual'] == (3693150000, 0)

	assert info['stepping'] == 2
	assert info['model'] == 8
	assert info['family'] == 23

	assert info['flags'] == [
		'abm',
		'aesni',
		'apic',
		'avx',
		'cmov',
		'cmp',
		'cr8',
		'cx16',
		'cx8',
		'de',
		'ffxsr',
		'fpu',
		'fxsr',
		'htt',
		'lahf',
		'lm',
		'mas',
		'mca',
		'mce',
		'mmx',
		'mmx+',
		'movbe',
		'msr',
		'mtrr',
		'nx',
		'osxsave',
		'pae',
		'pat',
		'pclmulqdq',
		'pge',
		'popcnt',
		'prefetch',
		'pse',
		'pse36',
		'rdrand',
		'rdtscp',
		'sep',
		'sse',
		'sse2',
		'sse3',
		'sse4.1',
		'sse4.2',
		'sse4a',
		'ssse3',
		'syscall',
		'tsc',
		'vme',
		'xsave',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == 'AuthenticAMD'
	assert info['brand_raw'] == 'AMD Ryzen 7 2700X Eight-Core Processor'
	assert info['hz_advertised_friendly'] == '3.6932 GHz'
	assert info['hz_actual_friendly'] == '3.6932 GHz'
	assert info['hz_advertised'] == (3693150000, 0)
	assert info['hz_actual'] == (3693150000, 0)

	assert info['arch'] == 'X86_64'
	assert info['bits'] == 64
	assert info['count'] == 8
	assert info['arch_string_raw'] == 'amd64'

	assert info['stepping'] == 2
	assert info['model'] == 8
	assert info['family'] == 23

	assert info['flags'] == [
		'abm',
		'aesni',
		'apic',
		'avx',
		'cmov',
		'cmp',
		'cr8',
		'cx16',
		'cx8',
		'de',
		'ffxsr',
		'fpu',
		'fxsr',
		'htt',
		'lahf',
		'lm',
		'mas',
		'mca',
		'mce',
		'mmx',
		'mmx+',
		'movbe',
		'msr',
		'mtrr',
		'nx',
		'osxsave',
		'pae',
		'pat',
		'pclmulqdq',
		'pge',
		'popcnt',
		'prefetch',
		'pse',
		'pse36',
		'rdrand',
		'rdtscp',
		'sep',
		'sse',
		'sse2',
		'sse3',
		'sse4.1',
		'sse4.2',
		'sse4a',
		'ssse3',
		'syscall',
		'tsc',
		'vme',
		'xsave',
	]
