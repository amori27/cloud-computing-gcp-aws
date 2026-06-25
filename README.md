# Cloud Computing GCP & AWS
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


Infrastructure as Code (IaC) templates and deployment scripts for Google Cloud Platform and Amazon Web Services using Terraform, Python, and cloud-native services.

## Description

Comprehensive cloud infrastructure project featuring Terraform templates for GCP and AWS, deployment automation scripts, and best practices for scalable cloud architecture including networking, compute, storage, and serverless components.

## Skills & Technologies

- Terraform 1.0+
- Google Cloud Platform (GCP)
- Amazon Web Services (AWS)
- Python Cloud SDKs
- Kubernetes (GKE/EKS)
- Cloud Functions/Lambda
- Cloud Storage/S3
- VPC Networking

## Installation

```bash
git clone https://github.com/amori27/cloud-computing-gcp-aws.git
cd cloud-computing-gcp-aws
pip install -r requirements.txt
terraform init
```

## Usage

### Terraform Deployment

```bash
cd terraform/gcp
terraform plan -var-file=vars/dev.tfvars
terraform apply -var-file=vars/dev.tfvars
```

### Python Deployment Script

```python
from src.deployer import CloudDeployer

deployer = CloudDeployer(provider="aws")
deployer.deploy_infrastructure("dev")
```

## Project Structure

```
cloud-computing-gcp-aws/
├── terraform/
│   ├── gcp/           # GCP Terraform templates
│   └── aws/           # AWS Terraform templates
├── src/
│   ├── deployer.py    # Deployment automation
│   └── utils.py       # Cloud utilities
├── scripts/           # Deployment scripts
├── requirements.txt
└── README.md
```

## References

- [Terraform Documentation](https://www.terraform.io/docs)
- [GCP Documentation](https://cloud.google.com/docs)
- [AWS Documentation](https://docs.aws.amazon.com/)

## License

MIT License
