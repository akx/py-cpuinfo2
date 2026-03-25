import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '32bit'
	cpu_count = 8
	is_windows = False
	arch_string_raw = 'i86pc'
	uname_string_raw = 'i386'
	can_cpuid = False

	@staticmethod
	def has_isainfo():
		return True

	@staticmethod
	def has_kstat():
		return True

	@staticmethod
	def isainfo_vb():
		returncode = 0
		output = r'''
64-bit amd64 applications
	rdseed avx2 rdrand avx xsave pclmulqdq aes movbe sse4.2 sse4.1
	ssse3 amd_lzcnt popcnt amd_sse4a tscp ahf cx16 sse3 sse2 sse fxsr
amd_mmx mmx cmov amd_sysc cx8 tsc fpu

'''
		return returncode, output

	@staticmethod
	def kstat_m_cpu_info():
		returncode = 0
		output = r'''
module: cpu_info                        instance: 0
name:   cpu_info0                       class:    misc
	brand                           AMD Ryzen 7 2700X Eight-Core Processor
	cache_id                        0
	chip_id                         0
	clock_MHz                       3693
	clog_id                         0
	core_id                         0
	cpu_type                        i386
	crtime                          22.539390752
	current_clock_Hz                3692643590
	current_cstate                  1
	family                          23
	fpu_type                        i387 compatible
	implementation                  x86 (chipid 0x0 AuthenticAMD 800F82 family 23 model 8 step 2 clock 3693 MHz)
	model                           8
	ncore_per_chip                  8
	ncpu_per_chip                   8
	pg_id                           1
	pkg_core_id                     0
	snaptime                        120.971135132
	socket_type                     Unknown
	state                           on-line
	state_begin                     1553482276
	stepping                        2
	supported_frequencies_Hz        3692643590
	supported_max_cstates           0
	vendor_id                       AuthenticAMD


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
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 10
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 17


def test_get_cpu_info_from_kstat():
	info = cpuinfo._get_cpu_info_from_kstat()

	assert info['vendor_id_raw'] == 'AuthenticAMD'
	assert info['brand_raw'] == 'AMD Ryzen 7 2700X Eight-Core Processor'
	assert info['hz_advertised_friendly'] == '3.6930 GHz'
	assert info['hz_actual_friendly'] == '3.6926 GHz'
	assert info['hz_advertised'] == (3693000000, 0)
	assert info['hz_actual'] == (3692643590, 0)

	assert info['stepping'] == 2
	assert info['model'] == 8
	assert info['family'] == 23
	assert info['flags'] == ['amd_mmx', 'amd_sysc', 'cmov', 'cx8', 'fpu', 'mmx', 'tsc']


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == 'AuthenticAMD'
	assert info['brand_raw'] == 'AMD Ryzen 7 2700X Eight-Core Processor'
	assert info['hz_advertised_friendly'] == '3.6930 GHz'
	assert info['hz_actual_friendly'] == '3.6926 GHz'
	assert info['hz_advertised'] == (3693000000, 0)
	assert info['hz_actual'] == (3692643590, 0)
	assert info['arch'] == 'X86_32'
	assert info['bits'] == 32
	assert info['count'] == 8

	assert info['arch_string_raw'] == 'i86pc'

	assert info['stepping'] == 2
	assert info['model'] == 8
	assert info['family'] == 23
	assert info['flags'] == ['amd_mmx', 'amd_sysc', 'cmov', 'cx8', 'fpu', 'mmx', 'tsc']
