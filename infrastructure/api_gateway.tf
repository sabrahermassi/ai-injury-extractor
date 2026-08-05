resource "aws_api_gateway_rest_api" "injury_api" {
  name = "injury-extractor-api"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "extract" {
  rest_api_id = aws_api_gateway_rest_api.injury_api.id
  parent_id   = aws_api_gateway_rest_api.injury_api.root_resource_id
  path_part   = "extract"
}

resource "aws_api_gateway_method" "extract_post" {
  rest_api_id = aws_api_gateway_rest_api.injury_api.id
  resource_id = aws_api_gateway_resource.extract.id

  http_method = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.injury_api.id
  resource_id = aws_api_gateway_resource.extract.id
  http_method = aws_api_gateway_method.extract_post.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"

  uri = aws_lambda_function.injury_extractor.invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.injury_extractor.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.injury_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.injury_api.id

  depends_on = [
    aws_api_gateway_integration.lambda
  ]
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id  = aws_api_gateway_rest_api.injury_api.id
  stage_name   = "dev"
}