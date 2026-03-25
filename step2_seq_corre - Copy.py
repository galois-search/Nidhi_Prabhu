import itertools
import math

# ------------------ File Paths ------------------
input_file = "D:\\Dileep\\NIDHI_V02\\outputdemo.txt"  # coefficients + seeds
output_file = "D:\\Dileep\\NIDHI_V02\\correlation1_output.txt"


# ------------------ Helper Functions ------------------

# ----- Read sequences for correlation -----
def read_sequences(filename):
    sequences = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  # ignore empty lines
                sequences.append(line)
    if not sequences:
        print(f"No sequences found in {filename}.")
        exit()
    return sequences


def detect_type(sequences):
    for seq in sequences:
        for d in seq:
            if d not in ['0', '1']:
                return "z4"
    return "binary"


# ---------- Binary Correlation ----------
def binary_correlation(seq1, seq2):
    agreement = sum(1 for a, b in zip(seq1, seq2) if a == b)
    disagreement = len(seq1) - agreement
    return agreement - disagreement


def circular_shift(seq, k):
    return seq[k:] + seq[:k]


# ---------- Z4 Helpers ----------
def simplify_complex_powers(powers):
    results = {"real": 0, "imaginary": 0}
    for p in powers:
        remainder = p % 4
        if remainder == 0:
            results["real"] += 1
        elif remainder == 1:
            results["imaginary"] += 1
        elif remainder == 2:
            results["real"] -= 1
        elif remainder == 3:
            results["imaginary"] -= 1
    r = results["real"]
    im = results["imaginary"]
    output = []
    if r != 0: output.append(f"{r}")
    if im != 0: output.append(f"{im}i")
    return " + ".join(output) if output else "0"


# ---------- Z4 Cross Correlation (Shift 0 Only) ----------
def z4_cross_correlation_shift0(seq1, seq2):
    """Digit-wise subtraction modulo 4, powers of i, only shift 0"""
    diff = [(int(a) - int(b)) % 4 for a, b in zip(seq1, seq2)]
    result = simplify_complex_powers(diff)
    cleaned = result.replace('i', 'j').replace(' ', '').replace('+-', '-').replace('--', '+')
    magnitude = abs(complex(cleaned))
    return [(0, result, magnitude)], magnitude


# ---------- Auto Correlation ----------
def auto_correlation(sequences, mode):
    results = []
    for idx, seq in enumerate(sequences):
        results.append(f"\nSequence {idx + 1}: {seq}")
        if mode == "binary":
            n = len(seq)
            for shift in range(1, n):
                shifted = circular_shift(seq, shift)
                corr = binary_correlation(seq, shifted)
                results.append(f"Shift {shift} → {corr}")
        else:  # z4 auto stays unchanged
            powers = [int(d) for d in seq]
            result = simplify_complex_powers(powers)
            cleaned = result.replace('i', 'j').replace(' ', '').replace('+-', '-').replace('--', '+')
            magnitude = abs(complex(cleaned))
            results.append(f"Auto-correlation → {result} | magnitude={magnitude}")
            results.append(f"Peak auto-correlation magnitude: {magnitude}")
    return results


# ---------- Cross Correlation ----------
def cross_correlation(sequences, mode):
    results = []
    for (i, seq1), (j, seq2) in itertools.combinations(enumerate(sequences), 2):
        results.append(f"\nSequence {i + 1} vs Sequence {j + 1}")
        if mode == "binary":
            n = len(seq1)
            peak_corr = None
            for shift in range(n):
                shifted_seq2 = circular_shift(seq2, shift)
                corr = binary_correlation(seq1, shifted_seq2)
                if peak_corr is None or abs(corr) > abs(peak_corr):
                    peak_corr = corr
                results.append(f"Shift {shift} → {corr}")
            results.append(f"Peak cross-correlation magnitude: {abs(peak_corr)}")
        else:  # z4 modified cross, shift 0 only
            z4_results, peak_mag = z4_cross_correlation_shift0(seq1, seq2)
            for shift, res, mag in z4_results:
                results.append(f"Shift {shift} → {res} | magnitude={mag}")
            results.append(f"Peak cross-correlation magnitude: {peak_mag}")
    return results


# ---------- LFSR Sequence Generator (Fixed Length 2^m - 1) ----------
def generate_lfsr_sequences_fixed_length(input_file):
    """
    Reads LFSR polynomial coefficients (first line) and seeds (remaining lines),
    generates sequences of length 2^m - 1 (maximal-length sequence) for each seed.
    Works modulo 4.
    """
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Read polynomial coefficients
    coeffs = list(map(int, lines[0].split()))
    m = len(coeffs) - 1  # polynomial degree
    mod = 4

    # Prepare RHS coefficients for feedback
    rhs_coeffs = coeffs[1:]  # exclude leading 1
    rhs_mod_coeffs = [(-c) % mod for c in rhs_coeffs]

    # Maximal sequence length for LFSR
    seq_length = 2 ** m - 1

    # Read seeds
    seeds = []
    for line in lines[1:]:
        seed = [int(x) for x in line]
        if len(seed) != m:
            print(f"Skipping invalid seed (length mismatch): {line}")
            continue
        seeds.append(seed)

    # Generate sequences
    sequences = []
    for seed in seeds:
        state = seed[::-1]  # reverse seed for feedback calculation
        sequence = seed.copy()  # initial sequence includes seed
        for _ in range(seq_length - len(seed)):
            feedback = sum(rhs_mod_coeffs[i] * state[i] for i in range(len(rhs_mod_coeffs))) % mod
            sequence.append(feedback)
            state = [feedback] + state[:-1]
        sequences.append(''.join(str(x) for x in sequence))

    return sequences


# -------------------- MAIN --------------------
def main():
    # ---- Step 1: Generate sequences from LFSR ----
    sequences = generate_lfsr_sequences_fixed_length(input_file)
    print(f"Generated {len(sequences)} LFSR sequences of length {len(sequences[0])} from seeds.")

    # ---- Step 2: Detect type for correlation ----
    mode = detect_type(sequences)
    print(f"Detected sequence type: {mode}")

    # ---- Step 3: Choose correlation ----
    print("\nChoose correlation option")
    print("1 → Auto correlation")
    print("2 → Cross correlation")
    print("3 → Both")
    choice = input("Enter choice: ")

    output_lines = []
    output_lines.append(f"Detected sequence type: {mode}\n")

    if choice == '1' or choice == '3':
        output_lines.append("AUTO CORRELATION")
        output_lines.extend(auto_correlation(sequences, mode))

    if choice == '2' or choice == '3':
        output_lines.append("\nCROSS CORRELATION")
        output_lines.extend(cross_correlation(sequences, mode))

    # Write results safely in UTF-8
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in output_lines:
            f.write(line + "\n")

    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    main()