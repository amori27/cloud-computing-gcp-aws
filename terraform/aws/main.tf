provider "aws" {
  region = var.region
}

variable "region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

resource "aws_vpc" "vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.environment}-vpc"
  }
}

resource "aws_subnet" "subnet" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.environment}-subnet"
  }
}

resource "aws_instance" "ec2_instance" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet.id

  tags = {
    Name = "${var.environment}-instance"
  }
}

resource "aws_s3_bucket" "bucket" {
  bucket = "${var.environment}-bucket-${random_id.bucket_id.hex}"

  tags = {
    Name        = "${var.environment}-bucket"
    Environment = var.environment
  }
}

resource "random_id" "bucket_id" {
  byte_length = 8
}
