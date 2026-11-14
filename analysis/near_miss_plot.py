"""Plot the best near miss |x^n + y^n - z^n| at each z, absolute and relative."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 1000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT, exist_ok=True)

def iroot(s, n):
    r = int(round(s ** (1.0 / n)))
    while r ** n > s: r -= 1
    while (r + 1) ** n <= s: r += 1
    return r

data = {}
for n in (3, 4, 5, 6):
    best = {}
    for x in range(1, N + 1):
        xn = x ** n
        for y in range(x, N + 1):
            s = xn + y ** n
            z0 = iroot(s, n)
            for z in (z0, z0 + 1):
                if z <= y or z > N: continue
                a = abs(s - z ** n)
                if a == 0: continue
                if z not in best or a < best[z]: best[z] = a
    zs = np.array(sorted(best)); ab = np.array([best[z] for z in zs], dtype=float)
    data[n] = (zs, ab)

colors = {3: "tab:red", 4: "tab:blue", 5: "tab:green", 6: "tab:purple"}
fig, ax = plt.subplots(1, 2, figsize=(14, 5.5))
for n, (zs, ab) in data.items():
    rel = ab / zs.astype(float) ** n
    for a, v in zip(ax, (ab, rel)):
        a.scatter(zs, v, s=6, alpha=0.35, color=colors[n])
        a.plot(zs, np.minimum.accumulate(v), color=colors[n], lw=1.6, label=f"n={n} (record low)")
zt = [9 * t ** 4 for t in range(1, 6)]
ax[0].scatter(zt, [1] * 5, marker="*", s=140, color="gold", edgecolor="k", zorder=5, label="n=3 family: error = 1")
ax[1].scatter(zt, [1 / z ** 3 for z in zt], marker="*", s=140, color="gold", edgecolor="k", zorder=5)
for a in ax:
    a.set_xscale("log"); a.set_yscale("log"); a.grid(alpha=0.3, which="both"); a.set_xlabel("z (largest term)")
ax[0].set_ylabel("smallest |x^n + y^n - z^n| at that z"); ax[0].set_title("Absolute error of best near miss")
ax[1].set_ylabel("|x^n + y^n - z^n| / z^n"); ax[1].set_title("Relative error of best near miss")
ax[0].legend(fontsize=8, loc="upper left")
fig.suptitle(f"Fermat near misses as z grows (all x <= y < z <= {N})")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "near_miss_magnitude.png"), dpi=150)
print("wrote", os.path.join(OUT, "near_miss_magnitude.png"))
