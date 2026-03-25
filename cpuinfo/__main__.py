import argparse
import json
import sys

from cpuinfo.cpuinfo import (
	CPUINFO_VERSION_STRING,
	_configure_trace,
	_get_cpu_info_from_cpuid_actual,
	_get_cpu_info_internal,
)


def print_cpuinfo(info):
	print(f"Python Version: {info.get('python_version', '')}")
	print(f"Cpuinfo Version: {info.get('cpuinfo_version_string', '')}")
	print(f"Vendor ID Raw: {info.get('vendor_id_raw', '')}")
	print(f"Hardware Raw: {info.get('hardware_raw', '')}")
	print(f"Brand Raw: {info.get('brand_raw', '')}")
	print(f"Hz Advertised Friendly: {info.get('hz_advertised_friendly', '')}")
	print(f"Hz Actual Friendly: {info.get('hz_actual_friendly', '')}")
	print(f"Hz Advertised: {info.get('hz_advertised', '')}")
	print(f"Hz Actual: {info.get('hz_actual', '')}")
	print(f"Arch: {info.get('arch', '')}")
	print(f"Bits: {info.get('bits', '')}")
	print(f"Count: {info.get('count', '')}")
	print(f"Arch String Raw: {info.get('arch_string_raw', '')}")
	print(f"L1 Data Cache Size: {info.get('l1_data_cache_size', '')}")
	print(f"L1 Instruction Cache Size: {info.get('l1_instruction_cache_size', '')}")
	print(f"L2 Cache Size: {info.get('l2_cache_size', '')}")
	print(f"L2 Cache Line Size: {info.get('l2_cache_line_size', '')}")
	print(f"L2 Cache Associativity: {info.get('l2_cache_associativity', '')}")
	print(f"L3 Cache Size: {info.get('l3_cache_size', '')}")
	print(f"Stepping: {info.get('stepping', '')}")
	print(f"Model: {info.get('model', '')}")
	print(f"Family: {info.get('family', '')}")
	print(f"Processor Type: {info.get('processor_type', '')}")
	print(f"Flags: {', '.join(info.get('flags', ''))}")


def main():
	parser = argparse.ArgumentParser(description='Gets CPU info with pure Python')
	parser.add_argument('--json', action='store_true', help='Return the info in JSON format')
	parser.add_argument('--version', action='store_true', help='Return the version of py-cpuinfo')
	parser.add_argument('--trace', action='store_true', help='Traces code paths used to find CPU info to file')
	parser.add_argument('--internal-cpuid', action='store_true', help=argparse.SUPPRESS)
	args = parser.parse_args()
	_configure_trace(args.trace)

	# Internal: run CPUID in isolation and return JSON result
	if args.internal_cpuid:
		output = _get_cpu_info_from_cpuid_actual()
		print(json.dumps(output))
		return

	if args.version:
		print(CPUINFO_VERSION_STRING)
		return

	info = _get_cpu_info_internal()

	if not info:
		sys.stderr.write("Failed to find cpu info\n")
		sys.exit(1)

	if args.json:
		print(json.dumps(info))
	else:
		print_cpuinfo(info)


if __name__ == "__main__":
	main()
