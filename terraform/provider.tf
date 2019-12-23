variable "region" {}

provider "aws" {
  profile = "default"
  region  = "${var.region}"
}
