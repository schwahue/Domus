terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "Ticketing"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "UserId"
  range_key      = "TicketId"

  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "TicketId"
    type = "S"
  }

  attribute {
    name = "Status"
    type = "S"
  }

  global_secondary_index {
    name               = "TicketIndex"
    hash_key           = "TicketId"
    range_key          = "Status"
    write_capacity     = 1
    read_capacity      = 1
    projection_type    = "INCLUDE"
    non_key_attributes = ["UserId"]
  }

  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}

data "archive_file" "lambda_create_dynamodb_object" {
    type="zip"

    source_file = "${path.module}/Lambda-functions/create-dynamodb-object.py"
    output_path = "${path.module}/Lambda-functions-zip/create-dynamodb-object.zip"
}

data "archive_file" "lambda_delete_dynamodb_object" {
    type="zip"

    source_file = "${path.module}/Lambda-functions/delete-dynamodb-object.py"
    output_path = "${path.module}/Lambda-functions-zip/delete-dynamodb-object.zip"
}

data "archive_file" "lambda_retrieve_dynamodb_object" {
    type="zip"

    source_file = "${path.module}/Lambda-functions/retrieve-dynamodb-object.py"
    output_path = "${path.module}/Lambda-functions-zip/retrieve-dynamodb-object.zip"
}

data "archive_file" "lambda_update_dynamodb_object" {
    type="zip"

    source_file = "${path.module}/Lambda-functions/update-dynamodb-object.py"
    output_path = "${path.module}/Lambda-functions-zip/update-dynamodb-object.zip"
}

resource "aws_lambda_function" "create_dynamodb_object" {
    function_name= "Create-DynamoDb-Object"
    role="arn:aws:iam::043264810099:role/LabRole"

    filename = data.archive_file.lambda_create_dynamodb_object.output_path

    runtime = "python3.8"
    handler = "create-dynamodb-object.lambda_handler"

    source_code_hash = data.archive_file.lambda_create_dynamodb_object.output_base64sha256
}

resource "aws_lambda_function" "delete_dynamodb_object" {
  function_name = "Delete-DynamoDb-Object"
  role="arn:aws:iam::043264810099:role/LabRole"

  filename = data.archive_file.lambda_delete_dynamodb_object.output_path

  runtime = "python3.8"
  handler = "delete-dynamodb-object.lambda_handler"

  source_code_hash = data.archive_file.lambda_delete_dynamodb_object.output_base64sha256
}

resource "aws_lambda_function" "retrieve_dynamodb_object" {
  function_name = "Retrieve-DynamoDb-Object"
  role="arn:aws:iam::043264810099:role/LabRole"

  filename = data.archive_file.lambda_retrieve_dynamodb_object.output_path

  runtime = "python3.8"
  handler = "retrieve-dynamodb-object.lambda_handler"

  source_code_hash = data.archive_file.lambda_retrieve_dynamodb_object.output_base64sha256
}

resource "aws_lambda_function" "update_dynamodb_object" {
  function_name = "Update-DynamoDb-Object"
  role="arn:aws:iam::043264810099:role/LabRole"

  filename = data.archive_file.lambda_update_dynamodb_object.output_path

  runtime = "python3.8"
  handler = "update-dynamodb-object.lambda_handler"

  source_code_hash = data.archive_file.lambda_update_dynamodb_object.output_base64sha256
}

resource "aws_apigatewayv2_api" "lambda" {
  name          = "domus_lambda_gw"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  name        = "domus_lambda_stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "create_dynamodb_object" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.create_dynamodb_object.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "create_dynamodb_object" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "PUT /create-dynamodb-object"
  target    = "integrations/${aws_apigatewayv2_integration.create_dynamodb_object.id}"
}

resource "aws_apigatewayv2_integration" "delete_dynamodb_object" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.delete_dynamodb_object.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "delete_dynamodb_object" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "DELETE /delete-dynamodb-object"
  target    = "integrations/${aws_apigatewayv2_integration.delete_dynamodb_object.id}"
}

resource "aws_apigatewayv2_integration" "retrieve_dynamodb_object" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.retrieve_dynamodb_object.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "retrieve_dynamodb_object" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "GET /retrieve-dynamodb-object"
  target    = "integrations/${aws_apigatewayv2_integration.retrieve_dynamodb_object.id}"
}
resource "aws_apigatewayv2_integration" "update_dynamodb_object" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = aws_lambda_function.update_dynamodb_object.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "update_dynamodb_object" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "POST /update-dynamodb-object"
  target    = "integrations/${aws_apigatewayv2_integration.update_dynamodb_object.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"

  retention_in_days = 30
}

resource "aws_lambda_permission" "create_dynamodb_object" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_dynamodb_object.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}

resource "aws_lambda_permission" "delete_dynamodb_object" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_dynamodb_object.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}

resource "aws_lambda_permission" "retrieve_dynamodb_object" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.retrieve_dynamodb_object.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}

resource "aws_lambda_permission" "update_dynamodb_object" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_dynamodb_object.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}
