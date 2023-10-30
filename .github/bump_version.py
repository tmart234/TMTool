import re
import toml

def get_version_from_cfg(content):
    return re.search(r'version\s*=\s*(.+)', content).group(1)

def bump_version(version_str):
    major, minor, patch = map(int, version_str.split('.'))
    return f"{major}.{minor}.{patch + 1}"

# Extract version from setup.cfg
with open("setup.cfg", "r") as f:
    content = f.read()
    cfg_version = get_version_from_cfg(content)

# Extract version from pyproject.toml
with open("pyproject.toml", 'r') as file:
    toml_content = toml.load(file)
    toml_version = toml_content['project']['version']

# Compare versions and pick the higher version
cfg_version_tuple = tuple(map(int, cfg_version.split('.')))
toml_version_tuple = tuple(map(int, toml_version.split('.')))

if cfg_version_tuple > toml_version_tuple:
    higher_version = cfg_version
else:
    higher_version = toml_version

# Bump the higher version
bumped_version = bump_version(higher_version)

# Update setup.cfg
updated_content = content.replace(f'version = {cfg_version}', f'version = {bumped_version}')
with open("setup.cfg", "w") as f:
    f.write(updated_content)

# Update pyproject.toml
toml_content['project']['version'] = bumped_version
with open("pyproject.toml", 'w') as file:
    toml.dump(toml_content, file)
