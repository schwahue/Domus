# Reference Link: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance

resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = var.db_engine_type
  engine_version       = "8.0.23"
  instance_class       = "db.t2.micro"
  identifier           = var.identifier
  name                 = var.db_name
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
  availability_zone    = "us-east-1a"
  publicly_accessible  = true

}


