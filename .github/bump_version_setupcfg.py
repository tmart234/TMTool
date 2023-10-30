# bump_version_setupcfg.py

import re

with open("setup.cfg", "r") as f:
    content = f.read()

# Extract version from setup.cfg
version = re.search(r'version\s*=\s*(.+)', content).group(1)
major, minor, patch = map(int, version.split("."))

# Bump patch version
new_version = f"{major}.{minor}.{patch + 1}"

# Replace in content
updated_content = content.replace(f'version = {version}', f'version = {new_version}')

with open("setup.cfg", "w") as f:
    f.write(updated_content)
