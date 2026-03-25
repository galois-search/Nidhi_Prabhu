from itertools import product
import os
import random


# -----------------------------
# 1. Generate all non-zero seeds
# -----------------------------
def generate_nonzero_seeds(degree, base):
    seeds = list(product(range(base), repeat=degree))
    return [s for s in seeds if any(c != 0 for c in s)]


# -----------------------------
# 2. Random selection of seeds
# -----------------------------
def select_random_seeds(seeds, subset_size):
    if subset_size > len(seeds):
        raise ValueError("Subset size cannot exceed total number of seeds")

    return random.sample(seeds, subset_size)


# -----------------------------
# 3. Main Program
# -----------------------------
if __name__ == "__main__":

    degree = int(input("Enter polynomial degree: "))
    base = int(input("Enter ring base (e.g., 4 for Z4): "))
    subset_size = int(input("Enter size of seed set: "))

    all_seeds = generate_nonzero_seeds(degree, base)
    selected_seeds = select_random_seeds(all_seeds, subset_size)

    # Desktop path
    #desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "outputdemo.txt")
    desktop_path = "D:\\Dileep\\NIDHI_V02\\outputdemo.txt"

    with open(desktop_path, "w") as f:
        for s in selected_seeds:
            f.write("".join(str(x) for x in s) + "\n")

    print(f"\nSeeds saved to: {desktop_path}")