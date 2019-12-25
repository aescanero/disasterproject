resource "tls_private_key" "tls-key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_private_key" "tls-launcher-key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "aws-key" {
  key_name   = "aws-key"
  public_key = fileexists("./files/disasterproject.groups.aws.key.ppk") == false ? "${tls_private_key.tls-key.public_key_openssh}" : file("./files/disasterproject.groups.aws.key.public")

  provisioner "local-exec" {
    command = "if ! [ -f ./files/disasterproject.groups.aws.key.ppk ];then echo '${tls_private_key.tls-key.public_key_openssh}' > './files/disasterproject.groups.aws.key.public' && echo '${tls_private_key.tls-key.private_key_pem}' > './files/disasterproject.groups.aws.key.ppk' && chmod 600 './files/disasterproject.groups.aws.key.ppk';fi"
  }
}

resource "aws_key_pair" "aws-launcher-key" {
  key_name   = "aws-launcher-key"
  public_key = fileexists("./files/disasterproject.groups.aws.launcher.key.ppk") == false ? "${tls_private_key.tls-launcher-key.public_key_openssh}" : file("./files/disasterproject.groups.aws.launcher.key.public")

  provisioner "local-exec" {
    command = "if ! [ -f ./files/disasterproject.groups.aws.launcher.key.ppk ];then echo '${tls_private_key.tls-launcher-key.public_key_openssh}' > './files/disasterproject.groups.aws.launcher.key.public' && echo '${tls_private_key.tls-launcher-key.private_key_pem}' > './files/disasterproject.groups.aws.launcher.key.ppk' && chmod 600 './files/disasterproject.groups.aws.launcher.key.ppk';fi"
  }
}
