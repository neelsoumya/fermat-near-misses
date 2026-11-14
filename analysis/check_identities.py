"""Verify the n=3 near-miss family and the arithmetic-progression reduction."""
from sympy import symbols, expand

t = symbols("t")
print("x^3 + y^3 - z^3 =", expand((9*t**4 - 3*t)**3 + (9*t**3 - 1)**3 - (9*t**4)**3))
assert all((9*s**4 - 3*s)**3 + (9*s**3 - 1)**3 == (9*s**4)**3 - 1 for s in range(1, 3001))
print("n=3 family verified exactly for t = 1..3000")

sol = [(n, y) for n in range(2, 60) for y in range(2, 3000)
       if (y - 1)**n + y**n == (y + 1)**n]
print("AP (d=1) solutions, n<60, y<3000:", sol)
