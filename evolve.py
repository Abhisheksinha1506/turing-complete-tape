import os
import datetime

def rule110(l, c, r):
    # Rule 110: 01101110 (binary 110)
    # 111 -> 0
    # 110 -> 1
    # 101 -> 1
    # 100 -> 0
    # 011 -> 1
    # 010 -> 1
    # 001 -> 1
    # 000 -> 0
    # Table based logic
    neighborhood = f"{l}{c}{r}"
    rules = {
        "111": 0,
        "110": 1,
        "101": 1,
        "100": 0,
        "011": 1,
        "010": 1,
        "001": 1,
        "000": 0
    }
    return rules[neighborhood]

def evolve():
    base_dir = os.path.dirname(__file__)
    tape_path = os.path.join(base_dir, 'tape.txt')
    evolution_path = os.path.join(base_dir, 'evolution.md')
    
    if not os.path.exists(tape_path):
        row = '0' * 50 + '1' + '0' * 50
    else:
        with open(tape_path, 'r') as f:
            row = f.read().strip()

    new_row_list = []
    for i in range(len(row)):
        l = int(row[i - 1]) if i > 0 else 0
        c = int(row[i])
        r = int(row[i + 1]) if i < len(row) - 1 else 0
        
        new_val = rule110(l, c, r)
        new_row_list.append(str(new_val))
    
    new_row = "".join(new_row_list)
    
    with open(tape_path, 'w') as f:
        f.write(new_row)
        
    ascii_row = new_row.replace('1', '█').replace('0', ' ')
    date_str = datetime.date.today().isoformat()
    
    gen_count = 0
    if os.path.exists(evolution_path):
        with open(evolution_path, 'r') as f:
            for line in f:
                if line.startswith('|') and not line.startswith('| Generation') and not line.startswith('|------------'):
                    gen_count += 1
    
    with open(evolution_path, 'a') as f:
        f.write(f"| {gen_count + 1} | {date_str} | `{ascii_row}` |\n")

    # Generate human summary
    active_cells = new_row.count('1')
    summary = f"The universal calculation has advanced to Generation {gen_count + 1}. "
    summary += f"The tape now contains {active_cells} active computational units. "
    summary += "Complex structures called 'gliders' are interacting across the tape, processing information in a Turing-complete manner."

    with open(os.path.join(base_dir, 'summary.txt'), 'w') as f:
        f.write(summary)

if __name__ == "__main__":
    evolve()
