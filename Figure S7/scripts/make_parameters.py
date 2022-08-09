from itertools import product

p_vals = [2, 8]
sigma_vals = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
norms = ["Defector", "Loner", "Neither", "Both"]
repeats = 20

params_string = ""
idx = 1
for _ in range(repeats):
    for p, sigma, norm in product(p_vals, sigma_vals, norms):
        line = f"{idx:04d} {p} {sigma} {norm}\n"
        params_string += line
        idx += 1


with open("K_parameters.txt", "w") as f:
    f.write(params_string)
