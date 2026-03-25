import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 4
	is_windows = False
	arch_string_raw = 'aarch64'
	uname_string_raw = 'x86_64'
	can_cpuid = False

	@staticmethod
	def has_proc_cpuinfo():
		return True

	@staticmethod
	def has_lscpu():
		return True

	@staticmethod
	def has_cpufreq_info():
		return True

	@staticmethod
	def cat_proc_cpuinfo():
		returncode = 0
		output = r'''
processor	: 0
BogoMIPS	: 2.00
Features	: fp asimd crc32
CPU implementer	: 0x41
CPU architecture: 8
CPU variant	: 0x0
CPU part	: 0xd03
CPU revision	: 4

processor	: 1
BogoMIPS	: 2.00
Features	: fp asimd crc32
CPU implementer	: 0x41
CPU architecture: 8
CPU variant	: 0x0
CPU part	: 0xd03
CPU revision	: 4

processor	: 2
BogoMIPS	: 2.00
Features	: fp asimd crc32
CPU implementer	: 0x41
CPU architecture: 8
CPU variant	: 0x0
CPU part	: 0xd03
CPU revision	: 4

processor	: 3
BogoMIPS	: 2.00
Features	: fp asimd crc32
CPU implementer	: 0x41
CPU architecture: 8
CPU variant	: 0x0
CPU part	: 0xd03
CPU revision	: 4

Hardware	: ODROID-C2
Revision	: 020c


'''
		return returncode, output

	@staticmethod
	def lscpu():
		returncode = 0
		output = r'''
Architecture:          aarch64
Byte Order:            Little Endian
CPU(s):                4
On-line CPU(s) list:   0-3
Thread(s) per core:    1
Core(s) per socket:    1
Socket(s):             4
CPU max MHz:           1536.0000
CPU min MHz:           100.0000
'''
		return returncode, output

	@staticmethod
	def cpufreq_info():
		returncode = 0
		output = r'''
cpufrequtils 008: cpufreq-info (C) Dominik Brodowski 2004-2009
Report errors and bugs to cpufreq@vger.kernel.org, please.
analyzing CPU 0:
  driver: meson_cpufreq
  CPUs which run at the same hardware frequency: 0 1 2 3
  CPUs which need to have their frequency coordinated by software: 0 1 2 3
  maximum transition latency: 200 us.
  hardware limits: 100.0 MHz - 1.54 GHz
  available frequency steps: 100.0 MHz, 250 MHz, 500 MHz, 1000 MHz, 1.30 GHz, 1.54 GHz
  available cpufreq governors: hotplug, interactive, conservative, ondemand, userspace, powersave, performance
  current policy: frequency should be within 100.0 MHz and 1.54 GHz.
                  The governor "interactive" may decide which speed to use
                  within this range.
  current CPU frequency is 1.54 GHz.
  cpufreq stats: 100.0 MHz:0.00%, 250 MHz:0.00%, 500 MHz:0.00%, 1000 MHz:0.00%, 1.30 GHz:0.00%, 1.54 GHz:100.00%  (439)
analyzing CPU 1:
  driver: meson_cpufreq
  CPUs which run at the same hardware frequency: 0 1 2 3
  CPUs which need to have their frequency coordinated by software: 0 1 2 3
  maximum transition latency: 200 us.
  hardware limits: 100.0 MHz - 1.54 GHz
  available frequency steps: 100.0 MHz, 250 MHz, 500 MHz, 1000 MHz, 1.30 GHz, 1.54 GHz
  available cpufreq governors: hotplug, interactive, conservative, ondemand, userspace, powersave, performance
  current policy: frequency should be within 100.0 MHz and 1.54 GHz.
                  The governor "interactive" may decide which speed to use
                  within this range.
  current CPU frequency is 1.54 GHz.
  cpufreq stats: 100.0 MHz:0.00%, 250 MHz:0.00%, 500 MHz:0.00%, 1000 MHz:0.00%, 1.30 GHz:0.00%, 1.54 GHz:100.00%  (439)
analyzing CPU 2:
  driver: meson_cpufreq
  CPUs which run at the same hardware frequency: 0 1 2 3
  CPUs which need to have their frequency coordinated by software: 0 1 2 3
  maximum transition latency: 200 us.
  hardware limits: 100.0 MHz - 1.54 GHz
  available frequency steps: 100.0 MHz, 250 MHz, 500 MHz, 1000 MHz, 1.30 GHz, 1.54 GHz
  available cpufreq governors: hotplug, interactive, conservative, ondemand, userspace, powersave, performance
  current policy: frequency should be within 100.0 MHz and 1.54 GHz.
                  The governor "interactive" may decide which speed to use
                  within this range.
  current CPU frequency is 1.54 GHz.
  cpufreq stats: 100.0 MHz:0.00%, 250 MHz:0.00%, 500 MHz:0.00%, 1000 MHz:0.00%, 1.30 GHz:0.00%, 1.54 GHz:100.00%  (439)
analyzing CPU 3:
  driver: meson_cpufreq
  CPUs which run at the same hardware frequency: 0 1 2 3
  CPUs which need to have their frequency coordinated by software: 0 1 2 3
  maximum transition latency: 200 us.
  hardware limits: 100.0 MHz - 1.54 GHz
  available frequency steps: 100.0 MHz, 250 MHz, 500 MHz, 1000 MHz, 1.30 GHz, 1.54 GHz
  available cpufreq governors: hotplug, interactive, conservative, ondemand, userspace, powersave, performance
  current policy: frequency should be within 100.0 MHz and 1.54 GHz.
                  The governor "interactive" may decide which speed to use
                  within this range.
  current CPU frequency is 1.54 GHz.
  cpufreq stats: 100.0 MHz:0.00%, 250 MHz:0.00%, 500 MHz:0.00%, 1000 MHz:0.00%, 1.30 GHz:0.00%, 1.54 GHz:100.00%  (439)

'''
		return returncode, output


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_registry()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 4
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 4
	assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) == 2
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 13


def test_get_cpu_info_from_cpufreq_info():
	info = cpuinfo._get_cpu_info_from_cpufreq_info()

	assert info['hz_advertised_friendly'] == '1.5400 GHz'
	assert info['hz_actual_friendly'] == '1.5400 GHz'
	assert info['hz_advertised'] == (1540000000, 0)
	assert info['hz_actual'] == (1540000000, 0)


def test_get_cpu_info_from_lscpu():
	info = cpuinfo._get_cpu_info_from_lscpu()

	assert info['hz_advertised_friendly'] == '1.5360 GHz'
	assert info['hz_actual_friendly'] == '1.5360 GHz'
	assert info['hz_advertised'] == (1536000000, 0)
	assert info['hz_actual'] == (1536000000, 0)


def test_get_cpu_info_from_proc_cpuinfo():
	info = cpuinfo._get_cpu_info_from_proc_cpuinfo()

	assert info['hardware_raw'] == 'ODROID-C2'

	assert info['flags'] == ['asimd', 'crc32', 'fp']


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['hardware_raw'] == 'ODROID-C2'
	assert info['hz_advertised_friendly'] == '1.5400 GHz'
	assert info['hz_actual_friendly'] == '1.5400 GHz'
	assert info['hz_advertised'] == (1540000000, 0)
	assert info['hz_actual'] == (1540000000, 0)
	assert info['arch'] == 'ARM_8'
	assert info['bits'] == 64
	assert info['count'] == 4

	assert info['arch_string_raw'] == 'aarch64'

	assert info['flags'] == ['asimd', 'crc32', 'fp']
