import os

import boto3

BUCKET_NAME = "exercise-4-backup-bucket"


def get_access_to_bucket(bucket_name):
    try:
        print("Accessing bucket %s..." % bucket_name)
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(bucket_name)
        print("Got access to bucket")
        return bucket
    except Exception as e:
        print("Can not get access to bucket: %s" % e)
        return None


def get_user_command():
    print("Input a command for the application")
    print("To get a list of objects in bucket type \"list\"")
    print("To backup a file to bucket type \"backup\"")
    print("To get all versions of a certain file \"versions\"")
    print("To download a file of a certain version type \"download\"")
    print("To delete a certain version of a file type \"delete\"")
    print("To stop the application type \"exit\"")
    return input("Type command here: ")


def print_bucket_objects(bucket):
    try:
        print("Bucket %s has the following files: " % bucket.name)
        for bucket_object in bucket.objects.all():
            print(bucket_object.key)
    except Exception as e:
        print("Failed to list files in bucket: %s" % e)


def backup_file(bucket):
    try:
        file_name = input("Provide a path to the file: ")
        if os.path.exists(file_name) and os.path.isfile(file_name):
            bucket.upload_file(file_name, os.path.basename(file_name))
        else:
            print("File %s does not exist or it is not a file" % file_name)
    except Exception as e:
        print("Failed to backup file: %s" % e)


def get_versions_of_file(bucket):
    file_name = input("Type file name: ")
    versions = list()
    for object_version in bucket.object_versions.filter(Prefix=file_name):
        versions.append({"timestamp": object_version.last_modified, "version_id": object_version.version_id, "version_obj": object_version})
    # Just in case sort by version timestamp in ascending order
    if len(versions) > 0:
        versions.sort(key=lambda x: x["timestamp"])
    return versions, file_name


def print_versions_of_file(bucket):
    file_name = None
    try:
        versions, file_name = get_versions_of_file(bucket)
        if len(versions) > 0:
            print("Versions of file %s available in bucket %s" % (file_name, bucket.name))
            for i in range(0, len(versions)):
                # Assign each version a number starting from 1
                print("Version: %s, Date: %s" % (i + 1, versions[i]["timestamp"]))
        else:
            print("File %s was not found in bucket" % file_name)
    except Exception as e:
        print("Failed to get versions of file %s: %s" % (file_name, e))


def download_file(bucket_name, file_name, version_id):
    download_to_path = input("Provide a path to which the file should be downloaded (or press Enter key to download it to the current folder): ")
    if download_to_path == "":
        download_to_path = file_name
    # Requesting a certain version of object works only via client
    response = boto3.client("s3").get_object(Bucket=bucket_name, Key=file_name, VersionId=version_id)
    with open(download_to_path, "wb") as f:
        f.write(response["Body"].read())


def download_certain_version_of_file(bucket):
    try:
        versions, file_name = get_versions_of_file(bucket)
        if len(versions) > 0:
            version_id = None
            version = input("Provide a version of file (or press Enter key to get the latest): ")
            # Version numbering starts from 1. That is why version 0 is invalid
            if version == "":
                version = len(versions)
                version_id = versions[len(versions) - 1]["version_obj"].id
            else:
                try:
                    version_number = int(version)
                    if version_number > 0:
                        version_id = versions[version_number - 1]["version_obj"].id
                    else:
                        print("Version %s is invalid" % version)
                except Exception as e:
                    print("Version %s is invalid" % version, e)
            if version_id is not None:
                download_file(bucket.name, file_name, version_id)
                print("Version %s of %s was downloaded" % (version, file_name))
        else:
            print("File %s was not found in bucket" % file_name)
    except Exception as e:
        print("Failed to download a version of a file", e)


def delete_file(bucket_name, file_name, version_id):
    # This functionality works only via client
    boto3.client("s3").delete_object(Bucket=bucket_name, Key=file_name, VersionId=version_id)


def delete_certain_version_of_file(bucket):
    try:
        versions, file_name = get_versions_of_file(bucket)
        if len(versions) > 0:
            version_id = None
            version = input("Provide a version of file (or press Enter key to get the latest): ")
            # Version numbering starts from 1. That is why version 0 is invalid
            if version == "":
                version = len(versions)
                version_id = versions[len(versions) - 1]["version_obj"].id
            else:
                try:
                    version_number = int(version)
                    if version_number > 0:
                        version_id = versions[version_number - 1]["version_obj"].id
                    else:
                        print("Version %s is invalid" % version)
                except Exception as e:
                    print("Version %s is invalid" % version, e)
            if version_id is not None:
                delete_file(bucket.name, file_name, version_id)
                print("Version %s of %s was deleted" % (version, file_name))
        else:
            print("File %s was not found in bucket" % file_name)
    except Exception as e:
        print("Failed to delete a version of a file", e)


if __name__ == "__main__":
    bucket = get_access_to_bucket(BUCKET_NAME)
    if bucket is not None:
        user_command = ""
        while user_command != "exit":
            user_command = get_user_command()
            if user_command == "list":
                print_bucket_objects(bucket)
            elif user_command == "backup":
                backup_file(bucket)
            elif user_command == "versions":
                print_versions_of_file(bucket)
            elif user_command == "download":
                download_certain_version_of_file(bucket)
            elif user_command == "delete":
                delete_certain_version_of_file(bucket)
            elif user_command == "exit":
                print("Exiting application")
            else:
                print("Unknown command \"%s\"" % user_command)
            print()
    print("Application exited")
