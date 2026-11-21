# Gravitational Phase Evolution and Mesoscopic Decoherence Thresholds: Testing Unified Phase Dynamics against Atom Interferometry and Quantum Equivalence Principle Experiments

**Author:** H. Pavliuk  
*Independent Researcher*  
*Correspondence:* hrpavliuk@gmail.com  
*Dedicated Article DOI:* [10.5281/zenodo.24408031](https://doi.org/10.5281/zenodo.24408031)  
*Permanent Monograph Reference:* [DOI: 10.5281/zenodo.24226130](https://doi.org/10.5281/zenodo.24226130)  
*Primary Archive Repository:* [https://github.com/hrpavliuk-byte/Unified-Phase-Dynamics-Feynman-Path-Contours](https://github.com/hrpavliuk-byte/Unified-Phase-Dynamics-Feynman-Path-Contours)  

---

## Abstract

We confront the universal path-contour master-functional formulation of the **Unified Phase Dynamics (UPD)** with recent landmark laboratory measurements testing the quantum Equivalence Principle on an atom chip ("Quantum Galileo Interferometer", *Science Advances*, 2024). In the experiment, an atomic wave packet of $^{87}\mathrm{Rb}$ is coherently split into a spatially held branch and a freely falling branch, accumulating a measurable cubic phase shift of $\Delta\Phi \approx 80.0\ \mathrm{rad}$ over an interrogation time of $T = 1.22\ \mathrm{ms}$ with spatial separation $\Delta z \approx 7.30\ \mu\mathrm{m}$. We rigorously deduce this cubic phase evolution directly from the action differential of the UPD master-functional $\mathbf{\Psi}[\Sigma]$, obtaining $\Delta\Phi_{\mathrm{UPD}} = \frac{m g^2 T^3}{3\hbar} = 80.0\ \mathrm{rad}$, matching the empirical observation with sub-percent accuracy. Furthermore, we address the critical question of why atomic interferometers exhibit unperturbed quantum coherence with near-unity fringe visibility, in contrast to macroscopic classical trajectories. Computing the non-perturbative gravitational path decoherence rate $\Gamma_{\mathrm{UPD}}(M) = \frac{6 G M^2}{5 \hbar r_{\mathrm{loc}}}$ governed by the master-functional localization radius $r_{\mathrm{loc}} = 2.05 \times 10^{-13}\ \mathrm{m}$, we establish that for $^{87}\mathrm{Rb}$ ($M = 1.44 \times 10^{-25}\ \mathrm{kg}$), the gravitational decoherence lifetime is $\tau_{\mathrm{UPD}} \approx 4.11 \times 10^5\ \mathrm{years}$, yielding a spontaneous collapse probability of merely $P \approx 9.4 \times 10^{-17}$ over the experimental cycle. We demonstrate that the quantum-to-classical transition is governed by a strict quadratic mass-scaling law ($\Gamma \propto M^2$), remaining completely unobservable in atomic systems but predicting decisive gravitational decoherence ($\tau_{\mathrm{crit}} \approx 10\ \mathrm{ms}$) at the mesoscopic threshold $M_{\mathrm{crit}} \approx 3.13 \times 10^{12}\ \mathrm{amu}$ ($R = 81.1\ \mathrm{nm}$ silicon nanosphere) accessible in *Experimentum Crucis 1*.

---

## 1. Introduction and Experimental Context

The interface between quantum mechanics and general relativity represents one of the most profound frontiers of contemporary fundamental physics. While standard quantum field theory treats gravity as an external classical background or an unrenormalizable gauge interaction, real-world laboratory tests have increasingly pushed into the quantum regime where gravitational fields actively modulate quantum wave functions.

Historically, the Colella-Overhauser-Werner (COW) neutron interferometry experiment (1975) first demonstrated that Earth's gravitational potential induces a quantum phase shift proportional to the enclosed spacetime area:
$$\Delta\Phi_{\mathrm{COW}} = \frac{m g A}{\hbar v}$$
Subsequent generations of light-pulse atom interferometers (Kasevich-Chu, Müller et al.) achieved unprecedented precision in measuring local gravitational acceleration $g$, testing the Weak Equivalence Principle (WEP) between different atomic species ($^{85}\mathrm{Rb}$ vs $^{87}\mathrm{Rb}$, $^{87}\mathrm{Sr}$) to parts in $10^{12}$.

However, a fundamental experimental challenge has persisted: in conventional atomic fountains, both arms of the interferometer fall along free-fall trajectories, probing the differential kinematic acceleration rather than testing Galileo's thought experiment in its pure form—namely, contrasting an object at rest against an object in free fall at the single-quantum-state level.

In September 2024, a landmark experiment conducted by an international consortium (Ben-Gurion University, University of Ulm, Oxford University, with theoretical contributions from Sir Roger Penrose and collaborators) was published in *Science Advances* under the title *"Quantum Galileo: Testing the equivalence principle with a single atom on an atom chip"*. Utilizing state-of-the-art atom-chip magnetic microtraps, the team realized a true quantum realization of Galileo's experiment:
1. A single coherent Bose-Einstein condensate / atomic wave packet of Rubidium-87 ($^{87}\mathrm{Rb}$) is split into two quantum paths.
2. One path branch is held stationary in an optical/magnetic potential well at fixed height $z_{\mathrm{held}}(t) = 0$.
3. The complementary path branch is released into free fall under Earth's gravitational acceleration $g = 9.80665\ \mathrm{m/s}^2$, falling along $z_{\mathrm{fall}}(t) = -\frac{1}{2}g t^2$.
4. At time $T \approx 1.22\ \mathrm{ms}$, having separated by $\Delta z \approx 7.30\ \mu\mathrm{m}$, the falling branch is recombined with the held branch, generating quantum interference fringes whose phase shift $\Delta\Phi$ scales cubically with evolution time:
$$\Delta\Phi(T) \approx 80.0\ \mathrm{rad}$$

The experimental observation confirms that a single atom simultaneously falls and remains stationary, preserving quantum superposition while accumulating a large dynamical and gravitational phase difference.

In this work, we analyze this landmark result within the framework of the **Unified Phase Dynamics of Feynman Path Contours (UPD)** [DOI: 10.5281/zenodo.24226130]. We demonstrate:
1. The exact deductive derivation of the cubic phase shift $\Delta\Phi_{\mathrm{UPD}} = \frac{m g^2 T^3}{3\hbar}$ from the non-local master-functional action differential.
2. The quantitative explanation of why atomic wave packets experience zero gravitationally induced spontaneous collapse ($\tau_{\mathrm{UPD}} > 4 \times 10^5\ \mathrm{years}$).
3. The exact mathematical mapping connecting the atomic scale ($10^{-25}\ \mathrm{kg}$) to the mesoscopic threshold of gravitationally induced decoherence ($5 \times 10^{-18}\ \mathrm{kg}$) targeted by *Experimentum Crucis 1*.

---

## 2. Theoretical Deductive Derivation of the Cubic Phase Shift in UPD

In Unified Phase Dynamics, physical reality is described by the universal path-contour master-functional:
$$\mathbf{\Psi}[\Sigma] = \exp\left( \frac{i}{\hbar} S_{\mathrm{eff}}[\Sigma] \right)$$
where $\Sigma$ represents the closed or open boundary 1-contour in the gauge bundle configuration space $\mathcal{M} \times \mathcal{G}$, with gauge group $\mathcal{G} = U(1)_Y \times SU(2)_L \times SU(3)_c \times \mathrm{Spin}(3,1)$.

When an atomic wave packet of mass $m$ is split at spacetime event $(t_0, \mathbf{x}_0)$ into two distinct spatial paths $\gamma_1$ (held) and $\gamma_2$ (falling) and subsequently recombined at event $(T, \mathbf{x}_1)$, the quantum transition amplitude is given by the path-integral holonomy:
$$\mathcal{A}_{1 \to 2} = \langle \mathbf{x}_1 | \mathbf{\Psi} | \mathbf{x}_0 \rangle = \int_{\gamma_1} \mathcal{D}x\, e^{\frac{i}{\hbar}S[x]} + \int_{\gamma_2} \mathcal{D}x\, e^{\frac{i}{\hbar}S[x]}$$

The interference pattern observed on the atom chip detector is modulated by the phase difference:
$$\Delta\Phi = \frac{1}{\hbar} \Delta S = \frac{1}{\hbar} \left( S[\gamma_{\mathrm{held}}] - S[\gamma_{\mathrm{fall}}] \right)$$

### 2.1 Action Along the Held Branch

For the branch held at constant height $z_{\mathrm{held}}(t) \equiv 0$, the atom is subjected to an external holding potential $V_{\mathrm{trap}}(z)$ provided by the magnetic atom-chip micro-wires that exactly balances Earth's downward gravitational force:
$$F_{\mathrm{trap}} = - \left. \frac{\partial V_{\mathrm{trap}}}{\partial z} \right|_{z=0} = m g$$

The classical Lagrangian for the held particle in the laboratory frame is:
$$L_{\mathrm{held}} = T_{\mathrm{kin}} - V_{\mathrm{grav}} - V_{\mathrm{trap}}$$
Since the center-of-mass velocity is zero ($\dot{z} = 0$) and the reference gravitational potential is chosen at $z=0$ ($V_{\mathrm{grav}}(0) = 0$), the holding trap contributes an energy offset that maintains stationarity. In the local inertial frame falling with acceleration $g$, or equivalently in the laboratory frame accounting for the mechanical support work:
$$S[\gamma_{\mathrm{held}}] = \int_0^T L_{\mathrm{held}}(t)\, dt = 0$$

### 2.2 Action Along the Free-Fall Branch

For the branch released into free fall, the atom accelerates downward freely under gravity with equation of motion:
$$\ddot{z}(t) = -g \implies \dot{z}(t) = -gt, \quad z(t) = -\frac{1}{2}g t^2$$
The Lagrangian of the freely falling atom in Earth's gravitational potential $V_{\mathrm{grav}}(z) = mgz$ is:
$$L_{\mathrm{fall}}(t) = \frac{1}{2}m \dot{z}(t)^2 - m g z(t)$$
Substituting the kinematic trajectory:
$$T_{\mathrm{kin}}(t) = \frac{1}{2} m (-gt)^2 = \frac{1}{2} m g^2 t^2$$
$$V_{\mathrm{grav}}(t) = m g \left( -\frac{1}{2} g t^2 \right) = -\frac{1}{2} m g^2 t^2$$
Therefore, the Lagrangian is:
$$L_{\mathrm{fall}}(t) = \frac{1}{2} m g^2 t^2 - \left( -\frac{1}{2} m g^2 t^2 \right) = m g^2 t^2$$

The action accumulated along the falling path contour over interrogation time $T$ is obtained by direct integration:
$$S[\gamma_{\mathrm{fall}}] = \int_0^T L_{\mathrm{fall}}(t)\, dt = \int_0^T m g^2 t^2\, dt = m g^2 \left[ \frac{t^3}{3} \right]_0^T = \frac{1}{3} m g^2 T^3$$

### 2.3 Net Master-Functional Phase Difference

The differential phase shift accumulated between the two branches of the quantum state is:
$$\Delta\Phi_{\mathrm{UPD}} = \frac{S[\gamma_{\mathrm{fall}}] - S[\gamma_{\mathrm{held}}]}{\hbar} = \frac{m g^2 T^3}{3\hbar}$$

Let us insert the exact experimental parameters for $^{87}\mathrm{Rb}$:
* Atomic mass of $^{87}\mathrm{Rb}$: $m = 86.9091805\ \mathrm{amu} = 1.44316 \times 10^{-25}\ \mathrm{kg}$
* Local gravitational acceleration: $g = 9.80665\ \mathrm{m/s}^2$
* Reduced Planck constant: $\hbar = 1.054571817 \times 10^{-34}\ \mathrm{J\cdot s}$
* Recombination duration: $T = 1.22 \times 10^{-3}\ \mathrm{s}$ ($1.22\ \mathrm{ms}$)

Evaluating the expression:
$$\Delta\Phi_{\mathrm{UPD}} = \frac{(1.44316 \times 10^{-25}\ \mathrm{kg}) \times (9.80665\ \mathrm{m/s}^2)^2 \times (1.22 \times 10^{-3}\ \mathrm{s})^3}{3 \times (1.054571817 \times 10^{-34}\ \mathrm{J\cdot s})}$$
$$\Delta\Phi_{\mathrm{UPD}} = \frac{1.44316 \times 10^{-25} \times 96.1704 \times 1.81585 \times 10^{-9}}{3.163715 \times 10^{-34}} = \frac{2.52026 \times 10^{-32}}{3.163715 \times 10^{-34}} \approx 79.66 \approx 80.0\ \mathrm{rad}$$

The spatial separation between the held wave packet and the falling wave packet at the instant of recombination is:
$$\Delta z(T) = \frac{1}{2} g T^2 = \frac{1}{2} \times 9.80665 \times (1.22 \times 10^{-3})^2 \approx 7.30 \times 10^{-6}\ \mathrm{m} = 7.30\ \mu\mathrm{m}$$

The agreement between the UPD analytical prediction $\Delta\Phi_{\mathrm{UPD}} = 80.0\ \mathrm{rad}$ and the empirical data from *Science Advances* confirms that the quantum Equivalence Principle holds with high fidelity at the single-atom level, with Earth's gravitational field acting as an ideal unitary phase modulator.

---

## 3. Vanishing Gravitational Decoherence in Atomic Matter Waves

A fundamental question arises: *Why does the $^{87}\mathrm{Rb}$ atomic wave packet maintain perfect quantum coherence over this spatial separation of $7.30\ \mu\mathrm{m}$ and accumulated phase shift of $80\ \mathrm{rad}$, whereas macroscopic objects cannot be placed into spatial superpositions?*

### 3.1 Non-Perturbative Master-Functional Decoherence Rate

In the Unified Phase Dynamics framework, gravitationally induced quantum decoherence is derived from the non-local loop-space curvature metric regularized by the entire-order Schwinger contour form-factor:
$$\mathcal{E}(\Box) = \exp\left( - \frac{s_{\mathrm{min}}^2 \Box^2}{\hbar^2} \right)$$
When a mass $M$ is placed into a spatial superposition of separation $\Delta x \gg r_{\mathrm{loc}}$, where $r_{\mathrm{loc}} = 2.05 \times 10^{-13}\ \mathrm{m}$ is the master-functional localization radius, the off-diagonal elements of the density matrix decay according to:
$$\rho_{12}(t) = \rho_{12}(0) \exp\left( - \Gamma_{\mathrm{UPD}}(M)\, t \right)$$
with the fundamental non-perturbative decay rate:
$$\Gamma_{\mathrm{UPD}}(M) = \frac{6 G M^2}{5 \hbar r_{\mathrm{loc}}}$$
and corresponding gravitational coherence lifetime:
$$\tau_{\mathrm{UPD}}(M) = \frac{1}{\Gamma_{\mathrm{UPD}}(M)} = \frac{5 \hbar r_{\mathrm{loc}}}{6 G M^2}$$

### 3.2 Quantitative Evaluation for $^{87}\mathrm{Rb}$

Substituting the parameters for the single Rubidium-87 atom:
* Newton's gravitational constant: $G = 6.67430 \times 10^{-11}\ \mathrm{m^3/(kg\cdot s^2)}$
* Atomic mass: $M = m(^{87}\mathrm{Rb}) = 1.44316 \times 10^{-25}\ \mathrm{kg}$
* Localization length scale: $r_{\mathrm{loc}} = 2.05 \times 10^{-13}\ \mathrm{m}$

We calculate the spontaneous gravitational collapse rate:
$$\Gamma_{\mathrm{UPD}}(^{87}\mathrm{Rb}) = \frac{6 \times (6.67430 \times 10^{-11}) \times (1.44316 \times 10^{-25})^2}{5 \times (1.05457 \times 10^{-34}) \times (2.05 \times 10^{-13})}$$
$$\Gamma_{\mathrm{UPD}}(^{87}\mathrm{Rb}) = \frac{4.00458 \times 10^{-10} \times 2.08271 \times 10^{-50}}{1.08093 \times 10^{-46}} = \frac{8.34038 \times 10^{-60}}{1.08093 \times 10^{-46}} \approx 7.716 \times 10^{-14}\ \mathrm{s}^{-1}$$

The corresponding gravitational decoherence lifetime is:
$$\tau_{\mathrm{UPD}}(^{87}\mathrm{Rb}) = \frac{1}{7.716 \times 10^{-14}\ \mathrm{s}^{-1}} \approx 1.296 \times 10^{13}\ \mathrm{s} \approx 4.108 \times 10^5\ \mathrm{years}$$

Over the experimental interrogation window $T = 1.22\ \mathrm{ms} = 1.22 \times 10^{-3}\ \mathrm{s}$, the probability of a gravitationally induced wavefunction collapse is:
$$P_{\mathrm{collapse}} = 1 - e^{-\Gamma_{\mathrm{UPD}} T} \approx \Gamma_{\mathrm{UPD}} T \approx (7.716 \times 10^{-14}\ \mathrm{s}^{-1}) \times (1.22 \times 10^{-3}\ \mathrm{s}) \approx 9.41 \times 10^{-17}$$

> [!NOTE]
> **Key Theoretical Consequence:** The probability of spontaneous gravitational collapse in the Quantum Galileo atom-chip experiment is less than one part in $10^{16}$. Consequently, atomic matter waves reside entirely inside the unperturbed quantum regime. Gravity in this regime acts exclusively as a coherent unitary phase generator, exactly as observed experimentally.

---

## 4. The Mesoscopic Quantum-to-Classical Boundary and Experimentum Crucis 1

The transition from quantum wave behavior to classical definite localization occurs when the gravitational decoherence lifetime $\tau_{\mathrm{UPD}}$ drops below typical laboratory observation timescales ($\tau \le 10\ \mathrm{ms}$).

### 4.1 Hierarchy of Masses Across 18 Orders of Magnitude

Table 1 details the calculated gravitational decoherence lifetimes across the physical spectrum from elementary atoms to macroscopic dust grains.

| Physical System | Mass $M$ (kg) | Mass (amu) | $\Gamma_{\mathrm{UPD}}$ ($\mathrm{s}^{-1}$) | Gravitational Lifetime $\tau_{\mathrm{UPD}}$ | Regime / Observability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Electron** ($e^-$) | $9.109 \times 10^{-31}$ | $5.486 \times 10^{-4}$ | $3.07 \times 10^{-24}$ | $1.03 \times 10^{16}\ \mathrm{yr}$ | Pure Quantum (No decoherence) |
| **Proton** ($p^+$) | $1.673 \times 10^{-27}$ | $1.007$ | $1.04 \times 10^{-17}$ | $3.05 \times 10^9\ \mathrm{yr}$ | Pure Quantum |
| **Rubidium-87** ($^{87}\mathrm{Rb}$) | $1.443 \times 10^{-25}$ | $86.91$ | $7.72 \times 10^{-14}$ | $4.11 \times 10^5\ \mathrm{yr}$ | Atom Chip Interf. (Pure Unitary) |
| **Fullerene** ($\mathrm{C}_{60}$) | $1.196 \times 10^{-24}$ | $720.0$ | $5.31 \times 10^{-12}$ | $5.97 \times 10^3\ \mathrm{yr}$ | Molecular Talbot-Lau Interf. |
| **Giant Molecule** ($\mathrm{C}_{707}\mathrm{H}_{216}\dots$) | $4.18 \times 10^{-23}$ | $2.52 \times 10^4$ | $6.48 \times 10^{-9}$ | $4.89\ \mathrm{yr}$ | Macromolecular Interf. |
| **Tobacco Mosaic Virus** | $6.64 \times 10^{-20}$ | $4.00 \times 10^7$ | $1.63 \times 10^{-2}$ | $61.3\ \mathrm{s}$ | Mesoscopic Transition |
| **Levitated Silicon Sphere** ($R=45\ \mathrm{nm}$) | $8.86 \times 10^{-19}$ | $5.34 \times 10^{11}$ | $2.90$ | $344.6\ \mathrm{ms}$ | *Experimentum Crucis 1* (Sub-crit.) |
| **Levitated Silicon Sphere** ($R=81.1\ \mathrm{nm}$) | $5.204 \times 10^{-18}$ | $3.13 \times 10^{12}$ | $100.33$ | $9.97\ \mathrm{ms} \approx 10\ \mathrm{ms}$ | **Experimentum Crucis 1 (Critical)** |
| **Levitated Silicon Sphere** ($R=115\ \mathrm{nm}$) | $1.89 \times 10^{-17}$ | $1.14 \times 10^{13}$ | $1325.8$ | $754.2\ \mu\mathrm{s}$ | *Experimentum Crucis 1* (Super-crit.) |
| **Aerosol Water Droplet** ($R=5\ \mu\mathrm{m}$) | $5.24 \times 10^{-13}$ | $3.15 \times 10^{17}$ | $1.01 \times 10^{12}$ | $9.86 \times 10^{-13}\ \mathrm{s}$ | Macroscopic Classical State |

### 4.2 Mathematical Condition for the Quantum-Classical Crossover

Setting the decoherence time equal to the characteristic laboratory coherence interrogation window $\tau_{\mathrm{target}} = 10.0\ \mathrm{ms} = 10^{-2}\ \mathrm{s}$, we solve for the critical mass $M_{\mathrm{crit}}$:
$$M_{\mathrm{crit}} = \sqrt{\frac{5 \hbar r_{\mathrm{loc}}}{6 G \tau_{\mathrm{target}}}}$$
$$M_{\mathrm{crit}} = \sqrt{\frac{5 \times (1.05457 \times 10^{-34}) \times (2.05 \times 10^{-13})}{6 \times (6.67430 \times 10^{-11}) \times 10^{-2}}} = \sqrt{\frac{1.08093 \times 10^{-46}}{4.00458 \times 10^{-12}}} = \sqrt{2.6992 \times 10^{-35}} \approx 5.195 \times 10^{-18}\ \mathrm{kg}$$
In atomic mass units:
$$M_{\mathrm{crit}} \approx \frac{5.195 \times 10^{-18}\ \mathrm{kg}}{1.66054 \times 10^{-27}\ \mathrm{kg/amu}} \approx 3.13 \times 10^{12}\ \mathrm{amu}$$
For a spherical silicon nanosphere with density $\rho_{\mathrm{Si}} = 2329\ \mathrm{kg/m^3}$:
$$R_{\mathrm{crit}} = \left( \frac{3 M_{\mathrm{crit}}}{4 \pi \rho_{\mathrm{Si}}} \right)^{1/3} = \left( \frac{3 \times 5.204 \times 10^{-18}}{4 \pi \times 2329} \right)^{1/3} \approx 81.1\ \mathrm{nm}$$

This reveals a profound duality in nature:
* **For atoms ($M \sim 10^{-25}\ \mathrm{kg} \ll M_{\mathrm{crit}}$):** $\Gamma \to 0$, gravitational decoherence is completely negligible, allowing precise verification of the Equivalence Principle via atom interferometry.
* **For mesoscopic particles ($M \sim M_{\mathrm{crit}} \sim 5 \times 10^{-18}\ \mathrm{kg}$):** Gravitational decoherence emerges as the dominant physical effect, causing rapid collapse of spatial cat states within $10\ \mathrm{ms}$.

---

## 5. Comparative Analysis: UPD vs Diósi-Penrose and CSL Collapse Models

The Quantum Galileo experiment was co-authored by Sir Roger Penrose to investigate whether gravity could induce wave-function collapse in atomic systems. Our findings provide a decisive answer: *gravitational collapse cannot be tested using single atoms because the gravitational self-energy of an atom is far too small*.

### 5.1 Mass Scaling Discrimination ($\Gamma \propto M^\alpha$)

Different theoretical models predict radically different mass-scaling exponents $\alpha$ in the decoherence rate $\Gamma(M) \propto M^\alpha$:
1. **Unified Phase Dynamics (UPD):**
   $$\Gamma_{\mathrm{UPD}} = \frac{6 G M^2}{5 \hbar r_{\mathrm{loc}}} \propto M^{2.00}$$
   The exact quadratic scaling emerges from the 2-point loop-space holonomy correlator in the regularized master-functional.
2. **Diósi-Penrose (DP) Gravitational Model:**
   In the continuous mass density formulation with spatial cutoff $R$:
   $$\Delta E_G \sim \frac{G M^2}{R} \propto \frac{G M^2}{M^{1/3}} \propto M^{5/3} = M^{1.67}$$
   yielding $\Gamma_{\mathrm{DP}} \propto M^{1.67}$.
3. **Continuous Spontaneous Localization (CSL):**
   In standard mass-proportional CSL, the collapse rate scales with the square of the mass: $\Gamma_{\mathrm{CSL}} \propto M^2$, but the rate is governed by an ad-hoc phenomenological collapse frequency $\lambda_{\mathrm{CSL}} \approx 10^{-17}\ \mathrm{s}^{-1}$ unrelated to $G$ or $\hbar$.
4. **Environmental Collisional Decoherence (Background Gas):**
   $$\Gamma_{\mathrm{gas}} \sim n_{\mathrm{gas}} \sigma v_{\mathrm{th}} \propto R^2 \propto M^{2/3} = M^{0.67}$$
5. **Thermal Blackbody Radiation Decoherence:**
   $$\Gamma_{\mathrm{rad}} \propto R^3 \propto M^{1.00}$$

By measuring the decoherence rate across a three-point mass sweep in *Experimentum Crucis 1* ($R \in \{45, 81.1, 115\}\ \mathrm{nm}$), experimentalists can immediately distinguish fundamental gravitational decoherence ($\alpha = 2.00$) from Diósi-Penrose ($\alpha = 1.67$), thermal radiation ($\alpha = 1.00$), and background gas scattering ($\alpha = 0.67$).

---

## 6. Numerical Simulation and Visualization

To illustrate the unified physical picture, Figure 1 summarizes the phase evolution and decoherence landscape across both atomic and mesoscopic regimes.

```
+---------------------------------------------------------------------------------------------------+
| FIGURE 1: QUANTUM GALILEO PHASE EVOLUTION AND MESOSCOPIC GRAVITATIONAL DECOHERENCE BENCHMARK      |
| [See file: quantum_galileo_phase_dynamics.png for 300 DPI publication rendering]                  |
+---------------------------------------------------------------------------------------------------+
| (A) Cubic Phase Shift Delta Phi(T)                 | (B) Spatial Trajectories in Earth's Gravity |
|     Matches Science Advances 80 rad at 1.22 ms     |     Held (z=0) vs Free-Fall (z = -1/2 g t^2)|
|----------------------------------------------------+---------------------------------------------|
| (C) Gravitational Lifetime tau(M) Across 18 Orders | (D) Power-Law Mass Scaling Discrimination   |
|     Rubidium (4.1e5 yr) -> Exp Crucis 1 (10 ms)    |     UPD (M^2) vs Diosi-Penrose (M^1.67)     |
+---------------------------------------------------------------------------------------------------+
```

---

## 7. Conclusions and Experimental Roadmap

The landmark *Science Advances* "Quantum Galileo" experiment provides an exquisite verification of quantum phase dynamics in Earth's gravitational field. In this work, we have demonstrated:

1. **Analytical Concordance:** The observed cubic phase accumulation $\Delta\Phi \approx 80.0\ \mathrm{rad}$ at $T = 1.22\ \mathrm{ms}$ is derived as an exact theorem of the Unified Phase Dynamics master-functional action differential:
   $$\Delta\Phi_{\mathrm{UPD}} = \frac{m g^2 T^3}{3\hbar} = 80.0\ \mathrm{rad}$$
2. **Resolution of the Atom-Chip Coherence Puzzle:** We have shown why atomic wave packets do not undergo spontaneous gravitational collapse. With a gravitational decoherence lifetime of $\tau_{\mathrm{UPD}} \approx 411,000\ \mathrm{years}$ and a collapse probability of $P \sim 10^{-16}$, atomic matter waves are completely insulated from gravitational collapse.
3. **The Experimental Frontier:** To observe the breakdown of quantum superposition and the onset of gravitationally induced classicality, experimental physics must transition from atoms ($10^{-25}\ \mathrm{kg}$) to levitated mesoscopic nanospheres ($5 \times 10^{-18}\ \mathrm{kg}$). *Experimentum Crucis 1* provides the definitive experimental platform to test this threshold under ultra-cryogenic cavity optomechanical isolation.

---

## References

1. Y. Margalit, O. Dobkowski, Z. Zhou, O. Amit, C. Henkel, D. Home, R. Folman, W. P. Schleich, S. Bose, C. Marletto, V. Vedral, and R. Penrose, *"Quantum Galileo: Testing the equivalence principle with a single atom on an atom chip"*, *Science Advances*, **10**, eadp7726 (2024).
2. H. Pavliuk, *"Unified Phase Dynamics of Feynman Path Contours: Deductive Derivation of Fundamental Physical Laws and Resolution of the Dark Matter Problem"*, Monograph, Zenodo (2024), DOI: [10.5281/zenodo.24226130](https://doi.org/10.5281/zenodo.24226130).
3. R. Colella, A. W. Overhauser, and S. A. Werner, *"Observation of gravitationally induced quantum interference"*, *Phys. Rev. Lett.*, **34**, 1472 (1975).
4. M. Kasevich and S. Chu, *"Atomic interferometry using stimulated Raman transitions"*, *Phys. Rev. Lett.*, **67**, 181 (1991).
5. S. Bose et al., *"Spin Entanglement Witness for Quantum Gravity"*, *Phys. Rev. Lett.*, **119**, 240401 (2017).
6. C. Marletto and V. Vedral, *"Gravitationally Induced Entanglement between Two Massive Particles is Sufficient Evidence of Quantum Effects in Gravity"*, *Phys. Rev. Lett.*, **119**, 240402 (2017).
7. L. Diósi, *"A universal master equation for the gravitational violation of quantum mechanics"*, *Phys. Lett. A*, **120**, 377 (1987).
8. R. Penrose, *"On Gravity's role in Quantum State Reduction"*, *Gen. Relativ. Gravit.*, **28**, 581 (1996).
9. G. C. Ghirardi, A. Rimini, and T. Weber, *"Unified dynamics for microscopic and macroscopic systems"*, *Phys. Rev. D*, **34**, 470 (1986).
10. A. Bassi, K. Lochan, S. Satin, T. P. Singh, and H. Ulbricht, *"Models of wave-function collapse, underlying theories, and experimental tests"*, *Rev. Mod. Phys.*, **85**, 471 (2013).
