"""DOE model backend for student simulator."""
from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np
import statsmodels.api as sm


@dataclass
class DOEModel:
    seed: int
    model_type: str  # "gaussian" or "polynomial"
    intercept: float
    # Linear coefficients for all factors (adds noise)
    b_a: float
    b_b: float
    b_c: float
    b_d: float
    b_e: float
    b_f: float
    b_g: float
    # Polynomial coefficients (for polynomial model)
    b_aa: float
    b_bb: float
    b_cc: float
    b_dd: float
    b_ee: float
    b_ff: float
    b_gg: float
    b_aaa: float
    b_bbb: float
    b_ccc: float
    b_ddd: float
    b_eee: float
    b_fff: float
    b_ggg: float
    b_ab: float
    b_aab: float
    b_abb: float
    # Gaussian peak parameters for the 2 significant factors
    # Peak 1 - larger peak
    peak1_center_x: float
    peak1_center_y: float
    peak1_amplitude: float
    peak1_variance: float  # controls width (smaller = sharper)
    # Peak 2 - smaller secondary peak
    peak2_center_x: float
    peak2_center_y: float
    peak2_amplitude: float
    peak2_variance: float
    sig_factors: Tuple[str, str]
    noise_std: float


def generate_seeded_model(seed: int = 12345678, noise_std: float = 0.0, model_type: str = "gaussian") -> DOEModel:
    """Generate deterministic model based on 8-digit seed.
    
    Args:
        seed: 8-digit seed for reproducibility
        noise_std: Standard deviation of noise
        model_type: Either "gaussian" (Gaussian peaks) or "polynomial" (quadratic/cubic)
    """
    normalized_seed = int(seed) % 100000000
    rng = np.random.default_rng(normalized_seed)

    factors = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    
    # Select 2 random significant factors
    sig_indices = rng.choice(7, 2, replace=False)
    sig_factors = tuple(sorted(factors[i] for i in sig_indices))

    intercept = rng.uniform(0, 5)

    # Linear coefficients: significant have small, others tiny (just noise)
    linear_coeffs = {}
    for f in factors:
        if f in sig_factors:
            linear_coeffs[f] = rng.uniform(0.01, 0.1) * (1 if rng.random() > 0.5 else -1)
        else:
            linear_coeffs[f] = rng.uniform(0.001, 0.05) * (1 if rng.random() > 0.5 else -1)

    if model_type == "gaussian":
        # Generate two Gaussian peaks within bounds [-50, 50]
        peak1_center_x = rng.uniform(-40, 40)
        peak1_center_y = rng.uniform(-40, 40)
        peak1_amplitude = rng.uniform(5, 15)
        peak1_variance = rng.uniform(10, 30)

        peak2_center_x = rng.uniform(-40, 40)
        peak2_center_y = rng.uniform(-40, 40)
        peak2_amplitude = rng.uniform(2, 8)
        peak2_variance = rng.uniform(10, 30)

        # Polynomial coefficients set to 0 for Gaussian model
        quad_coeffs = {f: 0.0 for f in factors}
        cubic_coeffs = {f: 0.0 for f in factors}
        b_ab = 0.0
        b_aab = 0.0
        b_abb = 0.0

    else:  # polynomial
        # Generate polynomial coefficients
        quad_coeffs = {f: 0.0 for f in factors}
        for f in sig_factors:
            quad_coeffs[f] = -rng.uniform(0.005, 0.02)

        cubic_coeffs = {f: 0.0 for f in factors}
        for f in sig_factors:
            cubic_coeffs[f] = rng.uniform(0.0001, 0.001) * (1 if rng.random() > 0.5 else -1)

        b_ab = rng.uniform(0.01, 0.05) * (1 if rng.random() > 0.5 else -1)
        b_aab = rng.uniform(0.0001, 0.001) * (1 if rng.random() > 0.5 else -1)
        b_abb = rng.uniform(0.0001, 0.001) * (1 if rng.random() > 0.5 else -1)

        # Gaussian coefficients set to 0 for polynomial model
        peak1_center_x = 0.0
        peak1_center_y = 0.0
        peak1_amplitude = 0.0
        peak1_variance = 1.0
        peak2_center_x = 0.0
        peak2_center_y = 0.0
        peak2_amplitude = 0.0
        peak2_variance = 1.0

    return DOEModel(
        seed=normalized_seed,
        model_type=model_type,
        intercept=intercept,
        b_a=linear_coeffs['A'],
        b_b=linear_coeffs['B'],
        b_c=linear_coeffs['C'],
        b_d=linear_coeffs['D'],
        b_e=linear_coeffs['E'],
        b_f=linear_coeffs['F'],
        b_g=linear_coeffs['G'],
        b_aa=quad_coeffs['A'],
        b_bb=quad_coeffs['B'],
        b_cc=quad_coeffs['C'],
        b_dd=quad_coeffs['D'],
        b_ee=quad_coeffs['E'],
        b_ff=quad_coeffs['F'],
        b_gg=quad_coeffs['G'],
        b_aaa=cubic_coeffs['A'],
        b_bbb=cubic_coeffs['B'],
        b_ccc=cubic_coeffs['C'],
        b_ddd=cubic_coeffs['D'],
        b_eee=cubic_coeffs['E'],
        b_fff=cubic_coeffs['F'],
        b_ggg=cubic_coeffs['G'],
        b_ab=b_ab,
        b_aab=b_aab,
        b_abb=b_abb,
        peak1_center_x=peak1_center_x,
        peak1_center_y=peak1_center_y,
        peak1_amplitude=peak1_amplitude,
        peak1_variance=peak1_variance,
        peak2_center_x=peak2_center_x,
        peak2_center_y=peak2_center_y,
        peak2_amplitude=peak2_amplitude,
        peak2_variance=peak2_variance,
        sig_factors=sig_factors,
        noise_std=noise_std,
    )


def calculate_response(factors: Dict[str, float], model: DOEModel) -> float:
    """Compute response using either Gaussian peaks or polynomial model."""
    a = float(factors.get("A", 0.0))
    b = float(factors.get("B", 0.0))
    c = float(factors.get("C", 0.0))
    d = float(factors.get("D", 0.0))
    e = float(factors.get("E", 0.0))
    f = float(factors.get("F", 0.0))
    g = float(factors.get("G", 0.0))

    sig1, sig2 = model.sig_factors
    sig1_val = locals()[sig1.lower()]
    sig2_val = locals()[sig2.lower()]

    # Linear terms (noise from all factors)
    response = (
        model.intercept
        + model.b_a * a
        + model.b_b * b
        + model.b_c * c
        + model.b_d * d
        + model.b_e * e
        + model.b_f * f
        + model.b_g * g
    )

    if model.model_type == "gaussian":
        # Gaussian peaks for significant factors
        dist1_sq = ((sig1_val - model.peak1_center_x)**2 + 
                    (sig2_val - model.peak1_center_y)**2)
        peak1 = model.peak1_amplitude * np.exp(-model.peak1_variance * dist1_sq / 2500)

        dist2_sq = ((sig1_val - model.peak2_center_x)**2 + 
                    (sig2_val - model.peak2_center_y)**2)
        peak2 = model.peak2_amplitude * np.exp(-model.peak2_variance * dist2_sq / 2500)

        response += peak1 + peak2

    else:  # polynomial
        # Polynomial terms for all factors
        response += (
            model.b_aa * (a ** 2)
            + model.b_bb * (b ** 2)
            + model.b_cc * (c ** 2)
            + model.b_dd * (d ** 2)
            + model.b_ee * (e ** 2)
            + model.b_ff * (f ** 2)
            + model.b_gg * (g ** 2)
            + model.b_aaa * (a ** 3)
            + model.b_bbb * (b ** 3)
            + model.b_ccc * (c ** 3)
            + model.b_ddd * (d ** 3)
            + model.b_eee * (e ** 3)
            + model.b_fff * (f ** 3)
            + model.b_ggg * (g ** 3)
            + model.b_ab * (sig1_val * sig2_val)
            + model.b_aab * (sig1_val ** 2 * sig2_val)
            + model.b_abb * (sig1_val * sig2_val ** 2)
        )

    if model.noise_std > 0:
        response += np.random.default_rng(model.seed).normal(0, model.noise_std)

    return float(response)


def model_equation(model: DOEModel) -> str:
    """Return a human-readable equation string."""
    sig1, sig2 = model.sig_factors
    terms = [f"{model.intercept:.3f}"]
    
    # Linear terms
    factors = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for f in factors:
        coef = getattr(model, f'b_{f.lower()}')
        if abs(coef) > 0.0001:
            terms.append(f"{coef:.4f}*{f}")
    
    if model.model_type == "gaussian":
        # Gaussian peaks
        terms.append(f"+ {model.peak1_amplitude:.2f}*exp(-{model.peak1_variance:.2f}*((({sig1}-{model.peak1_center_x:.1f})^2 + ({sig2}-{model.peak1_center_y:.1f})^2)/2500))")
        terms.append(f"+ {model.peak2_amplitude:.2f}*exp(-{model.peak2_variance:.2f}*((({sig1}-{model.peak2_center_x:.1f})^2 + ({sig2}-{model.peak2_center_y:.1f})^2)/2500))")
        return "Y = " + " ".join(terms)
    
    else:  # polynomial
        # Quadratic terms
        for f in factors:
            coef = getattr(model, f'b_{f.lower()}{f.lower()}')
            if abs(coef) > 0.0001:
                terms.append(f"{coef:.5f}*{f}^2")
        
        # Cubic terms
        for f in factors:
            coef = getattr(model, f'b_{f.lower()}{f.lower()}{f.lower()}')
            if abs(coef) > 0.00001:
                terms.append(f"{coef:.5f}*{f}^3")
        
        # Interaction
        if abs(model.b_ab) > 0.0001:
            terms.append(f"{model.b_ab:.5f}*{sig1}*{sig2}")
        
        # Cross-quadratic
        if abs(model.b_aab) > 0.00001:
            terms.append(f"{model.b_aab:.5f}*{sig1}^2*{sig2}")
        if abs(model.b_abb) > 0.00001:
            terms.append(f"{model.b_abb:.5f}*{sig1}*{sig2}^2")
        
        return "Y = " + " + ".join(terms)


def compute_anova(factor_table: Dict[str, float], response: float) -> Dict[str, float]:
    """Compute p-values for factors from regression."""
    df = factor_table
    y = np.array(df["Response"])
    X = np.column_stack([
        np.ones_like(y),
        np.array(df["A"]),
        np.array(df["B"]),
    ])
    model = sm.OLS(y, X).fit()
    return {
        "p_A": float(model.pvalues[1]),
        "p_B": float(model.pvalues[2]),
    }
