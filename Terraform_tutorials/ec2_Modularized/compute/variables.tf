variable "ami" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "security_groups" {
  type = list(string)
  default = []
}

variable "user_data" {
  type    = string
  default = ""
}

variable "instance_name" {
  type = string
}
