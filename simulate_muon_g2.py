"""
Quantitative Verification of Muon Anomalous Magnetic Moment (a_mu)
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

    # Fundamental constants
    alpha_em = 1.0 / 137.035999084
    m_mu_gev = 0.1056583755
    lambda_upd_gev = 1200.0  # 1.2 TeV electroweak-Higgs UPD scale
    delta_ym_gev = 1.60      # 1.55-1.65 GeV non-perturbative 0++ glueball gap

    # Schwinger 1-loop QED baseline
    a_mu_qed_1loop = alpha_em / (2.0 * math.pi)

    # Non-local Schwinger form-factor E(Box) = exp(-s_min^2 Box^2 / hbar^2)
    # Leading correction scales as (m_mu / Lambda_UPD)^4
    delta_a_mu_nonlocal = (alpha_em / (2.0 * math.pi)) * ((m_mu_gev / lambda_upd_gev) ** 4)

    # Experimental world average (Fermilab Runs 1-6 + BNL, June 2025, 124 ppb)
    a_mu_exp = 1165920715.0e-12
    a_mu_exp_err = 145.0e-12

    # Fermilab-only final result (139 ppb)
    a_mu_fnal = 1165920710.0e-12
    a_mu_fnal_err = 162.0e-12

    results = {
        "alpha_em": alpha_em,
        "m_mu_GeV": m_mu_gev,
        "Lambda_UPD_GeV": lambda_upd_gev,
        "Delta_YM_GeV": delta_ym_gev,
        "a_mu_QED_1loop": a_mu_qed_1loop,
        "delta_a_mu_nonlocal_Schwinger": delta_a_mu_nonlocal,
        "a_mu_Exp_World_Avg_2025": a_mu_exp,
        "a_mu_Exp_World_Avg_err": a_mu_exp_err,
        "a_mu_FNAL_2025": a_mu_fnal,
        "a_mu_FNAL_err": a_mu_fnal_err,
        "nonlocal_to_exp_err_ratio": delta_a_mu_nonlocal / a_mu_exp_err,
    }

    with open(os.path.join(out_dir, "muon_g2_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Plot: Non-local Schwinger suppression vs Fermilab precision band
    scales_gev = np.logspace(2, 4, 200)
    suppression = (alpha_em / (2.0 * math.pi)) * ((m_mu_gev / scales_gev) ** 4)

    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=150)
    ax.loglog(scales_gev, suppression, lw=2.2, color="#1f77b4", label=r"UPD Non-local Correction $\delta a_\mu^{\mathcal{E}}$")
    ax.axhline(a_mu_exp_err, color="#d62728", ls="--", lw=1.6, label=r"Fermilab 2025 Uncertainty ($1.45 \times 10^{-10}$)")
    ax.axvline(lambda_upd_gev, color="#2ca02c", ls=":", lw=1.6, label=r"$\Lambda_{\mathrm{UPD}} = 1.2\ \mathrm{TeV}$")
    ax.set_xlabel(r"UV Regulator Scale $\Lambda_{\mathrm{UPD}}$ (GeV)")
    ax.set_ylabel(r"Non-local Correction $|\delta a_\mu^{\mathcal{E}}|$")
    ax.set_title(r"Muon $g-2$: Schwinger Form-Factor Suppression vs. Fermilab 2025 Bound")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "muon_g2_simulation.png"))
    plt.close(fig)

    print(f"a_mu_QED_1loop               = {a_mu_qed_1loop:.12e}")
    print(f"delta_a_mu_nonlocal_Schwinger= {delta_a_mu_nonlocal:.6e}")
    print(f"a_mu_Exp_World_Avg_2025      = {a_mu_exp:.12e} +/- {a_mu_exp_err:.3e}")
    print(f"nonlocal / exp_err           = {delta_a_mu_nonlocal / a_mu_exp_err:.3e}")


if __name__ == "__main__":
    main()
