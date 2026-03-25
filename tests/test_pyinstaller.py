"""
Integration test for PyInstaller compatibility.

This test builds a frozen executable using PyInstaller and verifies
that cpuinfo works correctly when bundled, including the CPUID subprocess.

Uses CPUINFO_TEST_FAKE_CPUID to force and control the subprocess path
on all architectures (including non-x86).

Requires PyInstaller to be installed; skipped otherwise.
"""

import json
import os
import subprocess
import sys

import pytest

pyinstaller = pytest.importorskip("PyInstaller")

FAKE_CPUID_INFO = {
	# These may not end up getting used,
	# as other sources could have provided them.
	"vendor_id_raw": "FakeVendor",
	"brand_raw": "Fake CPU @ 3.00GHz",
	"hz_advertised_friendly": "3.0000 GHz",
	"hz_actual_friendly": "3.0000 GHz",
	"hz_advertised": "3000000000",
	"hz_actual": "3000000000",
	"stepping": 1,
	"model": 42,
	"family": 6,
	# processor_type is the only CPUID-only field.
	"processor_type": 99,
}

FAKE_CPUID_OUTPUT = json.dumps({
	"output": "",
	"stdout": "",
	"stderr": "",
	"info": FAKE_CPUID_INFO,
	"err": "",
	"is_fail": False,
})

PROGRAM = """
import json
import multiprocessing
import sys
multiprocessing.freeze_support()
from cpuinfo import get_cpu_info
info = get_cpu_info()
json.dump(info, sys.stdout)
"""


@pytest.fixture(scope="module")
def frozen_exe(tmp_path_factory):
	"""Build a frozen executable that uses cpuinfo and outputs JSON."""
	tmp_path = tmp_path_factory.mktemp("pyinstaller")
	script = tmp_path / "frozen_cpuinfo.py"
	script.write_text(PROGRAM)

	result = subprocess.run(
		[
			sys.executable,
			"-m",
			"PyInstaller",
			"--onefile",
			"--distpath",
			str(tmp_path / "dist"),
			"--workpath",
			str(tmp_path / "build"),
			"--specpath",
			str(tmp_path),
			str(script),
		],
		capture_output=True,
		text=True,
		timeout=120,
	)
	if result.returncode != 0:
		pytest.fail(f"PyInstaller build failed:\n{result.stdout}\n{result.stderr}")

	exe_name = "frozen_cpuinfo.exe" if sys.platform == "win32" else "frozen_cpuinfo"
	exe_path = tmp_path / "dist" / exe_name
	if not exe_path.exists():
		pytest.fail(f"Expected executable not found at {exe_path}")

	return exe_path


def test_frozen_exe_returns_valid_cpuinfo(frozen_exe):
	"""The frozen executable should return valid cpuinfo JSON."""
	result = subprocess.run(
		[str(frozen_exe)],
		capture_output=True,
		text=True,
		timeout=30,
	)
	assert result.returncode == 0, f"Frozen exe failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
	info = json.loads(result.stdout)
	assert isinstance(info, dict)
	assert "arch" in info
	assert "brand_raw" in info
	assert "count" in info
	assert isinstance(info["count"], int)
	assert info["count"] > 0


def test_frozen_exe_cpuid_subprocess(frozen_exe):
	"""The frozen executable's CPUID subprocess path should work correctly."""
	env = {**os.environ, "CPUINFO_TEST_FAKE_CPUID": FAKE_CPUID_OUTPUT}
	result = subprocess.run(
		[str(frozen_exe)],
		capture_output=True,
		text=True,
		timeout=30,
		env=env,
	)
	assert result.returncode == 0, f"Frozen exe failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
	info = json.loads(result.stdout)
	assert isinstance(info, dict)
	# processor_type is only populated by the CPUID path,
	# so it confirms the fake CPUID subprocess ran and its result was used.
	assert info.get("processor_type") == 99
