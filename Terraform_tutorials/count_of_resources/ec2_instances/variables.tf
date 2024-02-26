variable "instance_ids" {
  description = "A set of unique identifiers for each EC2 instance"
  type        = set(string)
}

variable "ami" {
  description = "The AMI to use for the instances"
  type        = string
}

variable "instance_type" {
  description = "The type of instance to start"
  type        = string
}

variable "region" {
  description = "The AWS region to create instances in"
  type        = string
  default     = "us-west-2"
}
