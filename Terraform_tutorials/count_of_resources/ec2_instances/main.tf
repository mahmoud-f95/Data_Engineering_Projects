provider "aws" {
  region = var.region
}

resource "aws_instance" "app_servers" {
  for_each     = var.instance_ids
  ami          = var.ami
  instance_type = var.instance_type

  tags = {
    Name = "ExampleInstance-${each.key}"
  }
}
