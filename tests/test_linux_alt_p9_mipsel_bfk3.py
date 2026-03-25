import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '32bit'
	cpu_count = 2
	is_windows = False
	arch_string_raw = 'mips'
	uname_string_raw = ''
	can_cpuid = False

	@staticmethod
	def has_proc_cpuinfo():
		return True

	@staticmethod
	def has_lscpu():
		return True

	@staticmethod
	def cat_proc_cpuinfo():
		returncode = 0
		output = r'''
system type		: Baikal-T Generic SoC
machine			: Baikal-T1 BFK3 evaluation board
processor		: 0
cpu model		: MIPS P5600 V3.0  FPU V2.0
BogoMIPS		: 1196.85
wait instruction	: yes
microsecond timers	: yes
tlb_entries		: 576
extra interrupt vector	: yes
hardware watchpoint	: yes, count: 4, address/irw mask: [0x0ffc, 0x0ffc, 0x0ffb, 0x0ffb]
isa			: mips1 mips2 mips32r1 mips32r2
ASEs implemented	: vz msa eva xpa
shadow register sets	: 1
kscratch registers	: 3
package			: 0
core			: 0
VCED exceptions		: not available
VCEI exceptions		: not available

processor		: 1
cpu model		: MIPS P5600 V3.0  FPU V2.0
BogoMIPS		: 1202.58
wait instruction	: yes
microsecond timers	: yes
tlb_entries		: 576
extra interrupt vector	: yes
hardware watchpoint	: yes, count: 4, address/irw mask: [0x0ffc, 0x0ffc, 0x0ffb, 0x0ffb]
isa			: mips1 mips2 mips32r1 mips32r2
ASEs implemented	: vz msa eva xpa
shadow register sets	: 1
kscratch registers	: 3
package			: 0
core			: 1
VCED exceptions		: not available
VCEI exceptions		: not available
'''
		return returncode, output

	@staticmethod
	def lscpu():
		returncode = 0
		output = r'''
Architecture:        mips
Byte Order:          Little Endian
CPU(s):              2
On-line CPU(s) list: 0,1
Thread(s) per core:  1
Core(s) per socket:  2
Socket(s):           1
Model:               MIPS P5600 V3.0  FPU V2.0
CPU max MHz:         1200,0000
CPU min MHz:         200,0000
BogoMIPS:            1196.85
Flags:               vz msa eva xpa
'''
		return returncode, output


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_registry()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 0
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 6
	assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) == 1
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 13


def test_get_cpu_info_from_lscpu():
	info = cpuinfo._get_cpu_info_from_lscpu()

	assert info['brand_raw'] == 'MIPS P5600 V3.0  FPU V2.0'
	assert info['hz_advertised_friendly'] == '1.2000 GHz'
	assert info['hz_actual_friendly'] == '1.2000 GHz'
	assert info['hz_advertised'] == (1200000000, 0)
	assert info['hz_actual'] == (1200000000, 0)
	assert info['flags'] == ['eva', 'msa', 'vz', 'xpa']


def test_get_cpu_info_from_proc_cpuinfo():
	info = cpuinfo._get_cpu_info_from_proc_cpuinfo()

	assert info['flags'] == ['eva', 'msa', 'vz', 'xpa']


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['brand_raw'] == 'MIPS P5600 V3.0  FPU V2.0'
	assert info['arch'] == 'MIPS_32'
	assert info['bits'] == 32
	assert info['count'] == 2
	assert info['arch_string_raw'] == 'mips'
	assert info['flags'] == ['eva', 'msa', 'vz', 'xpa']
