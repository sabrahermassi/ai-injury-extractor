resource "aws_lambda_function" "injury_extractor" {
  function_name = "injury-extractor"

  filename = "../lambda/function.zip"

  source_code_hash = filebase64sha256("../lambda/function.zip")

  handler = "handler.lambda_handler"
  runtime = "python3.12"

  role = aws_iam_role.lambda_role.arn

  environment {
    variables = {
      GROQ_API_KEY = var.groq_api_key
    }
  }
}