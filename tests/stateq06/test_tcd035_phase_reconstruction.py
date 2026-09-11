import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[2] / "tools/stateq06/tcd035_phase_reconstruction_oracle.py"
spec = importlib.util.spec_from_file_location("tcd035_oracle", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_complete_oracle_bank():
    result = mod.validate_cases()
    assert result["cases"] == 72
    assert result["nontrivial_divergence_cases"] > 0
    assert result["equality_controls"] > 0


def test_species_specific_coefficients_are_not_interchangeable():
    ch4 = mod.aqueous_from_total("CH4", 1.0e-4, 0.20, 0.45, 20.0)
    n2o = mod.aqueous_from_total("N2O", 1.0e-4, 0.20, 0.45, 20.0)
    assert ch4 != n2o


def test_zero_total_gas_is_exact_restart_control():
    w = mod.witness("CH4", 0.0, 0.15, 0.45, 25.0, 10.0)
    assert w["continuous"] == 0.0
    assert w["legacy_restart"] == 0.0


def test_saturated_layer_is_temperature_independent_control():
    w = mod.witness("N2O", 1.0e-4, 0.45, 0.45, 25.0, 10.0)
    assert w["legacy_restart"] == w["continuous"]


def test_unsaturated_nonzero_state_detects_reference_temperature_substitution():
    w = mod.witness("CH4", 1.0e-4, 0.20, 0.45, 25.0, 10.0)
    assert w["legacy_restart"] != w["continuous"]
    assert w["qualified_restart"] == w["continuous"]
