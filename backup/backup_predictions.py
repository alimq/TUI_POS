import subprocess
from pathlib import Path

base = Path(__file__).resolve().parent

rmd = base / "plots.Rmd"
out_dir = base / "output"
out_dir.mkdir(exist_ok=True)

expr = f"""
    rmarkdown::render(
    input = {str(rmd)!r},
    output_format = "pdf_document",
    output_dir = {str(out_dir)!r}
)
"""

result = subprocess.run(
    ["Rscript", "-e", expr],
    text=True,
    capture_output=True
)

if result.returncode != 0:
    print(result.stderr)
    raise RuntimeError("" \
    "Knitting failed.")

while True:
    ans = input("" \
    "Output current prediction? (y - yes, n - exit): ")
    if ans == 'y':
        print(result.stdout)
    else:
        break