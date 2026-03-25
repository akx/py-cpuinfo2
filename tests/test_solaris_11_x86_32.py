import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '32bit'
	cpu_count = 4
	is_windows = False
	arch_string_raw = 'i86pc'
	uname_string_raw = 'x86_32'
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
	ssse3 tscp ahf sse3 sse2 sse fxsr mmx cmov amd_sysc cx8 tsc fpu

'''
		return returncode, output

	@staticmethod
	def kstat_m_cpu_info():
		returncode = 0
		output = r'''
module: cpu_info                        instance: 0
name:   cpu_info0                       class:    misc
	brand                           Intel(r) Core(tm) i7 CPU         870  @ 2.93GHz
	cache_id                        0
	chip_id                         0
	clock_MHz                       2931
	clog_id                         0
	core_id                         0
	cpu_type                        i386
	crtime                          20.105018108
	cstates_count                   519253:519254
	cstates_nsec                    3370827137067:327348735595
	current_clock_Hz                2930505167
	current_cstate                  0
	current_pstate                  0
	family                          6
	fpu_type                        i387 compatible
	implementation                  x86 (chipid 0x0 GenuineIntel 106E5 family 6 model 30 step 5 clock 2933 MHz)
	max_ncpu_per_chip               4
	max_ncpu_per_core               1
	max_pwrcap                      0
	model                           30
	ncore_per_chip                  4
	ncpu_per_chip                   4
	pg_id                           1
	pkg_core_id                     0
	pstates_count                   null
	pstates_nsec                    null
	snaptime                        3678.092364544
	socket_type                     Unknown
	state                           on-line
	state_begin                     1435089171
	stepping                        5
	supported_frequencies_Hz        2930505167
	supported_max_cstates           1
	supported_max_pstates           0
	vendor_id                       GenuineIntel


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

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(r) Core(tm) i7 CPU         870  @ 2.93GHz'
	assert info['hz_advertised_friendly'] == '2.9310 GHz'
	assert info['hz_actual_friendly'] == '2.9305 GHz'
	assert info['hz_advertised'] == (2931000000, 0)
	assert info['hz_actual'] == (2930505167, 0)

	assert info['stepping'] == 5
	assert info['model'] == 30
	assert info['family'] == 6
	assert info['flags'] == [
		'ahf',
		'amd_sysc',
		'cmov',
		'cx8',
		'fpu',
		'fxsr',
		'mmx',
		'sse',
		'sse2',
		'sse3',
		'ssse3',
		'tsc',
		'tscp',
	]


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['vendor_id_raw'] == 'GenuineIntel'
	assert info['brand_raw'] == 'Intel(r) Core(tm) i7 CPU         870  @ 2.93GHz'
	assert info['hz_advertised_friendly'] == '2.9310 GHz'
	assert info['hz_actual_friendly'] == '2.9305 GHz'
	assert info['hz_advertised'] == (2931000000, 0)
	assert info['hz_actual'] == (2930505167, 0)
	assert info['arch'] == 'X86_32'
	assert info['bits'] == 32
	assert info['count'] == 4

	assert info['arch_string_raw'] == 'i86pc'

	assert info['stepping'] == 5
	assert info['model'] == 30
	assert info['family'] == 6
	assert info['flags'] == [
		'ahf',
		'amd_sysc',
		'cmov',
		'cx8',
		'fpu',
		'fxsr',
		'mmx',
		'sse',
		'sse2',
		'sse3',
		'ssse3',
		'tsc',
		'tscp',
	]
