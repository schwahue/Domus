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
  description = "Database name: "
}

variable "db_username" {
  type        = string
  description = "Database root username: "
}

variable "db_password" {
  type        = string
  description = "Database root user password: "
}

