output "function_name" {
  description = "Name of the Lambda function."

  value = [aws_lambda_function.create_dynamodb_object.function_name,
          aws_lambda_function.delete_dynamodb_object.function_name,
          aws_lambda_function.retrieve_dynamodb_object.function_name,
          aws_lambda_function.update_dynamodb_object.function_name]
}

output "base_url" {
  description = "Base URL for API Gateway stage."

  value = aws_apigatewayv2_stage.lambda.invoke_url
}
