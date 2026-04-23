import itertools
import os


def read_input(filename):
    if not os.path.exists(filename):
        print(f"Error: File not found at {filename}")
        return None, None, None

    try:
        with open(filename, 'r') as file:
            content = [line.strip() for line in file if line.strip()]

        if len(content) < 3:
            return None, None, None

        degree = int(content[0])
        raw_coeffs = content[1].replace(',', ' ').split()

        if len(raw_coeffs) == 1 and len(raw_coeffs[0]) > 1:
            full_coeffs = [int(d) % 4 for d in raw_coeffs[0]]
        else:
            full_coeffs = [int(float(c)) % 4 for c in raw_coeffs]

        steps = int(content[2])
        return degree, full_coeffs, steps

    except Exception as e:
        print(f"Error parsing file: {e}")
        return None, None, None


def is_unit(state):
    # Faster check: any odd value → unit
    return any(x & 1 for x in state)


def next_state(state, coeffs):
    # Compute feedback
    total = 0
    for c, s in zip(coeffs, state):
        total += c * s
    new_digit = (-total) & 3  # faster mod 4

    # Shift
    return (new_digit,) + state[:-1]


def get_orbit(start, coeffs, max_steps, global_seen):
    """
    Returns:
        cycle_states, bit_string, visited_path
    """
    visited_local = {}
    path = []
    bits = []

    current = start

    for step in range(max_steps):
        if current in global_seen:
            return None, None, path

        if current in visited_local:
            start_idx = visited_local[current]
            cycle = path[start_idx:]
            cycle_bits = bits[start_idx:]
            return cycle, "".join(map(str, cycle_bits)), path

        visited_local[current] = step
        path.append(current)
        bits.append(current[-1])

        current = next_state(current, coeffs)

    return None, None, path


def main():
    input_path = r"D:\Dileep\NIDHI_V02\24input.txt"
    output_folder = r"D:\Dileep\NIDHI_V02"

    degree, full_coeffs, steps = read_input(input_path)
    if degree is None:
        return

    output_filename = f"degree{degree}_optimized.txt"
    output_path = os.path.join(output_folder, output_filename)

    rhs_coeffs = full_coeffs[1:]
    rhs_coeffs += [0] * (degree - len(rhs_coeffs))

    global_seen = set()
    seed_count = 0
    output_lines = []

    print(f"\n--- Optimized Orbit Analysis (Degree {degree}) ---")

    total_states = 4 ** degree
    checked = 0

    for state in itertools.product(range(4), repeat=degree):
        checked += 1

        if checked % 50000 == 0:
            print(f"Checked {checked}/{total_states} states...")

        if state in global_seen:
            continue

        if not is_unit(state):
            global_seen.add(state)
            continue

        cycle, bit_str, path = get_orbit(state, rhs_coeffs, steps, global_seen)

        # Mark ALL visited states (huge speed gain)
        for s in path:
            global_seen.add(s)

        if cycle:
            seed_count += 1
            primary_seed = "".join(map(str, cycle[0]))
            period = len(cycle)

            output_lines.append(
                f"Orbit #{seed_count} | Seed: {primary_seed} | Period: {period}"
            )
            output_lines.append(f"Seq: {bit_str[:100]}...")
            output_lines.append("-" * 40)

            if seed_count % 5 == 0:
                print(f"Found {seed_count} cycles so far...")

    # Save results
    try:
        with open(output_path, 'w') as f:
            f.write(f"Results for Degree {degree}\n")
            f.write(f"Total Cycles: {seed_count}\n\n")
            f.write("\n".join(output_lines))

        print(f"\n✅ Done! Found {seed_count} cycles.")
        print(f"Saved to: {output_path}")

    except Exception as e:
        print(f"Error saving file: {e}")


if __name__ == "__main__":
    main()