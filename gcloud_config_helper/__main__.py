"""
demonstration usage
"""
__author__ = """Mark van Holsteijn"""
__email__ = "markvanholsteijn@binx.io"
__version__ = "0.1.0"

import argparse
import googleapiclient
import gcloud_config_helper
from google.cloud import compute_v1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="demonstrate gcloud-config-helper usage"
    )
    parser.add_argument("--name", default="", help="of the gcloud configuration to use")
    parser.add_argument(
        "--print-access-token", action=argparse.BooleanOptionalAction, help=" on stdout"
    )
    parser.add_argument(
        "--list-instances", action=argparse.BooleanOptionalAction, help=" on stdout"
    )

    if not gcloud_config_helper.on_path():
        parser.error("gcloud was not found on $PATH.")
    args = parser.parse_args()
    credentials = gcloud_config_helper.GCloudCredentials(args.name)
    print(f"active configuration name is {credentials.name}")
    print(f"configured project is {credentials.project}")
    if args.print_access_token:
        print(f"token is {credentials.token}")
    if credentials.expired:
        print(f"token has expired")
    else:
        print(f"token must be refreshed at {credentials.expiry}+00:00")

    if args.list_instances:
        try:
            from google.cloud import compute_v1

            credentials, project = gcloud_config_helper.default()
            c = compute_v1.InstancesClient(credentials=credentials)
            for zone, instances in c.aggregated_list(request={"project": project}):
                for instance in instances.instances:
                    print(f"found {instance.name} in zone {zone}")

        except ModuleNotFoundError:
            print("please run 'pip3 install google-cloud-compute' first")
