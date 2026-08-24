import numpy as np

def weighted_background(filepath):
    data = np.loadtxt(filepath, comments="#")
    qz, intensity, uncertainty = data[:, 0], data[:, 1], data[:, 2]

    weights = 1.0 / uncertainty**2
    rate = np.sum(intensity * weights) / np.sum(weights)
    rate_unc = 1.0 / np.sqrt(np.sum(weights))

    return rate, rate_unc

for label, path in [("background+", "gans_background_plus.refl"),
    ("background-", "gans_background_minus.refl"),
    ]:
    rate, unc = weighted_background(path)
    if "+" in label:
        r_plus, u_plus = rate, unc
    else:
        r_minus, u_minus = rate, unc
    
    print(f"{label}: {rate:.6e} +/- {unc:.6e} counts/s")

w_plus = 1.0 / u_plus**2
w_minus = 1.0 / u_minus**2

combined_rate = (r_plus * w_plus + r_minus * w_minus) / (w_plus + w_minus)
combined_unc = 1.0 / np.sqrt(w_plus + w_minus)

diff_sigma = abs(r_plus - r_minus) / np.sqrt(u_plus**2 + u_minus**2)

print(f"difference in combined sigma: {diff_sigma:.3f}")
print(f"combined background rate: {combined_rate:.6e} +/- {combined_unc:.6e} counts/s")