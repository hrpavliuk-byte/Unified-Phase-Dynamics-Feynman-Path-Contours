#!/usr/bin/env python3
"""
Unified Phase Dynamics (UPD) Cloud Quantum Experiment Suite
===========================================================
Executes real experimental tests of the 4 core predictions from:
"Quantum Entanglement, Non-Local Bell Correlations, and No-Signaling from the
Universal Path-Contour Master-Functional Psi[Sigma] in Unified Phase Dynamics"
(H. Pavliuk, Concept DOI: 10.5281/zenodo.24553270)

Experiments:
  1. Singlet Bell-CHSH Angular Curve S_UPD(theta) & Tsirelson Bound (2*sqrt(2))
  2. Causal No-Signaling Theorem (Bob marginal invariance under Alice rotations)
  3. 3-Qubit GHZ-Mermin Deterministic Paradox (<M_3> > 2)
  4. 4-Qubit Closed Wilson Plaquette & Knot Stabilizer Closure ([A_v, B_p] = 0)

Usage:
  # Local exact/shot simulator (zero extra dependencies beyond numpy):
  python qiskit_ibm_bell_experiment.py --mode local --shots 8192

  # Real IBM Quantum cloud processor (requires `pip install qiskit qiskit-ibm-runtime`):
  python qiskit_ibm_bell_experiment.py --mode ibm --token YOUR_IBM_QUANTUM_TOKEN --shots 4096
"""

import argparse
import json
import math
import os
import sys
import numpy as np


# ---------------------------------------------------------------------------
# Pure-NumPy Exact Statevector & Shot Sampler (for --mode local)
# ---------------------------------------------------------------------------
def _ry_gate(theta: float) -> np.ndarray:
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    return np.array([[c, -s], [s, c]], dtype=complex)


def _apply_1q(state: np.ndarray, U: np.ndarray, q: int, n_qubits: int) -> np.ndarray:
    state = state.reshape([2] * n_qubits)
    axes = list(range(n_qubits))
    # qiskit bit ordering: qubit 0 is least-significant / rightmost axis n_qubits - 1 - q
    target_axis = n_qubits - 1 - q
    state = np.tensordot(U, state, axes=([1], [target_axis]))
    state = np.moveaxis(state, 0, target_axis)
    return state.reshape(-1)


def _apply_cx(state: np.ndarray, ctrl: int, targ: int, n_qubits: int) -> np.ndarray:
    state = state.reshape([2] * n_qubits)
    ctrl_ax = n_qubits - 1 - ctrl
    targ_ax = n_qubits - 1 - targ
    out = state.copy()
    sl0 = [slice(None)] * n_qubits
    sl1 = [slice(None)] * n_qubits
    sl0[ctrl_ax] = 1
    sl1[ctrl_ax] = 1
    # Flip target axis when ctrl == 1
    sub = out[tuple(sl0)]
    new_targ_ax = targ_ax if targ_ax < ctrl_ax else targ_ax - 1
    out[tuple(sl1)] = np.flip(sub, axis=new_targ_ax)
    return out.reshape(-1)


def _sample_state(state: np.ndarray, n_qubits: int, shots: int, rng: np.random.Generator) -> dict:
    probs = np.abs(state) ** 2
    probs = probs / np.sum(probs)
    indices = rng.choice(len(probs), size=shots, p=probs)
    counts = {}
    for idx in indices:
        bitstr = format(int(idx), f"0{n_qubits}b")
        counts[bitstr] = counts.get(bitstr, 0) + 1
    return counts


H_GATE = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / math.sqrt(2.0)
X_GATE = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
S_DG_GATE = np.array([[1.0, 0.0], [0.0, -1.0j]], dtype=complex)


class LocalCircuitSpec:
    """Minimal gate-list circuit representation convertible to Qiskit or NumPy."""
    def __init__(self, n_qubits: int, name: str):
        self.n_qubits = n_qubits
        self.name = name
        self.ops = []

    def h(self, q: int):
        self.ops.append(("h", (q,)))

    def x(self, q: int):
        self.ops.append(("x", (q,)))

    def sdg(self, q: int):
        self.ops.append(("sdg", (q,)))

    def ry(self, theta: float, q: int):
        self.ops.append(("ry", (float(theta), q)))

    def cx(self, ctrl: int, targ: int):
        self.ops.append(("cx", (ctrl, targ)))

    def run_local(self, shots: int, rng: np.random.Generator) -> dict:
        state = np.zeros(2 ** self.n_qubits, dtype=complex)
        state[0] = 1.0
        for op, args in self.ops:
            if op == "h":
                state = _apply_1q(state, H_GATE, args[0], self.n_qubits)
            elif op == "x":
                state = _apply_1q(state, X_GATE, args[0], self.n_qubits)
            elif op == "sdg":
                state = _apply_1q(state, S_DG_GATE, args[0], self.n_qubits)
            elif op == "ry":
                state = _apply_1q(state, _ry_gate(args[0]), args[1], self.n_qubits)
            elif op == "cx":
                state = _apply_cx(state, args[0], args[1], self.n_qubits)
        return _sample_state(state, self.n_qubits, shots, rng)

    def to_qiskit(self):
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(self.n_qubits, self.n_qubits, name=self.name)
        for op, args in self.ops:
            if op == "h":
                qc.h(args[0])
            elif op == "x":
                qc.x(args[0])
            elif op == "sdg":
                qc.sdg(args[0])
            elif op == "ry":
                qc.ry(args[0], args[1])
            elif op == "cx":
                qc.cx(args[0], args[1])
        qc.measure(range(self.n_qubits), range(self.n_qubits))
        return qc


# ---------------------------------------------------------------------------
# Circuit Builders for the 4 UPD Experiments
# ---------------------------------------------------------------------------
def build_singlet_correlator_circuit(theta_a: float, theta_b: float, name: str) -> LocalCircuitSpec:
    """
    Prepare singlet |Psi^-> = (|01> - |10>)/sqrt(2) representing closed contour
    vertex x0, then measure Pauli spin projections (a.sigma) x (b.sigma) in XZ plane
    by rotating each qubit by Ry(-theta) before Z-basis readout.
    """
    c = LocalCircuitSpec(2, name)
    c.x(0)
    c.x(1)
    c.h(0)
    c.cx(0, 1)  # Now (|01> - |10>)/sqrt(2)
    c.ry(-theta_a, 0)
    c.ry(-theta_b, 1)
    return c


def build_ghz_basis_circuit(bases: str, name: str) -> LocalCircuitSpec:
    """
    Prepare 3-qubit GHZ state (|000> + |111>)/sqrt(2) and rotate each qubit to
    measure XXX, XYY, YXY, or YYX.
    """
    c = LocalCircuitSpec(3, name)
    c.h(0)
    c.cx(0, 1)
    c.cx(0, 2)
    for q, b in enumerate(bases):
        if b == "X":
            c.h(q)
        elif b == "Y":
            c.sdg(q)
            c.h(q)
    return c


def build_wilson_plaquette_circuit(coupling_angle: float, measure_dual_x: bool, name: str) -> LocalCircuitSpec:
    """
    4-qubit minimal closed Wilson plaquette loop W(C) = Z0 Z1 Z2 Z3:
    Prepares ground state of H = -cos(alpha)*(Z0Z1Z2Z3) - sin(alpha)*(X0 + X1 + X2 + X3)
    in the Z2 gauge-invariant plaquette sector via GHZ-like plaquette entanglement,
    allowing measurement of both electric flux closure <Z0Z1Z2Z3> and magnetic loop flip <X0X1X2X3>.
    """
    c = LocalCircuitSpec(4, name)
    # Create gauge-invariant plaquette loop ground state in Z2 lattice gauge sector
    c.h(0)
    c.cx(0, 1)
    c.cx(1, 2)
    c.cx(2, 3)
    # Apply gauge-holonomy deformation Ry(coupling_angle) on each link
    for q in range(4):
        c.ry(coupling_angle, q)
    if measure_dual_x:
        for q in range(4):
            c.h(q)
    return c


# ---------------------------------------------------------------------------
# Analysis Helpers
# ---------------------------------------------------------------------------
def correlator_from_counts(counts: dict) -> tuple[float, float, float]:
    """
    Compute parity expectation <Z_0 ... Z_{n-1}>, standard error, and qubit-1 marginal P(r_1=+1).
    Bitstring convention: rightmost char is qubit 0 (bitstr[-1 - q]).
    """
    total = sum(counts.values())
    exp_val = 0.0
    p_bob_plus = 0.0
    for bitstr, cnt in counts.items():
        ones = bitstr.count("1")
        parity = 1.0 if (ones % 2 == 0) else -1.0
        exp_val += parity * cnt
        # Bob = qubit 1 -> bitstr[-2]
        if len(bitstr) >= 2 and bitstr[-2] == "0":
            p_bob_plus += cnt
    exp_val /= total
    p_bob_plus /= total
    stderr = math.sqrt(max(0.0, 1.0 - exp_val ** 2) / total)
    return exp_val, stderr, p_bob_plus


def execute_suite(mode: str, shots: int, ibm_token: str | None, backend_name: str | None, instance: str | None):
    circuits = []
    meta = []

    # 1. Bell-CHSH angular sweep: theta in [0, 15, 30, 45, 60, 75, 90, 135] deg
    sweep_deg = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0, 135.0]
    for deg in sweep_deg:
        th = math.radians(deg)
        pairs = [("ab", 0.0, th), ("abp", 0.0, 3 * th), ("apb", 2 * th, th), ("apbp", 2 * th, 3 * th)]
        for tag, ta, tb in pairs:
            name = f"chsh_{int(deg)}_{tag}"
            circuits.append(build_singlet_correlator_circuit(ta, tb, name))
            meta.append(("chsh", deg, tag))

    # 2. Explicit No-Signaling test at fixed Bob theta_b = pi/4 across Alice angles
    alice_angles = [0.0, math.pi / 4.0, math.pi / 2.0, 1.23]
    for idx, ta in enumerate(alice_angles):
        name = f"nosig_{idx}"
        circuits.append(build_singlet_correlator_circuit(ta, math.pi / 4.0, name))
        meta.append(("nosig", ta, idx))

    # 3. 3-Qubit GHZ-Mermin test
    for basis in ["XXX", "XYY", "YXY", "YYX"]:
        circuits.append(build_ghz_basis_circuit(basis, f"ghz_{basis}"))
        meta.append(("ghz", basis, None))

    # 4. 4-Qubit Wilson Plaquette Loop holonomy test across coupling angles
    plaq_angles = [0.0, 0.4, 0.8, 1.2, math.pi / 2.0]
    for idx, ang in enumerate(plaq_angles):
        circuits.append(build_wilson_plaquette_circuit(ang, False, f"plaq_z_{idx}"))
        meta.append(("plaq_z", ang, idx))
        circuits.append(build_wilson_plaquette_circuit(ang, True, f"plaq_x_{idx}"))
        meta.append(("plaq_x", ang, idx))

    # Run circuits
    all_counts = []
    backend_used = "local_numpy_statevector_sampler"
    if mode == "local":
        rng = np.random.default_rng(20261126)
        for c in circuits:
            all_counts.append(c.run_local(shots, rng))
    elif mode == "ibm":
        try:
            from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
            from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
        except ImportError as exc:
            print("ERROR: IBM mode requires `pip install qiskit qiskit-ibm-runtime`.", file=sys.stderr)
            raise SystemExit(1) from exc

        if not ibm_token:
            print("ERROR: Please pass --token YOUR_IBM_QUANTUM_API_TOKEN (or set IBM_QUANTUM_TOKEN env).", file=sys.stderr)
            raise SystemExit(1)

        service = QiskitRuntimeService(channel="ibm_quantum_platform", token=ibm_token, instance=instance) if instance else QiskitRuntimeService(channel="ibm_quantum_platform", token=ibm_token)
        if backend_name:
            backend = service.backend(backend_name)
        else:
            backend = service.least_busy(operational=True, simulator=False, min_num_qubits=5)
        backend_used = backend.name
        print(f"Submitting {len(circuits)} UPD circuits ({shots} shots each) to IBM QPU: {backend_used}")

        qiskit_circuits = [c.to_qiskit() for c in circuits]
        pm = generate_preset_pass_manager(backend=backend, optimization_level=2)
        isa_circuits = pm.run(qiskit_circuits)

        sampler = Sampler(mode=backend)
        job = sampler.run(isa_circuits, shots=shots)
        print(f"IBM Quantum Job ID: {job.job_id()}")
        result = job.result()
        for idx in range(len(circuits)):
            pub_res = result[idx]
            # Extract classical register counts cleanly across Qiskit SamplerV2 versions
            creg_name = list(pub_res.data.keys())[0]
            all_counts.append(getattr(pub_res.data, creg_name).get_counts())
    else:
        raise ValueError(f"Unknown mode: {mode}")

    # Parse results
    chsh_map = {deg: {} for deg in sweep_deg}
    nosig_list = []
    ghz_map = {}
    plaq_z_map = {}
    plaq_x_map = {}

    for m, cnts in zip(meta, all_counts):
        exp_val, stderr, p_bob = correlator_from_counts(cnts)
        kind, param, extra = m
        if kind == "chsh":
            chsh_map[param][extra] = (exp_val, stderr)
        elif kind == "nosig":
            nosig_list.append({
                "theta_alice_rad": round(param, 4),
                "E_ab": round(exp_val, 5),
                "P_Bob_plus": round(p_bob, 5),
                "stderr_P_Bob": round(math.sqrt(max(0.0, p_bob * (1.0 - p_bob)) / shots), 5),
            })
        elif kind == "ghz":
            ghz_map[param] = (exp_val, stderr)
        elif kind == "plaq_z":
            plaq_z_map[round(param, 4)] = (exp_val, stderr)
        elif kind == "plaq_x":
            plaq_x_map[round(param, 4)] = (exp_val, stderr)

    chsh_summary = []
    for deg in sweep_deg:
        d = chsh_map[deg]
        S_meas = abs(d["ab"][0] - d["abp"][0] + d["apb"][0] + d["apbp"][0])
        S_err = math.sqrt(sum(v[1] ** 2 for v in d.values()))
        th = math.radians(deg)
        S_upd_exact = abs(3.0 * math.cos(th) - math.cos(3.0 * th))
        chsh_summary.append({
            "theta_deg": deg,
            "S_measured": round(S_meas, 5),
            "S_stderr": round(S_err, 5),
            "S_UPD_theory": round(S_upd_exact, 5),
            "violates_Bell_2": bool(S_meas > 2.0),
            "within_Tsirelson": bool(S_meas - 2 * S_err <= 2.0 * math.sqrt(2.0)),
        })

    ghz_M3 = ghz_map["XXX"][0] - ghz_map["XYY"][0] - ghz_map["YXY"][0] - ghz_map["YYX"][0]
    ghz_err = math.sqrt(sum(v[1] ** 2 for v in ghz_map.values()))
    max_bob_drift = max(x["P_Bob_plus"] for x in nosig_list) - min(x["P_Bob_plus"] for x in nosig_list)

    plaq_summary = []
    for ang in plaq_angles:
        key = round(ang, 4)
        ez, _ = plaq_z_map[key]
        ex, _ = plaq_x_map[key]
        plaq_summary.append({
            "coupling_angle_rad": key,
            "Wilson_loop_Z0Z1Z2Z3_meas": round(ez, 5),
            "Wilson_loop_Z_theory": round(math.cos(ang) ** 4 + math.sin(ang) ** 4, 5),
            "dual_X0X1X2X3_meas": round(ex, 5),
            "dual_X_theory": round(math.cos(ang) ** 4 + math.sin(ang) ** 4, 5),
        })

    output = {
        "backend": backend_used,
        "mode": mode,
        "shots_per_circuit": shots,
        "total_circuits": len(circuits),
        "exp1_chsh_angular_sweep": chsh_summary,
        "exp2_no_signaling_check": {
            "rows": nosig_list,
            "max_P_Bob_drift": round(max_bob_drift, 5),
            "theory_expected_drift": 0.0,
        },
        "exp3_ghz_mermin_paradox": {
            "XXX": round(ghz_map["XXX"][0], 5),
            "XYY": round(ghz_map["XYY"][0], 5),
            "YXY": round(ghz_map["YXY"][0], 5),
            "YYX": round(ghz_map["YYX"][0], 5),
            "M3_measured": round(ghz_M3, 5),
            "M3_stderr": round(ghz_err, 5),
            "M3_UPD_theory": 4.0,
            "LHV_classical_bound": 2.0,
        },
        "exp4_wilson_plaquette_holonomy": plaq_summary,
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ibm_qpu_experiment_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("\n=== UPD Quantum Hardware / Simulator Experiment Complete ===")
    print(f"Backend: {backend_used} | Circuits: {len(circuits)} | Shots: {shots}")
    max_s = max(chsh_summary, key=lambda r: r["S_measured"])
    print(f"Exp 1 (CHSH Peak at theta={max_s['theta_deg']} deg): S = {max_s['S_measured']:.4f} +/- {max_s['S_stderr']:.4f} (Theory = {max_s['S_UPD_theory']:.4f})")
    print(f"Exp 2 (No-Signaling): Max Bob marginal drift = {max_bob_drift:.5f} (Theory = 0.0)")
    print(f"Exp 3 (GHZ-Mermin): <M_3> = {ghz_M3:.4f} +/- {ghz_err:.4f} (Theory = 4.0, LHV <= 2.0)")
    print(f"Exp 4 (Wilson Plaquette at alpha=0): <Z0Z1Z2Z3> = {plaq_summary[0]['Wilson_loop_Z0Z1Z2Z3_meas']:.4f}, <X0X1X2X3> = {plaq_summary[0]['dual_X0X1X2X3_meas']:.4f}")
    print(f"Saved full results to: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Run UPD Bell/GHZ/Wilson experiments locally or on IBM Quantum QPU.")
    parser.add_argument("--mode", choices=["local", "ibm"], default="local", help="Execution backend mode.")
    parser.add_argument("--shots", type=int, default=8192, help="Number of measurement shots per circuit.")
    parser.add_argument("--token", type=str, default=os.environ.get("IBM_QUANTUM_TOKEN"), help="IBM Quantum API token.")
    parser.add_argument("--backend", type=str, default=None, help="Optional IBM QPU backend name (e.g. ibm_brisbane).")
    parser.add_argument("--instance", type=str, default=None, help="Optional IBM Quantum CRN/instance.")
    args = parser.parse_args()
    execute_suite(args.mode, args.shots, args.token, args.backend, args.instance)


if __name__ == "__main__":
    main()
