resource "aws_lambda_function" "injury_extractor" {

  function_name = "injury-extractor"

  filename = "../lambda/function.zip"

  handler = "handler.lambda_handler"

  runtime = "python3.12"

  role = aws_iam_role.lambda_role.arn

}