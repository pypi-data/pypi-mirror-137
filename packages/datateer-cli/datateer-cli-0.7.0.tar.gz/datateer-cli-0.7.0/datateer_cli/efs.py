import boto3


def get_efs_id_by_name(name: str):
    client = boto3.client("efs")
    list = client.describe_file_systems()["FileSystems"]
    for efs in list:
        if efs["Name"] == name:
            return efs["FileSystemId"]

    raise Exception(f"Could not find an EFS named {name}")
