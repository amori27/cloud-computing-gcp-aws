"""Cloud Utilities Module.

This module provides utility functions for cloud operations
including storage, compute, and networking.
"""

import json
from typing import Any


def get_gcp_storage_url(bucket: str, object_name: str) -> str:
    """Generate a GCS storage URL.

    Args:
        bucket: GCS bucket name.
        object_name: Object name in bucket.

    Returns:
        Full GCS URL.
    """
    return f"gs://{bucket}/{object_name}"


def get_s3_url(bucket: str, object_name: str, region: str = "us-east-1") -> str:
    """Generate an S3 storage URL.

    Args:
        bucket: S3 bucket name.
        object_name: Object name in bucket.
        region: AWS region.

    Returns:
        Full S3 URL.
    """
    return f"https://{bucket}.s3.{region}.amazonaws.com/{object_name}"


def format_cloudwatch_log(stream_name: str, log_data: str) -> dict[str, Any]:
    """Format log data for CloudWatch.

    Args:
        stream_name: Log stream name.
        log_data: Log message.

    Returns:
        Formatted log entry.
    """
    return {
        "logStreamName": stream_name,
        "logData": log_data,
        "timestamp": None
    }


def parse_gcp_service_account(path: str) -> dict[str, str]:
    """Parse GCP service account JSON file.

    Args:
        path: Path to service account JSON.

    Returns:
        Service account info.
    """
    with open(path, 'r') as f:
        data = json.load(f)

    return {
        "type": data.get("type"),
        "project_id": data.get("project_id"),
        "private_key_id": data.get("private_key_id"),
        "client_email": data.get("client_email")
    }


def generate_vm_config(
    name: str,
    machine_type: str,
    zone: str,
    disk_size: int = 100
) -> dict[str, Any]:
    """Generate VM configuration for GCP or AWS.

    Args:
        name: Instance name.
        machine_type: Machine type.
        zone: Availability zone.
        disk_size: Boot disk size in GB.

    Returns:
        VM configuration dictionary.
    """
    return {
        "name": name,
        "machine_type": machine_type,
        "zone": zone,
        "disk": {
            "size_gb": disk_size,
            "type": "pd-standard"
        },
        "network": {
            "interface": "NIC0",
            "network": "default"
        }
    }


def calculate_cloud_cost(
    instance_count: int,
    machine_type: str,
    hours_per_month: float = 730
) -> dict[str, float]:
    """Estimate cloud infrastructure costs.

    Args:
        instance_count: Number of instances.
        machine_type: Instance type.
        hours_per_month: Hours in a month.

    Returns:
        Cost breakdown.
    """
    base_costs = {
        "small": 0.05,
        "medium": 0.10,
        "large": 0.20
    }

    size = "small"
    if "xlarge" in machine_type or "2xlarge" in machine_type:
        size = "large"
    elif "large" in machine_type or "xlarge" in machine_type:
        size = "medium"

    hourly_rate = base_costs.get(size, 0.10)
    monthly_compute = instance_count * hourly_rate * hours_per_month

    storage_cost = instance_count * 10 * 0.10
    network_cost = instance_count * 5 * 0.10

    return {
        "compute_cost": round(monthly_compute, 2),
        "storage_cost": round(storage_cost, 2),
        "network_cost": round(network_cost, 2),
        "total_cost": round(monthly_compute + storage_cost + network_cost, 2)
    }
