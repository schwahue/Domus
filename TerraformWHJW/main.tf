# call variables with 'var.<something>'

provider "aws" {
  region                  = "us-east-1"
  shared_credentials_file = "/Users/whjw1/.aws/credentials"
  profile                 = "default"
}


module "rds_db" {
  source         = "./database_module"
  db_engine_type = var.db_engine_type
  db_name        = var.db_name
  db_username    = var.db_username
  db_password    = var.db_password
  identifier     = var.identifier
}

# output "output_see_db_engine_type" {
#   value = module.rds_db.db_engine_type
# }
