"""
Quantitative Verification of Lepton Anomalous Magnetic Moments (a_e, a_mu, a_tau)
in Unified Phase Dynamics (UPD) vs. Fermilab Final World Average (2025).
"""

import json
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    out_dir = os.path.dirname(os.path.abspath(__file__))

    alpha_em = 1.0 / 137.035999084
    lambda_upd_gev = 1200.0  # 1.2 TeV electroweak-Higgs UPD scale
    delta_ym_gev = 1.60      # 1.55-1.65 GeV non-perturbative 0++ glueball gap

    leptons = {
        "electron": {"mass_GeV": 0.00051099895, "a_ref": 0.00115965218},
        "muon":     {"mass_GeV": 0.1056583755,  "a_ref": 1165920715.0e-12},
        "tau":      {"mass_GeV": 1.77686,       "a_ref": 0.00117721},
    }

    a_1loop = alpha_em / (2.0 * math.pi)
    a_mu_exp = 1165920715.0e-12
    a_mu_exp_err = 145.0e-12
    a_mu_fnal = 1165920710.0e-12
    a_mu_fnal_err = 162.0e-12

    lepton_results = {}
    for name, info in leptons.items():
        m_l = info["mass_GeV"]
        delta_nl = a_1loop * ((m_l / lambda_upd_gev) ** 4)
        lepton_results[name] = {
            "mass_GeV": m_l,
            "a_ref": info["a_ref"],
            "delta_a_nonlocal_Schwinger": delta_nl,
            "suppression_factor_m_over_Lambda_4": (m_l / lambda_upd_gev) ** 4,
        }

    results = {
        "alpha_em": alpha_em,
        "Lambda_UPD_GeV": lambda_upd_gev,
        "Delta_YM_GeV": delta_ym_gev,
        "a_1loop_Schwinger": a_1loop,
        "a_mu_Exp_World_Avg_2025": a_mu_exp,
        "a_mu_Exp_World_Avg_err": a_mu_exp_err,
        "a_mu_FNAL_2025": a_mu_fnal,
        "a_mu_FNAL_err": a_mu_fnal_err,
        "leptons": lepton_results,
        "tau_to_muon_enhancement": (leptons["tau"]["mass_GeV"] / leptons["muon"]["mass_GeV"]) ** 4,
        "muon_nonlocal_to_exp_err_ratio": lepton_results["muon"]["delta_a_nonlocal_Schwinger"] / a_mu_exp_err,
    }

    with open(os.path.join(out_dir, "muon_g2_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Figure 1: Non-local Schwinger suppression for e, mu, tau vs Fermilab 2025 precision
    scales_gev = np.logspace(2, 4, 250)
    fig, ax = plt.subplots(figsize=(7.8, 4.6), dpi=160)
    for name, color, lbl in [
        ("electron", "#9467bd", r"Electron $|\delta a_e^{\mathcal{E}}|$"),
        ("muon",     "#1f77b4", r"Muon $|\delta a_\mu^{\mathcal{E}}|$"),
        ("tau",      "#ff7f0e", r"Tau $|\delta a_\tau^{\mathcal{E}}|$"),
    ]:
        m_l = leptons[name]["mass_GeV"]
        ax.loglog(scales_gev, a_1loop * ((m_l / scales_gev) ** 4), lw=2.2, color=color, label=lbl)

    ax.axhline(a_mu_exp_err, color="#d62728", ls="--", lw=1.6, label=r"Fermilab 2025 Uncertainty ($1.45 \times 10^{-10}$)")
    ax.axvline(lambda_upd_gev, color="#2ca02c", ls=":", lw=1.8, label=r"$\Lambda_{\mathrm{UPD}} = 1.2\ \mathrm{TeV}$")
    ax.set_xlabel(r"UV Regulator Scale $\Lambda_{\mathrm{UPD}}$ (GeV)")
    ax.set_ylabel(r"Non-local Schwinger Correction $|\delta a_\ell^{\mathcal{E}}|$")
    ax.set_title(r"Lepton $g-2$ Series ($e, \mu, \tau$): Schwinger Form-Factor Suppression vs. Fermilab 2025")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(frameon=True, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "muon_g2_simulation.png"))
    plt.close(fig)

    # Figure 2: Standard Model Component Hierarchy (log scale in units of 10^-11)
    fig2, ax2 = plt.subplots(figsize=(7.8, 4.2), dpi=160)
    labels = [
        "QED (5-loop)",
        "HVP (QCD)",
        "Electroweak",
        "HLbL",
        "FNAL 2025 Err",
        "UPD Non-local (mu)",
    ]
    vals_1e11 = [1.16584719e8, 6840.0, 154.0, 92.0, 14.5, lepton_results["muon"]["delta_a_nonlocal_Schwinger"] * 1e11]
    colors = ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#ef4444", "#0f172a"]
    y_pos = np.arange(len(labels))
    ax2.barh(y_pos, vals_1e11, color=colors)
    ax2.set_xscale("log")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels)
    ax2.invert_yaxis()
    ax2.set_xlabel(r"Magnitude in units of $10^{-11}$ (log scale)")
    ax2.set_title(r"Muon $g-2$ Budget: SM Sectors, Fermilab 2025 Precision, and UPD UV Suppression")
    ax2.grid(True, axis="x", which="both", alpha=0.3)
    fig2.tight_layout()
    fig2.savefig(os.path.join(out_dir, "muon_g2_budget.png"))
    plt.close(fig2)

    for k, v in lepton_results.items():
        print(f"{k:10s}: delta_a = {v['delta_a_nonlocal_Schwinger']:.6e} (supp = {v['suppression_factor_m_over_Lambda_4']:.3e})")
    print(f"tau/muon enhancement = {results['tau_to_muon_enhancement']:.2f}x")
    print(f"muon_nl / exp_err    = {results['muon_nonlocal_to_exp_err_ratio']:.3e}")


if __name__ == "__main__":
    main()
