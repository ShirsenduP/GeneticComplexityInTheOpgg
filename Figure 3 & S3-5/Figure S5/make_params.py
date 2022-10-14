from itertools import product

n_vals = [2, 3, 4, 5]
norms = ["Defector", "Loner", "Neither", "Both"]
p_vals = [*range(1, 13)]
iters = [*range(10)]

params_list = []

for i, (_, n, p, norm) in enumerate(product(iters, n_vals, p_vals, norms), start=1):
    s = f"{i:04d} {n} {p} {norm}"
    params_list.append(s)

params_str = "\n".join(params_list)

with open("params.txt", "w") as f:
    f.write(params_str)
