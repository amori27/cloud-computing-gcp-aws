# Cloud Computing: GCP & AWS

Terraform templates and Python deployment scripts for multi-cloud infrastructure — VPC networking, compute (GKE/EKS), object storage (Cloud Storage/S3), and serverless functions.

## Usage

```bash
cd terraform/gcp
terraform plan -var-file=vars/dev.tfvars
terraform apply -var-file=vars/dev.tfvars
```

```python
from src.deployer import CloudDeployer
deployer = CloudDeployer(provider="aws")
deployer.deploy_infrastructure("dev")
```

## Structure

```
terraform/
├── gcp/         # GCP Terraform templates
└── aws/         # AWS Terraform templates
src/
├── deployer.py  # Deployment automation
└── utils.py     # Cloud utilities
```

## License

MIT
