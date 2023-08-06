from requirements import REQUIREMENTS

with open("requirements.txt", "w") as f:
    for requirement in REQUIREMENTS:
        f.writelines(f"{requirement}\n")
