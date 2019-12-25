variable "vpc_network" {}

resource "aws_vpc" "main" {
  cidr_block = "${var.vpc_network}"
}
