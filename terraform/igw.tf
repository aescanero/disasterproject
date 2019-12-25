
resource "aws_internet_gateway" "igw" {
  vpc_id = "${aws_vpc.main.id}"

  tags = {
    Name   = "main"
    Domain = "${var.domain}"
  }
}
