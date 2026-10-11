"""Compatibility entrypoint for existing CWL's python -m app command."""

from detect_water_body.main import aoi2box as aoi2box
from detect_water_body.main import crop as crop
from detect_water_body.main import get_asset as get_asset
from detect_water_body.main import main as main
from detect_water_body.main import normalized_difference as normalized_difference
from detect_water_body.main import threshold as threshold

if __name__ == "__main__":
    main()
