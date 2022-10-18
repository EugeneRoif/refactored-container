import json
import sys

with open("trivy_report", "r") as fp:
    f = fp.read()

report = json.loads(f)
if "Vulnerabilites" not in report["Results"]:
    print(f"No Vulnerabilites found to fix")
    sys.exit(0)

with open("Dockerfile", "w") as fp:
    fp.write(f"FROM {report['ArtifactName']}\n")

for i in report["Results"]:
    scan_type = i["Type"]
    pkg = set()

    for scan_class in i["Vulnerabilities"]:
        if scan_class["FixedVersion"]:
            pkg.add(f"{scan_class['PkgName']}:{scan_class['FixedVersion']}")

    if scan_type == "ubuntu":
        with open("Dockerfile", "a") as fp:
            fp.write("apt-get update && apt-get install -y \\\n")
            for i in pkg:
                fp.write(f"\t{i} && \\\n")
            fp.write("\trm -rf /var/lib/apt/lists/*\n")

if len(open("Dockerfile", "r").readlines()) == 1:
    print(f"No Volnerabities found to fix")
    sys.exit(0)

print(f"Created new Dockerfile, please rebuild")
sys.exit(1)
