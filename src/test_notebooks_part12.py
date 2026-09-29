import glob
import json
import os
import subprocess
import tempfile

notebooks = sorted(glob.glob("notebooks/part-12/*.ipynb"))
print(f"Found {len(notebooks)} notebooks in part-12. Testing execution with Python 3.10...")

passed = 0
failed = 0

for nb_path in notebooks:
    fname = os.path.basename(nb_path)
    print(f"\n--- Testing: {fname} ---")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    code = "import matplotlib\nmatplotlib.use('Agg')\n\n"
    code += "\n\n".join(["".join(c["source"]) for c in code_cells])
    
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tf:
        tf.write(code)
        tf_name = tf.name
        
    try:
        res = subprocess.run(["py", "-3.10", tf_name], capture_output=True, text=True, timeout=90)
        if res.returncode == 0:
            print(f"[PASS] {fname}")
            passed += 1
        else:
            print(f"[FAIL] {fname}")
            print("STDERR:\n", res.stderr[-500:] if res.stderr else "None")
            print("STDOUT:\n", res.stdout[-300:] if res.stdout else "None")
            failed += 1
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {fname} exceeded timeout!")
        failed += 1
    finally:
        if os.path.exists(tf_name):
            os.remove(tf_name)

print("\n==========================================")
print(f"SUMMARY: {passed} PASSED, {failed} FAILED")
print("==========================================")
