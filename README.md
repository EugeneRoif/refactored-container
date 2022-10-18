# refactored-container
EXPERIMENTAL - Auto patching for Containers

*Use Trivy to patch containers:*
---------------------------------
* First run the trivy to export a report: ```trivy image --ignore-unfixed --quiet --security-checks vuln nginx:latest -f json | tee trivy_report```
* Exectute the python script: ```python3 create_dockerfile.py```
