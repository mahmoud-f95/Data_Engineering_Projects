output "DB_Private_IP" {
  value = module.db_instance.private_ip
}

output "Web_Public_IP" {
  value = module.web_instance.public_ip
}
