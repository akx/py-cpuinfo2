import pytest

from cpuinfo import cpuinfo
from tests import helpers


class MockDataSource:
	bits = '64bit'
	cpu_count = 4
	is_windows = False
	arch_string_raw = 'loongarch64'
	uname_string_raw = 'loongarch64'
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
system type		: generic-loongson-machine

processor		: 0
package			: 0
core			: 0
CPU Family		: Loongson-64bit
Model Name		: Loongson-3A5000
CPU Revision		: 0x10
FPU Revision		: 0x00
CPU MHz			: 2500.00
BogoMIPS		: 5000.00
TLB Entries		: 2112
Address Sizes		: 48 bits physical, 48 bits virtual
ISA			: loongarch32 loongarch64
Features		: cpucfg lam ual fpu complex crypto lvz
Hardware Watchpoint	: yes, iwatch count: 0, dwatch count: 0

processor		: 1
package			: 0
core			: 1
CPU Family		: Loongson-64bit
Model Name		: Loongson-3A5000
CPU Revision		: 0x10
FPU Revision		: 0x00
CPU MHz			: 2500.00
BogoMIPS		: 5000.00
TLB Entries		: 2112
Address Sizes		: 48 bits physical, 48 bits virtual
ISA			: loongarch32 loongarch64
Features		: cpucfg lam ual fpu complex crypto lvz
Hardware Watchpoint	: yes, iwatch count: 0, dwatch count: 0

processor		: 2
package			: 0
core			: 2
CPU Family		: Loongson-64bit
Model Name		: Loongson-3A5000
CPU Revision		: 0x10
FPU Revision		: 0x00
CPU MHz			: 2500.00
BogoMIPS		: 5000.00
TLB Entries		: 2112
Address Sizes		: 48 bits physical, 48 bits virtual
ISA			: loongarch32 loongarch64
Features		: cpucfg lam ual fpu complex crypto lvz
Hardware Watchpoint	: yes, iwatch count: 0, dwatch count: 0

processor		: 3
package			: 0
core			: 3
CPU Family		: Loongson-64bit
Model Name		: Loongson-3A5000
CPU Revision		: 0x10
FPU Revision		: 0x00
CPU MHz			: 2500.00
BogoMIPS		: 5000.00
TLB Entries		: 2112
Address Sizes		: 48 bits physical, 48 bits virtual
ISA			: loongarch32 loongarch64
Features		: cpucfg lam ual fpu complex crypto lvz
Hardware Watchpoint	: yes, iwatch count: 0, dwatch count: 0

'''
		return returncode, output

	@staticmethod
	def lscpu():
		returncode = 0
		output = r'''
Architecture:        loongarch64
Byte Order:          Little Endian
CPU(s):              4
On-line CPU(s) list: 0-3
Model name:          -
Thread(s) per core:  1
Core(s) per socket:  4
Socket(s):           1
BogoMIPS:            5000.00
Flags:               cpucfg lam ual fpu complex crypto lvz
L1d cache:           256 KiB (4 instances)
L1i cache:           256 KiB (4 instances)
L2 cache:            1 MiB (4 instances)
L3 cache:            16 MiB (1 instance)
NUMA node(s):        1
NUMA node0 CPU(s):   0-3
'''
		return returncode, output


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
	helpers.monkey_patch_data_source(cpuinfo, MockDataSource, monkeypatch)


def test_returns():
	assert len(cpuinfo._get_cpu_info_from_registry()) == 0
	assert len(cpuinfo._get_cpu_info_from_cpufreq_info()) == 0
	assert len(cpuinfo._get_cpu_info_from_lscpu()) == 6
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

	assert info['brand_raw'] == '-'
	assert info['l1_data_cache_size'] == 262144
	assert info['l1_instruction_cache_size'] == 262144
	assert info['l2_cache_size'] == 1048576
	assert info['l3_cache_size'] == 16777216
	assert info['flags'] == ['complex', 'cpucfg', 'crypto', 'fpu', 'lam', 'lvz', 'ual']


def test_get_cpu_info_from_proc_cpuinfo():
	info = cpuinfo._get_cpu_info_from_proc_cpuinfo()

	assert info['brand_raw'] == 'Loongson-3A5000'
	assert info['hz_advertised_friendly'] == '2.5000 GHz'
	assert info['hz_actual_friendly'] == '2.5000 GHz'
	assert info['hz_advertised'] == (2500000000, 0)
	assert info['hz_actual'] == (2500000000, 0)
	assert info['flags'] == ['complex', 'cpucfg', 'crypto', 'fpu', 'lam', 'lvz', 'ual']


def test_all():
	info = cpuinfo._get_cpu_info_internal()

	assert info['brand_raw'] == 'Loongson-3A5000'
	assert info['arch'] == 'LOONG_64'
	assert info['bits'] == 64
	assert info['count'] == 4
	assert info['arch_string_raw'] == 'loongarch64'
	assert info['flags'] == ['complex', 'cpucfg', 'crypto', 'fpu', 'lam', 'lvz', 'ual']
