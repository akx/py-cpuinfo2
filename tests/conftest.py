import os
import struct

import pytest

_INTERPRETER_BITS = struct.calcsize("P") * 8


def pytest_configure(config):
	required_bits = os.environ.get("CPUINFO_REQUIRE_BITS")
	if required_bits:
		required_bits = int(required_bits)
		if _INTERPRETER_BITS != required_bits:
			pytest.exit(
				f"CPUINFO_REQUIRE_BITS={required_bits} but interpreter is {_INTERPRETER_BITS}-bit",
				returncode=1,
			)
