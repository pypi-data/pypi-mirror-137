import sys
import json
import os.path as osp
sys.path.insert(0, osp.abspath(osp.join(osp.dirname(__file__), '..')))
from co2mpas_dice._version import __jet_version__

fpath = osp.join(osp.dirname(__file__), 'package.json')
with open(fpath) as f:
    package = json.load(f)
package['version'] = __jet_version__
with open(fpath, 'w') as f:
    json.dump(package, f, indent=2)
