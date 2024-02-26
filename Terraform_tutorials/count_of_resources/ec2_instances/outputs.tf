output "instance_private_ips" {
  value = { for id, instance in aws_instance.app_servers : id => instance.private_ip }
  description = "The private IP addresses of the EC2 instances"
}
