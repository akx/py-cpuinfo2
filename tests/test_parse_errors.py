import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 1
	is_windows = True
	arch_string_raw = 'x86_64'
	uname_string_raw = 'x86_64'
	can_cpuid = False

	@staticmethod
	def has_proc_cpuinfo():
		return True

	@staticmethod
	def has_dmesg():
		return True

	@staticmethod
	def has_var_run_dmesg_boot():
		return True

	@staticmethod
	def has_cpufreq_info():
		return True

	@staticmethod
	def has_sestatus():
		return True

	@staticmethod
	def has_sysctl():
		return True

	@staticmethod
	def has_isainfo():
		return True

	@staticmethod
	def has_kstat():
		return True

	@staticmethod
	def has_sysinfo():
		return True

	@staticmethod
	def cat_proc_cpuinfo():
		return 0, ""

	@staticmethod
	def cpufreq_info():
		return 0, ""

	@staticmethod
	def sestatus_b():
		return 0, ""

	@staticmethod
	def dmesg_a():
		return 0, ""

	@staticmethod
	def cat_var_run_dmesg_boot():
		return 0, ""

	@staticmethod
	def sysctl_machdep_cpu_hw_cpufrequency():
		return 0, ""

	@staticmethod
	def isainfo_vb():
		return 0, ""

	@staticmethod
	def kstat_m_cpu_info():
		return 0, ""

	@staticmethod
	def sysinfo_cpu():
		return 0, ""

	@staticmethod
	def winreg_processor_brand():
		return {}

	@staticmethod
	def winreg_vendor_id_raw():
		return {}

	@staticmethod
	def winreg_arch_string_raw():
		return {}

	@staticmethod
	def winreg_hz_actual():
		return {}

	@staticmethod
	def winreg_feature_bits():
		return {}


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
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0


def test_all():
	assert cpuinfo._get_cpu_info_from_registry() == {}
	assert cpuinfo._get_cpu_info_from_proc_cpuinfo() == {}
	assert cpuinfo._get_cpu_info_from_sysctl() == {}
	assert cpuinfo._get_cpu_info_from_kstat() == {}
	assert cpuinfo._get_cpu_info_from_dmesg() == {}
	assert cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot() == {}
	assert cpuinfo._get_cpu_info_from_sysinfo() == {}
