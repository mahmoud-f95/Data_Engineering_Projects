resource "aws_instance" "instance" {
  ami             = var.ami
  instance_type   = var.instance_type
  security_groups = var.security_groups
  user_data       = var.user_data

  tags = {
    Name = var.instance_name
  }
}

resource "aws_eip" "instance_ip" {
  instance = aws_instance.instance.id
  depends_on = [aws_instance.instance]
}
