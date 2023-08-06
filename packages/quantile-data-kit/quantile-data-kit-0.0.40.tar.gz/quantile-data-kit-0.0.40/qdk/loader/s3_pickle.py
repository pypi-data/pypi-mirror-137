import pickle
from typing import Any

from dagster import Field, OutputDefinition, StringSource
from dagster_aws.s3 import s3_resource
from qdk.loader.base import BaseLoader


class S3PickleLoader(BaseLoader):
    output_defs = [
        OutputDefinition(Any, "result"),
    ]

    config_schema = {
        "bucket": Field(
            StringSource,
            is_required=True,
        ),
        "location": Field(
            StringSource,
            is_required=True,
        ),
    }

    required_resource_keys = {
        "s3",
    }

    @classmethod
    def load(cls, s3: s3_resource, bucket: str, location: str) -> Any:
        response = s3.get_object(Bucket=bucket, Key=location)
        body_string = response["Body"].read()
        object = pickle.loads(body_string)

        return object
