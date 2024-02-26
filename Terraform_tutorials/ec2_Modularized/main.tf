provider "aws" {
  region = "eu-west-2"
}

module "networking" {
  source = "./networking"
  ingress = [80, 443]
  egress  = [80, 443]
}

module "db_instance" {
  source          = "./compute"
  ami             = "ami-032598fcc7e9d1c7a"
  instance_type   = "t2.micro"
  instance_name   = "DB Server"
}

module "web_instance" {
  source          = "./compute"
  ami             = "ami-032598fcc7e9d1c7a"
  instance_type   = "t2.micro"
  security_groups = [module.networking.security_group_name]
  user_data       = file("server-script.sh")
  instance_name   = "Web Server"
}
