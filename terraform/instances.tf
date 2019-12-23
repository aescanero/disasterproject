variable "domain" {}
variable "ami" {}

resource "aws_instance" "kmaster" {
  ami                         = "${var.ami}"
  instance_type               = "t3.small"
  get_password_data           = false
  source_dest_check           = true
  associate_public_ip_address = false
  subnet_id                   = "${aws_subnet.private.id}"
  vpc_security_group_ids      = ["${aws_security_group.general_rule.id}"]
  key_name                    = "${aws_key_pair.aws-key.id}"
  private_ip                  = "192.168.8.11"
  user_data                   = "${file("userdata.sh")}"
  tags = {
    Domain = "${domain}"
    Name   = "kmaster.disasterproject.com"
  }
}

resource "aws_instance" "knode1" {
  ami                         = "${var.ami}"
  instance_type               = "t3.small"
  get_password_data           = false
  source_dest_check           = true
  associate_public_ip_address = false
  subnet_id                   = "${aws_subnet.private.id}"
  vpc_security_group_ids      = ["${aws_security_group.general_rule.id}"]
  key_name                    = "${aws_key_pair.aws-key.id}"
  private_ip                  = "192.168.8.12"
  user_data                   = "${file("userdata.sh")}"
  tags = {
    Domain = "${domain}"
    Name   = "knode1.disasterproject.com"
  }
}

resource "aws_instance" "knode2" {
  ami                         = "${var.ami}"
  instance_type               = "t3.small"
  get_password_data           = false
  source_dest_check           = true
  associate_public_ip_address = false
  subnet_id                   = "${aws_subnet.private.id}"
  vpc_security_group_ids      = ["${aws_security_group.general_rule.id}"]
  key_name                    = "${aws_key_pair.aws-key.id}"
  private_ip                  = "192.168.8.13"
  user_data                   = "${file("userdata.sh")}"
  tags = {
    Domain = "${domain}"
    Name   = "knode2.${domain}"
  }
}

resource "aws_instance" "launcher" {
  ami                         = "${var.ami}"
  instance_type               = "t2.micro"
  get_password_data           = false
  source_dest_check           = true
  associate_public_ip_address = true
  subnet_id                   = "${aws_subnet.public.id}"
  vpc_security_group_ids      = ["${aws_security_group.general_rule.id}"]
  key_name                    = "${aws_key_pair.aws-launcher-key.id}"
  private_ip                  = "192.168.0.254"
  user_data                   = "${file("userdata.launch.sh")}"
  tags = {
    Domain = "${domain}"
    Name   = "launcher.${domain}"
  }
}
