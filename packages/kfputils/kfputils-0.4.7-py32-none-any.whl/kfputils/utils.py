"""Utils."""

from yaml import safe_load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper  # noqa:F401
import pathlib
from typing import Dict

PARAMS_FILE = "params.yaml"


def read_params(params_file: str) -> Dict:
    """Read pipeline arguments from a yaml file."""
    data = safe_load(pathlib.Path(params_file).read_text())
    return data
    # return data["args"]


def serialise_params(data: Dict) -> str:
    """Serialise params to format required by $ kfp run submit."""
    out = ""
    for k in data:
        out += f"{k}={data[k]} "
    return out.rstrip()


def extract_write_spec(in_file: str, out_file: str):
    """Extract spec from manifest and write to file."""
    data = safe_load(pathlib.Path(in_file))
    with open(out_file, "w+") as f:
        dump(data["spec"], f, default_flow_style=False)
