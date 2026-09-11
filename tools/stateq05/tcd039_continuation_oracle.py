#!/usr/bin/env python3
"""Source-shaped B1 oracle for ANIMO revision-53 TCD-039.

This module is deliberately narrow.  It mirrors only the continuation algebra
needed to test whether cumulative potential crop uptake is persistent state.
It is not a replacement implementation of the ANIMO crop model and is not B2.
"""

MIUP = 0.90


def demand_deficit(potential: float, actual: float) -> float:
    return potential - actual


def advance_from_layers(prior: float, flev: list[float], coma: float, st: float) -> float:
    result = prior
    for fraction in flev:
        result = result + fraction * coma * st
    return result


def apply_n_shortage(n_actual: float, n_potential: float, p_potential: float | None = None, miup: float = MIUP):
    out_n = n_potential
    out_p = p_potential
    if n_actual < miup * n_potential:
        damage = miup * n_potential - n_actual
        if out_p is not None:
            out_p = out_p - out_p * damage / n_potential
        out_n = out_n - damage
    return out_n, out_p


def apply_p_shortage(p_actual: float, p_potential: float, n_potential: float, miup: float = MIUP):
    out_p = p_potential
    out_n = n_potential
    if p_actual < miup * p_potential:
        damage = miup * p_potential - p_actual
        out_n = out_n - out_n * damage / p_potential
        out_p = out_p - damage
    return out_n, out_p


def restore_working(n_owner: float, p_owner: float | None, ipo: int):
    return {"Amplni_pot": n_owner, "Amplpo_pot": p_owner if ipo == 1 else None}


def source_shaped_step(state: dict[str, float | None], step: dict, ipo: int = 1):
    n = float(state["n_potential"])
    p = None if ipo != 1 else float(state["p_potential"])

    n = n + float(step.get("n_increment", 0.0))
    if ipo == 1:
        p = p + float(step.get("p_increment", 0.0))

    if "n_actual" in step:
        n, p = apply_n_shortage(float(step["n_actual"]), n, p, float(step.get("miup", MIUP)))

    if ipo == 1 and "p_actual" in step:
        n, p = apply_p_shortage(float(step["p_actual"]), float(p), n, float(step.get("miup", MIUP)))

    return {"n_potential": n, "p_potential": p}


def run_sequence(initial: dict[str, float | None], steps: list[dict], ipo: int = 1):
    state = dict(initial)
    for step in steps:
        state = source_shaped_step(state, step, ipo=ipo)
    return state


def split_witness(zero_at_split: bool = False):
    initial = {"n_potential": 0.015625, "p_potential": 0.0078125}
    steps = [
        {"n_increment": 0.001953125, "p_increment": 0.0009765625},
        {"n_increment": 0.0009765625, "p_increment": 0.00048828125, "n_actual": 0.0107421875},
        {"n_increment": 0.001953125, "p_increment": 0.0009765625, "p_actual": 0.0048828125},
        {"n_increment": 0.0009765625, "p_increment": 0.00048828125},
    ]
    continuous = run_sequence(initial, steps, ipo=1)
    checkpoint = run_sequence(initial, steps[:2], ipo=1)
    if zero_at_split:
        checkpoint = {"n_potential": 0.0, "p_potential": 0.0}
    resumed = run_sequence(checkpoint, steps[2:], ipo=1)
    return continuous, resumed
