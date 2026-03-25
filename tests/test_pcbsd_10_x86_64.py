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
	def dmesg_a():
		retcode = 0
		output = r'''Copyright (c) 1992-2014 The FreeBSD Project.
Copyright (c) 1979, 1980, 1983, 1986, 1988, 1989, 1991, 1992, 1993, 1994
    The Regents of the University of California. All rights reserved.
FreeBSD is a registered trademark of The FreeBSD Foundation.
FreeBSD 10.0-RELEASE-p17 #0: Tue Sep 16 14:33:46 UTC 2014
    root@amd64-builder.pcbsd.org:/usr/obj/usr/src/sys/GENERIC amd64
FreeBSD clang version 3.3 (tags/RELEASE_33/final 183502) 20130610
CPU: Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz (2993.39-MHz K8-class CPU)
  Origin = "GenuineIntel"  Id = 0x306c3  Family = 0x6  Model = 0x3c  Stepping = 3
  Features=0x78bfbff<FPU,VME,DE,PSE,TSC,MSR,PAE,MCE,CX8,APIC,SEP,MTRR,PGE,MCA,CMOV,PAT,PSE36,CLFLUSH,MMX,FXSR,SSE,SSE2>
  Features2=0x209<SSE3,MON,SSSE3>
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
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 6
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 13


def test_get_cpu_info_from_dmesg():
	info = cpuinfo._get_cpu_info_from_dmesg()

	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz'
	assert info['hz_advertised_friendly'] == '3.1000 GHz'
	assert info['hz_actual_friendly'] == '3.1000 GHz'
	assert info['hz_advertised'] == (3100000000, 0)
	assert info['hz_actual'] == (3100000000, 0)

	assert info['flags'] == [
		'apic',
		'clflush',
		'cmov',
		'cx8',
		'de',
		'fpu',
		'fxsr',
		'lahf',
		'lm',
		'mca',
		'mce',
		'mmx',
		'mon',
		'msr',
		'mtrr',
		'nx',
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
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['brand_raw'] == 'Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz'
	assert info['hz_advertised_friendly'] == '3.1000 GHz'
	assert info['hz_actual_friendly'] == '3.1000 GHz'
	assert info['hz_advertised'] == (3100000000, 0)
	assert info['hz_actual'] == (3100000000, 0)
	assert info['arch'] == 'X86_64'
	assert info['bits'] == 64
	assert info['count'] == 1

	assert info['arch_string_raw'] == 'amd64'

	assert info['flags'] == [
		'apic',
		'clflush',
		'cmov',
		'cx8',
		'de',
		'fpu',
		'fxsr',
		'lahf',
		'lm',
		'mca',
		'mce',
		'mmx',
		'mon',
		'msr',
		'mtrr',
		'nx',
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
	]
