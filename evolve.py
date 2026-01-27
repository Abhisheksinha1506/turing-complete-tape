from pathlib import Path
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

    # Update README with latest status
    readme_path = os.path.join(base_dir, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            content = f.read()
        
        start_marker = "<!-- LATEST_STATUS_START -->"
        end_marker = "<!-- LATEST_STATUS_END -->"
        
        if start_marker in content and end_marker in content:
            parts = content.split(start_marker)
            prefix = parts[0] + start_marker
            suffix = end_marker + parts[1].split(end_marker)[1]
            new_content = f"{prefix}\n> {summary}\n{suffix}"
            
            with open(readme_path, 'w') as f:
                f.write(new_content)


def update_readme(summary):
    readme_path = Path("README.md")
    if not readme_path.exists(): return
    try:
        content = readme_path.read_text()
        start = "<!-- LATEST_STATUS_START -->"
        end = "<!-- LATEST_STATUS_END -->"
        if start not in content or end not in content: return
        parts = content.split(start)
        suffix_parts = parts[1].split(end)
        prefix = parts[0] + start
        suffix = end + suffix_parts[1]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_inner = f"
*{summary} ({timestamp})*
"
        readme_path.write_text(prefix + new_inner + suffix)
    except Exception as e: print(f"⚠️ README Update Failed: {e}")
if __name__ == "__main__":
    evolve()
