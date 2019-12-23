resource "aws_key_pair" "aws-key" {
  key_name   = "aws-key"
  public_key = "${file("./files/disasterproject.groups.aws.key.ppk")}"
}

resource "aws_key_pair" "aws-launcher-key" {
  key_name   = "aws-launcher-key"
  public_key = "${file("./files/disasterproject.groups.aws.launcher.key.ppk")}"
}

