import re
import toml

# Bump version in setup.cfg
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

# Bump version in pyproject.toml
def bump_version(version_str):
    major, minor, patch = map(int, version_str.split('.'))
    return f"{major}.{minor}.{patch + 1}"

with open("pyproject.toml", 'r') as file:
    content = toml.load(file)

old_version = content['project']['version']
content['project']['version'] = bump_version(old_version)

with open("pyproject.toml", 'w') as file:
    toml.dump(content, file)
