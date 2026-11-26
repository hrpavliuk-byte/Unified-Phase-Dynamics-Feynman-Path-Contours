#!/usr/bin/env python3
"""
Generate publication-grade 2-panel comparison figure overlaying real
156-qubit IBM Quantum Heron r2 (`ibm_fez`, Job ID: dc42jguq4uuc73a7v0j0)
experimental measurements against Unified Phase Dynamics (Psi[Sigma]) predictions.
"""

import json
import math
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(base_dir, "ibm_qpu_real_hardware_results.json"), encoding="utf-8"))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.4), dpi=220)

# Panel A: CHSH Curve — Exact UPD Theory vs Live ibm_fez QPU
th_deg = np.linspace(0.0, 180.0, 361)
th_rad = np.radians(th_deg)
s_theory = np.abs(3.0 * np.cos(th_rad) - np.cos(3.0 * th_rad))

exp1 = data["exp1_chsh_angular_sweep"]
x_pts = [r["theta_deg"] for r in exp1]
y_pts = [r["S_measured"] for r in exp1]
y_err = [r["S_stderr"] for r in exp1]

ax1.plot(th_deg, s_theory, color="#1d4ed8", lw=2.3,
         label=r"UPD Contour Theory $S_{\mathrm{UPD}}(\theta) = |3\cos\theta - \cos 3\theta|$")
ax1.axhline(2.0, color="#dc2626", lw=1.8, ls=":", label=r"Bell–CHSH Classical Bound ($S=2$)")
ax1.axhline(2.0 * math.sqrt(2.0), color="#059669", lw=1.8, ls="-.",
            label=r"Tsirelson Bound ($2\sqrt{2} \approx 2.8284$)")
ax1.fill_between(th_deg, 2.0, s_theory, where=(s_theory > 2.0), color="#3b82f6", alpha=0.14)
ax1.errorbar(x_pts, y_pts, yerr=y_err, fmt="o", color="#b91c1c", ecolor="#ef4444",
             capsize=4, elinewidth=2.0, markersize=6.5, zorder=5,
             label=r"IBM Quantum `ibm_fez` (4,096 shots/circuit)")
ax1.annotate(r"Peak $2.727 \pm 0.023$ ($31.8\sigma > 2$)", xy=(135, 2.727), xytext=(72, 2.95),
             arrowprops=dict(arrowstyle="->", color="#b91c1c", lw=1.2), fontsize=8.8, color="#991b1b")
ax1.set_xlim(0, 180)
ax1.set_ylim(0, 3.22)
ax1.set_xlabel(r"Analyzer Step Angle $\theta$ (degrees)", fontsize=10.5)
ax1.set_ylabel(r"CHSH Correlation $|S(\theta)|$", fontsize=10.5)
ax1.set_title(r"A. Real IBM QPU (`ibm_fez`) vs. $\Psi[\Sigma]$ CHSH Curve", fontsize=11.3, fontweight="bold")
ax1.grid(True, alpha=0.25)
ax1.legend(loc="lower center", fontsize=7.9, framealpha=0.94)

# Panel B: 4-Qubit Closed Wilson Plaquette Loop & 3-Qubit GHZ Inset Info
a_grid = np.linspace(0.0, math.pi / 2.0, 200)
w_theory = np.cos(a_grid) ** 4 + np.sin(a_grid) ** 4
exp4 = data["exp4_wilson_plaquette_holonomy"]
ax_pts = [r["coupling_angle_rad"] for r in exp4]
wz_pts = [r["Wilson_loop_Z0Z1Z2Z3_meas"] for r in exp4]
wx_pts = [r["dual_X0X1X2X3_meas"] for r in exp4]

ax2.plot(a_grid, w_theory, color="#0284c7", lw=2.3,
         label=r"Exact Plaquette Curve $\cos^4\alpha + \sin^4\alpha$")
ax2.plot(ax_pts, wz_pts, "o-", color="#7c3aed", lw=1.6, ms=7,
         label=r"`ibm_fez` Wilson Loop $\langle Z_0 Z_1 Z_2 Z_3 \rangle$")
ax2.plot(ax_pts, wx_pts, "s--", color="#059669", lw=1.6, ms=6.5,
         label=r"`ibm_fez` Dual Loop $\langle X_0 X_1 X_2 X_3 \rangle$")

ghz_m3 = data["exp3_ghz_mermin_paradox"]["M3_measured"]
ghz_err = data["exp3_ghz_mermin_paradox"]["M3_stderr"]
info_txt = (
    f"IBM Heron r2 (`ibm_fez`)\n"
    f"Job: dc42jguq4uuc73a7v0j0\n"
    f"3-Qubit GHZ–Mermin:\n"
    f"  <M3> = {ghz_m3:.4f} ± {ghz_err:.4f}\n"
    f"  (>166σ above LHV ≤ 2)"
)
ax2.text(0.50, 0.87, info_txt, fontsize=8.7, bbox=dict(boxstyle="round,pad=0.45", facecolor="#f8fafc", edgecolor="#cbd5e1"))
ax2.set_xlim(-0.05, math.pi / 2.0 + 0.05)
ax2.set_ylim(0.35, 1.12)
ax2.set_xlabel(r"Gauge Twist Angle $\alpha$ (radians)", fontsize=10.5)
ax2.set_ylabel(r"4-Qubit Plaquette Holonomy Expectation", fontsize=10.5)
ax2.set_title(r"B. 4-Qubit Wilson Plaquette & 3-Qubit GHZ (`ibm_fez`)", fontsize=11.3, fontweight="bold")
ax2.grid(True, alpha=0.25)
ax2.legend(loc="lower center", fontsize=8.0, framealpha=0.94)

plt.tight_layout()
out_png = os.path.join(base_dir, "ibm_fez_hardware_benchmark.png")
plt.savefig(out_png, dpi=220)
plt.close(fig)
print("Generated:", out_png)
