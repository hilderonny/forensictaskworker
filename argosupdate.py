import os

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--argospath', type=str, action='store', required=True, help='Directory where the Argos Translate models are stored.')
args = parser.parse_args()

# Check write access to directories
import sys
import os

# Check existence of Argos Translate files
ARGOSPATH = args.argospath
ARGOSENDEPACKAGEPATH = os.path.join(ARGOSPATH, "packages")
if not os.access(ARGOSPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Argos Translate directory {ARGOSPATH}')
if not os.access(ARGOSENDEPACKAGEPATH, os.R_OK):
    sys.exit(f'ERROR: Cannot read Argos package directory {ARGOSENDEPACKAGEPATH}')
print(f'Using argos translate path {ARGOSPATH}')

print('Updating Argos Translate')
os.environ['ARGOS_PACKAGES_DIR'] = ARGOSENDEPACKAGEPATH

from argostranslate import package

# Update package definitions from remote
package.update_package_index()

# Load available packages from local package index
available_packages = package.get_available_packages()

# Download and install all available packages
for available_package in available_packages:
    print(f'Installing package {available_package.from_code} -  {available_package.to_code}')
    download_path = available_package.download()
    package.install_from_path(download_path)
