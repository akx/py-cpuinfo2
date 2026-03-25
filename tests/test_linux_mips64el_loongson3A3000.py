import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 4
	is_windows = False
	arch_string_raw = 'mips64'
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
system type             : generic-loongson-machine
machine                 : Unknown
processor               : 0
cpu model               : ICT Loongson-3 V0.13  FPU V0.1
model name              : ICT Loongson-3A R3 (Loongson-3A3000) @ 1449MHz
BogoMIPS                : 2887.52
wait instruction        : yes
microsecond timers      : yes
tlb_entries             : 1088
extra interrupt vector  : no
hardware watchpoint     : yes, count: 0, address/irw mask: []
isa                     : mips1 mips2 mips3 mips4 mips5 mips32r1 mips32r2 mips64r1 mips64r2
ASEs implemented        : vz
shadow register sets    : 1
kscratch registers      : 6
package                 : 0
core                    : 0
VCED exceptions         : not available
VCEI exceptions         : not available

processor               : 1
cpu model               : ICT Loongson-3 V0.13  FPU V0.1
model name              : ICT Loongson-3A R3 (Loongson-3A3000) @ 1449MHz
BogoMIPS                : 2902.61
wait instruction        : yes
microsecond timers      : yes
tlb_entries             : 1088
extra interrupt vector  : no
hardware watchpoint     : yes, count: 0, address/irw mask: []
isa                     : mips1 mips2 mips3 mips4 mips5 mips32r1 mips32r2 mips64r1 mips64r2
ASEs implemented        : vz
shadow register sets    : 1
kscratch registers      : 6
package                 : 0
core                    : 1
VCED exceptions         : not available
VCEI exceptions         : not available

processor               : 2
cpu model               : ICT Loongson-3 V0.13  FPU V0.1
model name              : ICT Loongson-3A R3 (Loongson-3A3000) @ 1449MHz
BogoMIPS                : 2902.61
wait instruction        : yes
microsecond timers      : yes
tlb_entries             : 1088
extra interrupt vector  : no
hardware watchpoint     : yes, count: 0, address/irw mask: []
isa                     : mips1 mips2 mips3 mips4 mips5 mips32r1 mips32r2 mips64r1 mips64r2
ASEs implemented        : vz
shadow register sets    : 1
kscratch registers      : 6
package                 : 0
core                    : 2
VCED exceptions         : not available
VCEI exceptions         : not available

processor               : 3
cpu model               : ICT Loongson-3 V0.13  FPU V0.1
model name              : ICT Loongson-3A R3 (Loongson-3A3000) @ 1449MHz
BogoMIPS                : 2887.52
wait instruction        : yes
microsecond timers      : yes
tlb_entries             : 1088
extra interrupt vector  : no
hardware watchpoint     : yes, count: 0, address/irw mask: []
isa                     : mips1 mips2 mips3 mips4 mips5 mips32r1 mips32r2 mips64r1 mips64r2
ASEs implemented        : vz
shadow register sets    : 1
kscratch registers      : 6
package                 : 0
core                    : 3
VCED exceptions         : not available
VCEI exceptions         : not available
'''
		return returncode, output

	@staticmethod
	def lscpu():
		returncode = 0
		output = r'''
Architecture:          mips64
Byte Order:            Little Endian
CPU(s):                4
On-line CPU(s) list:   0-3
Thread(s) per core:    1
Core(s) per socket:    4
Socket(s):             1
NUMA node(s):          1
Model name:            ICT Loongson-3A R3 (Loongson-3A3000) @ 1449MHz
BogoMIPS:              2887.52
L1d cache:             64K
L1i cache:             64K
L2 cache:              256K
L3 cache:              2048K
NUMA node0 CPU(s):     0-3
'''
		return returncode, output


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_registry()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 0
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 5
	assert len(cpuinfo._get_cpu_info_from_proc_cpuinfo()) == 6
	assert len(cpuinfo._get_cpu_info_from_sysctl()) == 0
	assert len(cpuinfo._get_cpu_info_from_kstat()) == 0
	assert len(cpuinfo._get_cpu_info_from_dmesg()) == 0
	assert len(cpuinfo._get_cpu_info_from_cat_var_run_dmesg_boot()) == 0
	assert len(cpuinfo._get_cpu_info_from_ibm_pa_features()) == 0
	assert len(cpuinfo._get_cpu_info_from_sysinfo()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpuid()) == 0
	assert len(cpuinfo._get_cpu_info_internal()) == 17


def test_get_cpu_info_from_lscpu():
	info = cpuinfo._get_cpu_info_from_lscpu()

	assert info['brand_raw'] == 'ICT Loongson-3A R3 (Loongson-3A3000) @ 1449MHz'
	assert info['l1_data_cache_size'] == 65536
	assert info['l1_instruction_cache_size'] == 65536
	assert info['l2_cache_size'] == 262144
	assert info['l3_cache_size'] == 2097152


def test_get_cpu_info_from_proc_cpuinfo():
	info = cpuinfo._get_cpu_info_from_proc_cpuinfo()

	assert info['brand_raw'] == 'ICT Loongson-3A R3 (Loongson-3A3000) @ 1449MHz'
	assert info['hz_advertised_friendly'] == '1.4490 GHz'
	assert info['hz_actual_friendly'] == '1.4490 GHz'
	assert info['hz_advertised'] == (1449000000, 0)
	assert info['hz_actual'] == (1449000000, 0)
	assert info['flags'] == ['vz']


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['brand_raw'] == 'ICT Loongson-3A R3 (Loongson-3A3000) @ 1449MHz'
	assert info['arch'] == 'MIPS_64'
	assert info['bits'] == 64
	assert info['count'] == 4
	assert info['arch_string_raw'] == 'mips64'
	assert info['flags'] == ['vz']
