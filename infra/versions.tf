terraform {
  required_version = ">= 1.5"

  required_providers {
    linode = {
      source  = "linode/linode"
      version = "~> 2.0"
    }
  }

  # Uncomment to store state remotely (recommended for teams):
  # backend "s3" {
  #   endpoints = { s3 = "https://us-east-1.linodeobjects.com" }
  #   bucket   = "your-tf-state-bucket"
  #   key      = "ebike-shop/terraform.tfstate"
  #   region   = "us-east-1"
  # }
}