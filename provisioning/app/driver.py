import argparse
import logging
import uuid
import os

from shutil import rmtree

from app.common.bbox import BBOX
from app.common.http_retriever import check_exists
from app.profiles import xyz, topo, xyzsummer, xyzwinter
from app.record.run_recorder import record_run, has_prior_run
from app.sources.xyz_service import build_exists_check_requests as xyz_check_builder
from app.common.util import (
    get_result_path,
    get_run_data_path,
    configure_logging,
    remove_intermediaries,
)


def provision(bbox: BBOX, profile_name: str, xyz_url: str) -> None:
    bbox_repeat_if_exists = int(os.environ.get("BBOX_REPEAT_IF_EXISTS", 0)) == 1
    bbox_exists = has_prior_run(get_result_path((profile_name,)), bbox)
    if bbox_exists and not bbox_repeat_if_exists:
        logging.info(
            f"Skipping {profile_name} {bbox.min_x},{bbox.min_y} {bbox.max_x},{bbox.max_y} as it already exists"
        )
        return

    run_id = str(uuid.uuid4())
    profiles = {
        profile.NAME: {
            "execute": profile.execute,
            "zoom_min": profile.ZOOM_MIN,
            "zoom_max": profile.ZOOM_MAX,
            "format": profile.OUTPUT_FORMAT,
        }
        for profile in [xyz, topo, xyzsummer, xyzwinter]
    }
    profiles[profile_name]["execute"](bbox, run_id, {"xyz_url": xyz_url})
    logging.info("Validating result")
    check_exists(
        xyz_check_builder(
            bbox,
            "{0}/{1}/{{z}}/{{x}}/{{y}}.png".format(
                os.environ.get("HTTP_URL", "http://localhost:9000/tiles/files"),
                profile_name,
            ),
            profiles[profile_name]["zoom_min"],
            profiles[profile_name]["zoom_max"],
            "image/{0}".format(profiles[profile_name]["format"]),
        )
    )
    record_run(get_result_path((profile_name,)), bbox)
    if remove_intermediaries():
        run_dir = get_run_data_path(run_id, None)
        result_temp_dir = get_result_path((run_id,))
        if os.path.exists(run_dir):
            rmtree(run_dir)
        if os.path.exists(result_temp_dir):
            rmtree(result_temp_dir)
    logging.info("Finished")


if __name__ == "__main__":
    # has been directly invoked, likely debugging
    configure_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("min_x", type=float)
    parser.add_argument("min_y", type=float)
    parser.add_argument("max_x", type=float)
    parser.add_argument("max_y", type=float)
    parser.add_argument("profile", type=str)
    parser.add_argument("xyz_url", type=str)
    args = vars(parser.parse_args())
    provision(
        BBOX(
            **{
                key: value
                for key, value in args.items()
                if key in ("min_x", "min_y", "max_x", "max_y")
            }
        ),
        args["profile"],
        args["xyz_url"],
    )
