module "ec2_instances" {
  source        = "./ec2_instances"
  instance_ids  = toset(["instance1", "instance2", "instance3"])
  ami           = "ami-0c55b159cbfafe1f0" # Replace with the actual AMI you want to use
  instance_type = "t2.micro"
}

output "ec2_instance_private_ips" {
  value = module.ec2_instances.instance_private_ips
  description = "The private IP addresses of the EC2 instances created by the module"
}
