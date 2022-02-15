# If we do not specify a default value, when we run the plan, it will prompt us to enter the value for each variable respectively
# If there is a default value, it will not prompt to enter value for variable, we should instead use .tfvars files to configure different values


variable "instance_type" {
  type        = string
  description = "Instance type of EC2"
  default     = "t2.micro"
}

# From database_module variables.tf

variable "db_engine_type" {
  type        = string
  description = "Database engine type: "
  default     = "mysql"
}

variable "identifier" {
  type        = string
  description = "Database instance name: "
}

variable "db_name" {
  type        = string
  description = "Database name:"
}

variable "db_username" {
  type        = string
  description = "Database root username: "
}

variable "db_password" {
  type        = string
  description = "Database root user password: "
}

