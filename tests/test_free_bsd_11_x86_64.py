import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 1
	is_windows = False
	arch_string_raw = 'amd64'
	uname_string_raw = 'x86_64'
	can_cpuid = False

	@staticmethod
	def has_dmesg():
		return True

	@staticmethod
	def has_var_run_dmesg_boot():
		return True

	@staticmethod
	def dmesg_a():
		retcode = 0
		output = r'''Copyright (c) 1992-2014 The FreeBSD Project.
Copyright (c) 1979, 1980, 1983, 1986, 1988, 1989, 1991, 1992, 1993, 1994
    The Regents of the University of California. All rights reserved.
FreeBSD is a registered trademark of The FreeBSD Foundation.
FreeBSD 10.0-RELEASE-p17 #0: Tue Sep 16 14:33:46 UTC 2014
    root@amd64-builder.pcbsd.org:/usr/obj/usr/src/sys/GENERIC amd64
FreeBSD clang version 3.3 (tags/RELEASE_33/final 183502) 20130610
VT(vga): text 80x25
CPU: Intel(R) Pentium(R) CPU G640 @ 2.80GHz (2793.73-MHz K8-class CPU)
  Origin="GenuineIntel"  Id=0x206a7  Family=0x6  Model=02a  Stepping=7
  Features=0x1783fbff<FPU,VME,DE,PSE,TSC,MSR,PAE,MCE,CX8,APIC,SEP,MTRR,PGE,MCA,CMOV,PAT,PSE36,MMX,FXSR,SSE,SSE2,HTT>
  Features2=0xc982203<SSE3,PCLMULQDQ,SSSE3,CX16,SSE4.1,SSE4.2,POPCNT,XSAVE,OSXSAVE>
  AMD Features=0x28100800<SYSCALL,NX,RDTSCP,LM>
  AMD Features2=0x1<LAHF>
  TSC: P-state invariant
 '''
		return retcode, output

	@staticmethod
	def cat_var_run_dmesg_boot():
		retcode = 0
		output = r'''
VT(vga): text 80x25
CPU: Intel(R) Pentium(R) CPU G640 @ 2.80GHz (2793.73-MHz K8-class CPU)
  Origin="GenuineIntel"  Id=0x206a7  Family=0x6  Model=02a  Stepping=7
  Features=0x1783fbff<FPU,VME,DE,PSE,TSC,MSR,PAE,MCE,CX8,APIC,SEP,MTRR,PGE,MCA,CMOV,PAT,PSE36,MMX,FXSR,SSE,SSE2,HTT>
  Features2=0xc982203<SSE3,PCLMULQDQ,SSSE3,CX16,SSE4.1,SSE4.2,POPCNT,XSAVE,OSXSAVE>
  AMD Features=0x28100800<SYSCALL,NX,RDTSCP,LM>
  AMD Features2=0x1<LAHF>
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
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 10
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 17


def test_get_cpu_info_from_dmesg():
	info = cpuinfo._get_cpu_info_from_dmesg()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Pentium(R) CPU G640 @ 2.80GHz'
	assert info['hz_advertised_friendly'] == '2.8000 GHz'
	assert info['hz_actual_friendly'] == '2.8000 GHz'
	assert info['hz_advertised'] == (2800000000, 0)
	assert info['hz_actual'] == (2800000000, 0)

	assert info['stepping'] == 7
	assert info['model'] == 42
	assert info['family'] == 6
	assert info['flags'] == [
		'apic',
		'cmov',
		'cx16',
		'cx8',
		'de',
		'fpu',
		'fxsr',
		'htt',
		'lahf',
		'lm',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'nx',
		'osxsave',
		'pae',
		'pat',
		'pclmulqdq',
		'pge',
		'popcnt',
		'pse',
		'pse36',
		'rdtscp',
		'sep',
		'sse',
		'sse2',
		'sse3',
		'sse4.1',
		'sse4.2',
		'ssse3',
		'syscall',
		'tsc',
		'vme',
		'xsave',
	]


def test_get_cpu_info_from_cat_var_run_dmesg_boot():
	info = cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Pentium(R) CPU G640 @ 2.80GHz'
	assert info['hz_advertised_friendly'] == '2.8000 GHz'
	assert info['hz_actual_friendly'] == '2.8000 GHz'
	assert info['hz_advertised'] == (2800000000, 0)
	assert info['hz_actual'] == (2800000000, 0)

	assert info['stepping'] == 7
	assert info['model'] == 42
	assert info['family'] == 6
	assert info['flags'] == [
		'apic',
		'cmov',
		'cx16',
		'cx8',
		'de',
		'fpu',
		'fxsr',
		'htt',
		'lahf',
		'lm',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'nx',
		'osxsave',
		'pae',
		'pat',
		'pclmulqdq',
		'pge',
		'popcnt',
		'pse',
		'pse36',
		'rdtscp',
		'sep',
		'sse',
		'sse2',
		'sse3',
		'sse4.1',
		'sse4.2',
		'ssse3',
		'syscall',
		'tsc',
		'vme',
		'xsave',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(R) Pentium(R) CPU G640 @ 2.80GHz'
	assert info['hz_advertised_friendly'] == '2.8000 GHz'
	assert info['hz_actual_friendly'] == '2.8000 GHz'
	assert info['hz_advertised'] == (2800000000, 0)
	assert info['hz_actual'] == (2800000000, 0)
	assert info['arch'] == 'X86_64'
	assert info['bits'] == 64
	assert info['count'] == 1

	assert info['arch_string_raw'] == 'amd64'

	assert info['stepping'] == 7
	assert info['model'] == 42
	assert info['family'] == 6
	assert info['flags'] == [
		'apic',
		'cmov',
		'cx16',
		'cx8',
		'de',
		'fpu',
		'fxsr',
		'htt',
		'lahf',
		'lm',
		'mca',
		'mce',
		'mmx',
		'msr',
		'mtrr',
		'nx',
		'osxsave',
		'pae',
		'pat',
		'pclmulqdq',
		'pge',
		'popcnt',
		'pse',
		'pse36',
		'rdtscp',
		'sep',
		'sse',
		'sse2',
		'sse3',
		'sse4.1',
		'sse4.2',
		'ssse3',
		'syscall',
		'tsc',
		'vme',
		'xsave',
	]
