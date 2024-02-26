output "private_ip" {
  value = aws_instance.instance.private_ip
}

output "public_ip" {
  value = aws_eip.instance_ip.public_ip
}
