#!/usr/bin/env python3
"""
Numerical Verification of Quantum Entanglement, CHSH/Bell Correlations,
GHZ Paradox, No-Signaling Marginalization, and Gravitational Decoherence Crossover
in Unified Phase Dynamics (UPD) of Feynman Path Contours.

Author: H. Pavliuk (Hryhorii Pavliuk), Independent Researcher
ORCID: 0009-0000-0899-3463
Monograph Concept DOI: 10.5281/zenodo.24226129
"""

import json
import math
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Pauli matrices and SU(2) invariant antisymmetric tensor (Spin(3,1) spatial cover)
I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
SIGMA = [SX, SY, SZ]
EPS = np.array([[0, 1], [-1, 0]], dtype=complex)


def spin_operator(theta: float, phi: float = 0.0) -> np.ndarray:
    """Hermitian spin projection n . sigma along unit vector n(theta, phi)."""
    nx = math.sin(theta) * math.cos(phi)
    ny = math.sin(theta) * math.sin(phi)
    nz = math.cos(theta)
    return nx * SX + ny * SY + nz * SZ


def holonomy_singlet_correlator(theta_a: float, theta_b: float,
                                phi_a: float = 0.0, phi_b: float = 0.0) -> float:
    """
    Exact closed-contour trace evaluation for bipartite spin-1/2 singlet:
    E(a, b) = (1/2) Tr[ eps^dag (a.sigma) eps (b.sigma)^T ]
    where eps is the SU(2) x SU(2) invariant topological vertex tensor.
    """
    A = spin_operator(theta_a, phi_a)
    B = spin_operator(theta_b, phi_b)
    E = 0.5 * np.trace(EPS.conj().T @ A @ EPS @ B.T)
    return float(np.real(E))


def joint_probabilities(theta_a: float, theta_b: float) -> dict:
    """
    Compute joint contour detection probabilities P(r_a, r_b | a, b)
    and verify strict no-signaling trace marginalization.
    """
    A = spin_operator(theta_a)
    B = spin_operator(theta_b)
    psi_singlet = np.array([0.0, 1.0, -1.0, 0.0], dtype=complex) / math.sqrt(2.0)
    rho = np.outer(psi_singlet, psi_singlet.conj())

    probs = {}
    for ra in (+1, -1):
        Pa = 0.5 * (I2 + ra * A)
        for rb in (+1, -1):
            Pb = 0.5 * (I2 + rb * B)
            Pab = np.kron(Pa, Pb)
            probs[(ra, rb)] = float(np.real(np.trace(rho @ Pab)))

    marg_b_plus = probs[(+1, +1)] + probs[(-1, +1)]
    marg_b_minus = probs[(+1, -1)] + probs[(-1, -1)]
    marg_a_plus = probs[(+1, +1)] + probs[(+1, -1)]
    marg_a_minus = probs[(-1, +1)] + probs[(-1, -1)]
    return {
        "P_++": probs[(+1, +1)],
        "P_+-": probs[(+1, -1)],
        "P_-+": probs[(-1, +1)],
        "P_--": probs[(-1, -1)],
        "P_B_+": marg_b_plus,
        "P_B_-": marg_b_minus,
        "P_A_+": marg_a_plus,
        "P_A_-": marg_a_minus,
    }


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Exact CHSH optimum and Tsirelson verification
    # Optimal spin-1/2 planar angles: a=0, a'=pi/2, b=pi/4, b'=3*pi/4
    a, ap = 0.0, math.pi / 2.0
    b, bp = math.pi / 4.0, 3.0 * math.pi / 4.0

    E_ab = holonomy_singlet_correlator(a, b)
    E_abp = holonomy_singlet_correlator(a, bp)
    E_apb = holonomy_singlet_correlator(ap, b)
    E_apbp = holonomy_singlet_correlator(ap, bp)
    S_raw = E_ab - E_abp + E_apb + E_apbp
    # Standard CHSH linear combination S = |E(a,b) - E(a,b')| + |E(a',b) + E(a',b')|
    # With a=0, b=3pi/4, b'=pi/4, a'=pi/2: E(0,3pi/4)=+0.7071, E(0,pi/4)=-0.7071, E(pi/2,3pi/4)=-0.7071, E(pi/2,pi/4)=-0.7071
    # Standard orientation giving S = +2*sqrt(2):
    a1, a2 = 0.0, math.pi / 2.0
    b1, b2 = -math.pi / 4.0, math.pi / 4.0
    S_chsh_opt = abs(
        holonomy_singlet_correlator(a1, b1)
        - holonomy_singlet_correlator(a1, b2)
        + holonomy_singlet_correlator(a2, b1)
        + holonomy_singlet_correlator(a2, b2)
    )
    # Using canonical maximization: a=0, a'=pi/2, b=pi/4, b'=3pi/4 -> |E(a,b) - E(a,b') + E(a',b) + E(a',b')|?
    # Note: E(0,pi/4)=-c, E(0,3pi/4)=+c, E(pi/2,pi/4)=-c, E(pi/2,3pi/4)=-c => (-c)-(+c)+(-c)+(-c) = -4c = -2*sqrt(2)!
    S_abs = abs(S_raw)

    # Verify Bell operator norm ||B|| = 2*sqrt(2) numerically in 4x4 Hilbert space
    A_op = np.kron(spin_operator(a), I2)
    Ap_op = np.kron(spin_operator(ap), I2)
    B_op = np.kron(I2, spin_operator(b))
    Bp_op = np.kron(I2, spin_operator(bp))
    Bell_op = A_op @ B_op - A_op @ Bp_op + Ap_op @ B_op + Ap_op @ Bp_op
    eigvals = np.linalg.eigvalsh(Bell_op)
    max_eig = float(np.max(np.abs(eigvals)))

    # 2. No-signaling check across arbitrary settings
    ns_1 = joint_probabilities(0.0, math.pi / 4.0)
    ns_2 = joint_probabilities(1.23, math.pi / 4.0)
    no_signaling_diff = abs(ns_1["P_B_+"] - ns_2["P_B_+"])

    # 3. 3-qubit GHZ Mermin paradox verification
    ket0 = np.array([1.0, 0.0], dtype=complex)
    ket1 = np.array([0.0, 1.0], dtype=complex)
    psi_ghz = (np.kron(np.kron(ket0, ket0), ket0) + np.kron(np.kron(ket1, ket1), ket1)) / math.sqrt(2.0)

    def kron3(op1, op2, op3):
        return np.kron(np.kron(op1, op2), op3)

    XYY = kron3(SX, SY, SY)
    YXY = kron3(SY, SX, SY)
    YYX = kron3(SY, SY, SX)
    XXX = kron3(SX, SX, SX)
    Mermin_op = XXX - XYY - YXY - YYX

    exp_XYY = float(np.real(psi_ghz.conj().T @ XYY @ psi_ghz))
    exp_YXY = float(np.real(psi_ghz.conj().T @ YXY @ psi_ghz))
    exp_YYX = float(np.real(psi_ghz.conj().T @ YYX @ psi_ghz))
    exp_XXX = float(np.real(psi_ghz.conj().T @ XXX @ psi_ghz))
    exp_Mermin = float(np.real(psi_ghz.conj().T @ Mermin_op @ psi_ghz))

    # 4. Schwinger non-local UV correction to visibility and S_CHSH
    Lambda_UPD = 1200.0  # GeV (electroweak holonomy scale = 1.2 TeV)
    energies_GeV = {
        "optical_photon_2eV": 2.0e-9,
        "microwave_5GHz": 2.068e-14,
        "lhc_13TeV_hadronic": 100.0,
    }
    uv_shifts = {}
    for label, E_val in energies_GeV.items():
        delta_vis = (E_val / Lambda_UPD) ** 4
        uv_shifts[label] = {
            "energy_GeV": E_val,
            "fractional_visibility_shift": delta_vis,
            "delta_S_CHSH": 2.0 * math.sqrt(2.0) * delta_vis,
        }

    # 5. Experimentum Crucis 1 bridge: Gravitational phase decoherence cutoff for Bell violation
    # tau_crit = 10 ms at M_crit = 3.13e12 amu; Gamma ~ M^2 scaling
    M_crit_amu = 3.13e12
    tau_crit_ms = 10.0
    t_bell_cutoff_ms = tau_crit_ms * math.log(math.sqrt(2.0))  # time where 2*sqrt(2)*exp(-t/tau) = 2

    masses_amu = [1.0e11, 1.0e12, 3.13e12, 1.0e13]
    mass_crossover = {}
    for m in masses_amu:
        tau_m = tau_crit_ms * (M_crit_amu / m) ** 2
        t_cut = tau_m * math.log(math.sqrt(2.0))
        mass_crossover[f"{m:.2e}_amu"] = {
            "tau_G_ms": tau_m,
            "t_bell_cutoff_ms": t_cut,
        }

    # Sweep S(theta) for symmetric angle parameterization a=0, a'=2*theta, b=theta, b'=3*theta
    thetas = np.linspace(0.0, math.pi, 361)
    S_theta_upd = np.array([
        abs(
            holonomy_singlet_correlator(0.0, th)
            - holonomy_singlet_correlator(0.0, 3.0 * th)
            + holonomy_singlet_correlator(2.0 * th, th)
            + holonomy_singlet_correlator(2.0 * th, 3.0 * th)
        )
        for th in thetas
    ])
    # Piecewise linear LHV model for comparison: E_LHV(theta) = -1 + 2*theta/pi
    def lhv_E(delta):
        d = abs(delta) % (2.0 * math.pi)
        if d > math.pi:
            d = 2.0 * math.pi - d
        return -1.0 + 2.0 * d / math.pi

    S_theta_lhv = np.array([
        abs(lhv_E(th) - lhv_E(3.0 * th) + lhv_E(th) + lhv_E(th))
        for th in thetas
    ])

    results = {
        "chsh_verification": {
            "S_UPD_max": S_abs,
            "Tsirelson_bound": 2.0 * math.sqrt(2.0),
            "Bell_classical_bound": 2.0,
            "Bell_operator_eigenvalues": [float(v) for v in eigvals],
            "max_operator_norm": max_eig,
            "E_ab": E_ab,
            "E_abp": E_abp,
            "E_apb": E_apb,
            "E_apbp": E_apbp,
        },
        "no_signaling_verification": {
            "setting_1_a0_bpi4": ns_1,
            "setting_2_a1p23_bpi4": ns_2,
            "marginal_difference_Bob": no_signaling_diff,
        },
        "ghz_mermin_paradox": {
            "E_XYY": exp_XYY,
            "E_YXY": exp_YXY,
            "E_YYX": exp_YYX,
            "E_XXX": exp_XXX,
            "Mermin_S3_UPD": exp_Mermin,
            "Mermin_LHV_bound": 2.0,
        },
        "schwinger_uv_shifts": uv_shifts,
        "gravitational_bell_cutoff": {
            "M_crit_amu": M_crit_amu,
            "tau_crit_ms": tau_crit_ms,
            "t_bell_cutoff_ms_at_Mcrit": t_bell_cutoff_ms,
            "mass_scaling": mass_crossover,
        },
    }

    json_path = os.path.join(out_dir, "bell_entanglement_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # ---- FIGURE 1: CHSH Angular Landscape & Loophole-Free Experimental Benchmarks ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.4), dpi=220)

    deg = np.degrees(thetas)
    ax1.plot(deg, S_theta_upd, color="#1d4ed8", lw=2.5,
             label=r"UPD Contour Holonomy $S_{\mathrm{UPD}}(\theta) = |3\cos\theta - \cos 3\theta|$")
    ax1.plot(deg, S_theta_lhv, color="#64748b", lw=2.0, ls="--",
             label=r"Piecewise-Linear Local Hidden Variable $E_{\mathrm{LHV}}(\theta)$")
    ax1.axhline(2.0, color="#dc2626", lw=1.8, ls=":", label=r"Bell–CHSH Classical Bound ($S = 2$)")
    ax1.axhline(2.0 * math.sqrt(2.0), color="#059669", lw=1.8, ls="-.",
                label=rf"Tsirelson Bound ($2\sqrt{{2}} \approx {2*math.sqrt(2):.4f}$)")
    ax1.fill_between(deg, 2.0, S_theta_upd, where=(S_theta_upd > 2.0),
                     color="#3b82f6", alpha=0.16, label="Non-local Violation Zone")
    ax1.scatter([45.0, 135.0], [2.0 * math.sqrt(2.0), 2.0 * math.sqrt(2.0)],
                color="#059669", zorder=5, s=45)
    ax1.annotate(r"Max $2\sqrt{2}$ at $\theta=45^\circ$", xy=(45, 2.8284), xytext=(55, 2.93),
                 arrowprops=dict(arrowstyle="->", color="#059669", lw=1.1), fontsize=8.8, color="#065f46")
    ax1.set_xlim(0, 180)
    ax1.set_ylim(0, 3.25)
    ax1.set_xlabel(r"Relative Analyzer Step Angle $\theta$ (degrees)", fontsize=10.5)
    ax1.set_ylabel(r"CHSH Parameter $|S(\theta)|$", fontsize=10.5)
    ax1.set_title("A. Contour CHSH Violation & Tsirelson Bound", fontsize=11.5, fontweight="bold")
    ax1.grid(True, alpha=0.25)
    ax1.legend(loc="lower center", fontsize=8.0, framealpha=0.93)

    # Panel B: Experimental Loophole-Free & High-Precision Bell Tests
    exps = [
        ("Freedman–Clauser (1972)", 2.72, 0.05),
        ("Aspect et al. (1982)", 2.697, 0.015),
        ("Weihs et al. (1998)", 2.73, 0.022),
        ("Hensen et al. (Delft 2015, LF)", 2.42, 0.20),
        ("Poh et al. (2015, Opt. Prec.)", 2.8276, 0.0008),
        ("Rosenfeld et al. (Munich 2017)", 2.221, 0.033),
        ("Storz et al. (ETH 2023, SC)", 2.0747, 0.0033),
    ]
    y_pos = np.arange(len(exps))
    vals = [e[1] for e in exps]
    errs = [e[2] for e in exps]
    labels = [e[0] for e in exps]

    ax2.axvline(2.0, color="#dc2626", lw=2.0, ls=":", label=r"Bell–CHSH Classical Bound ($S=2$)")
    ax2.axvline(2.0 * math.sqrt(2.0), color="#059669", lw=2.0, ls="-.",
                label=r"UPD Unattenuated Ideal ($2\sqrt{2} \approx 2.8284$)")
    ax2.errorbar(vals, y_pos, xerr=errs, fmt="o", color="#1d4ed8", ecolor="#60a5fa",
                 elinewidth=2.2, capsize=4, markersize=7, label="Measured $S_{\\mathrm{CHSH}} \\pm 1\\sigma$")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels, fontsize=9.0)
    ax2.invert_yaxis()
    ax2.set_xlim(1.85, 3.00)
    ax2.set_xlabel(r"Observed CHSH Correlation $S_{\mathrm{CHSH}}$", fontsize=10.5)
    ax2.set_title("B. Precision & Loophole-Free Bell Benchmarks", fontsize=11.5, fontweight="bold")
    ax2.grid(True, axis="x", alpha=0.25)
    ax2.legend(loc="lower right", fontsize=8.0, framealpha=0.93)

    plt.tight_layout()
    fig1_path = os.path.join(out_dir, "bell_chsh_correlation_curve.png")
    plt.savefig(fig1_path, dpi=220)
    plt.close(fig)

    # ---- FIGURE 2: UV Schwinger Suppression & Gravitational Macro-Bell Cutoff ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.4), dpi=220)

    E_grid = np.logspace(-14, 3.5, 300)  # GeV
    delta_S_grid = 2.0 * math.sqrt(2.0) * (E_grid / Lambda_UPD) ** 4
    ax1.loglog(E_grid, delta_S_grid, color="#1d4ed8", lw=2.5,
               label=r"UPD UV Shift $|\delta S^{\mathcal{E}}| \approx 2\sqrt{2}(E/\Lambda_{\mathrm{UPD}})^4$")
    ax1.axhline(8.0e-4, color="#dc2626", lw=1.8, ls="--",
                label=r"Best Optical CHSH Precision ($\sigma_S \approx 8\times 10^{-4}$)")
    ax1.axvline(Lambda_UPD, color="#059669", lw=1.8, ls=":",
                label=r"$\Lambda_{\mathrm{UPD}} = 1.2\ \mathrm{TeV}$")
    ax1.scatter([2e-9, 100.0],
                [uv_shifts["optical_photon_2eV"]["delta_S_CHSH"], uv_shifts["lhc_13TeV_hadronic"]["delta_S_CHSH"]],
                color="#7c3aed", zorder=5, s=45)
    ax1.annotate(r"Optical ($2$ eV): $10^{-47}$", xy=(2e-9, 2.18e-47), xytext=(1e-8, 1e-41),
                 arrowprops=dict(arrowstyle="->", color="#7c3aed"), fontsize=8.5, color="#5b21b6")
    ax1.annotate(r"EW ($100$ GeV): $1.4\times 10^{-4}$", xy=(100, 1.36e-4), xytext=(1.5, 1e-10),
                 arrowprops=dict(arrowstyle="->", color="#7c3aed"), fontsize=8.5, color="#5b21b6")
    ax1.set_xlim(1e-14, 3e3)
    ax1.set_ylim(1e-65, 10.0)
    ax1.set_xlabel(r"Probe Energy Scale $E$ (GeV)", fontsize=10.5)
    ax1.set_ylabel(r"Non-Local Schwinger Shift $|\delta S^{\mathcal{E}}|$", fontsize=10.5)
    ax1.set_title(r"A. UV Preservation of $2\sqrt{2}$ by $\mathcal{E}(-\partial^2)$", fontsize=11.5, fontweight="bold")
    ax1.grid(True, which="both", alpha=0.22)
    ax1.legend(loc="lower right", fontsize=8.0, framealpha=0.93)

    t_ms = np.linspace(0.0, 20.0, 400)
    styles = [
        (1.0e12, "#0284c7", "--", r"$M = 1.00 \times 10^{12}$ amu ($\tau_G = 98.0$ ms)"),
        (3.13e12, "#dc2626", "-", r"$M_{\mathrm{crit}} = 3.13 \times 10^{12}$ amu ($\tau_{\mathrm{crit}} = 10.0$ ms)"),
        (5.0e12, "#7c3aed", "-.", r"$M = 5.00 \times 10^{12}$ amu ($\tau_G = 3.92$ ms)"),
    ]
    for m_val, col, ls_style, lbl in styles:
        tau_m = tau_crit_ms * (M_crit_amu / m_val) ** 2
        S_eff = 2.0 * math.sqrt(2.0) * np.exp(-t_ms / tau_m)
        ax2.plot(t_ms, S_eff, color=col, ls=ls_style, lw=2.3, label=lbl)

    ax2.axhline(2.0, color="#111827", lw=1.8, ls=":", label=r"Bell Classical Threshold ($S_{\mathrm{eff}} = 2$)")
    ax2.scatter([t_bell_cutoff_ms], [2.0], color="#dc2626", zorder=6, s=55)
    ax2.annotate(rf"$t_{{\mathrm{{Bell}}}} = {t_bell_cutoff_ms:.2f}$ ms", xy=(t_bell_cutoff_ms, 2.0),
                 xytext=(t_bell_cutoff_ms + 2.2, 2.25),
                 arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.2), fontsize=9.0, color="#991b1b")
    ax2.fill_between(t_ms, 0, 2.0, color="#94a3b8", alpha=0.12)
    ax2.set_xlim(0, 20)
    ax2.set_ylim(0.2, 3.0)
    ax2.set_xlabel(r"Superposition / Interferometry Time $t$ (ms)", fontsize=10.5)
    ax2.set_ylabel(r"Effective Macro-Bell Parameter $S_{\mathrm{eff}}(t)$", fontsize=10.5)
    ax2.set_title(r"B. Macroscopic Gravitational Bell Cutoff (EC1 Bridge)", fontsize=11.5, fontweight="bold")
    ax2.grid(True, alpha=0.25)
    ax2.legend(loc="upper right", fontsize=8.0, framealpha=0.93)

    plt.tight_layout()
    fig2_path = os.path.join(out_dir, "bell_decoherence_vis_cutoff.png")
    plt.savefig(fig2_path, dpi=220)
    plt.close(fig)

    print("Simulation completed successfully.")
    print(f"CHSH max S_UPD = {S_abs:.6f} (Tsirelson = {2*math.sqrt(2):.6f})")
    print(f"Bell operator norm = {max_eig:.6f}")
    print(f"No-signaling Bob marginal diff = {no_signaling_diff:.2e}")
    print(f"GHZ Mermin S3 = {exp_Mermin:.6f} (vs LHV <= 2)")
    print(f"Experimentum Crucis 1 Bell cutoff time at M_crit = {t_bell_cutoff_ms:.4f} ms")


if __name__ == "__main__":
    main()
