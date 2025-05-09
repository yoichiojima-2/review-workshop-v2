import json
from pprint import pprint
from pathlib import Path


def main():
    with Path("KPI.ipynb").open() as f:
        data = json.load(f)

    md = ""
    for cell in data["cells"]:
        if cell["cell_type"] == "markdown":
            md += "".join(cell["source"]) + "\n\n"
        elif cell["cell_type"] == "code":
            md += f"```python\n{''.join(cell['source'])}\n```\n\n"
    
    Path("KPI.md").write_text(md)
    print("Markdown file created successfully.")


if __name__ == "__main__":
    main()
