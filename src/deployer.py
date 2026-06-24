"""Cloud Infrastructure Deployer.

This module provides automation for deploying cloud infrastructure
across GCP and AWS using Terraform and cloud-native tools.
"""

import subprocess
from typing import Any


class CloudDeployer:
    """Handles cloud infrastructure deployment."""

    def __init__(self, provider: str = "aws"):
        """Initialize the CloudDeployer.

        Args:
            provider: Cloud provider (aws or gcp).
        """
        self.provider = provider.lower()
        self.valid_providers = ["aws", "gcp"]

        if self.provider not in self.valid_providers:
            raise ValueError(f"Provider must be one of {self.valid_providers}")

    def run_terraform(self, command: str, tf_dir: str = ".") -> subprocess.CompletedProcess:
        """Run a Terraform command.

        Args:
            command: Terraform command to run.
            tf_dir: Directory containing Terraform files.

        Returns:
            CompletedProcess object.
        """
        cmd = ["terraform", "-chdir=" + tf_dir] + command.split()
        return subprocess.run(cmd, capture_output=True, text=True)

    def init(self, tf_dir: str) -> dict[str, Any]:
        """Initialize Terraform.

        Args:
            tf_dir: Terraform directory.

        Returns:
            Initialization result.
        """
        result = self.run_terraform("init", tf_dir)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }

    def plan(self, tf_dir: str, var_file: str | None = None) -> dict[str, Any]:
        """Create a Terraform plan.

        Args:
            tf_dir: Terraform directory.
            var_file: Optional variable file.

        Returns:
            Plan result.
        """
        cmd = "plan -out=tfplan"
        if var_file:
            cmd += f" -var-file={var_file}"

        result = self.run_terraform(cmd, tf_dir)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }

    def apply(self, tf_dir: str, auto_approve: bool = True) -> dict[str, Any]:
        """Apply Terraform changes.

        Args:
            tf_dir: Terraform directory.
            auto_approve: Auto-approve changes.

        Returns:
            Apply result.
        """
        cmd = "apply"
        if auto_approve:
            cmd += " -auto-approve"
        cmd += " tfplan"

        result = self.run_terraform(cmd, tf_dir)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }

    def deploy_infrastructure(self, environment: str, tf_dir: str = ".") -> dict[str, Any]:
        """Deploy complete infrastructure.

        Args:
            environment: Environment name (dev, staging, prod).
            tf_dir: Terraform directory.

        Returns:
            Deployment result.
        """
        init_result = self.init(tf_dir)
        if not init_result["success"]:
            return init_result

        var_file = f"vars/{environment}.tfvars"
        plan_result = self.plan(tf_dir, var_file)
        if not plan_result["success"]:
            return plan_result

        return self.apply(tf_dir)

    def destroy(self, tf_dir: str, auto_approve: bool = True) -> dict[str, Any]:
        """Destroy infrastructure.

        Args:
            tf_dir: Terraform directory.
            auto_approve: Auto-approve destruction.

        Returns:
            Destruction result.
        """
        cmd = "destroy"
        if auto_approve:
            cmd += " -auto-approve"

        result = self.run_terraform(cmd, tf_dir)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }


def deploy_gcp_function(
    project_id: str,
    function_name: str,
    region: str = "us-central1"
) -> dict[str, Any]:
    """Deploy a Cloud Function to GCP.

    Args:
        project_id: GCP project ID.
        function_name: Name of the function.
        region: GCP region.

    Returns:
        Deployment result.
    """
    cmd = [
        "gcloud", "functions", "deploy", function_name,
        "--project=" + project_id,
        "--region=" + region,
        "--runtime=python39",
        "--trigger-http",
        "--allow-unauthenticated"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "success": result.returncode == 0,
        "output": result.stdout,
        "error": result.stderr
    }


def deploy_lambda_function(
    function_name: str,
    zip_path: str,
    role_arn: str
) -> dict[str, Any]:
    """Deploy a Lambda function to AWS.

    Args:
        function_name: Name of the function.
        zip_path: Path to deployment package.
        role_arn: IAM role ARN.

    Returns:
        Deployment result.
    """
    cmd = [
        "aws", "lambda", "update-function-code",
        "--function-name", function_name,
        "--zip-file", f"fileb://{zip_path}"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "success": result.returncode == 0,
        "output": result.stdout,
        "error": result.stderr
    }


if __name__ == "__main__":
    deployer = CloudDeployer(provider="aws")
    print(f"Initialized deployer for {deployer.provider}")
