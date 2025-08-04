resource "aws_lambda_function" "whatsapp_bot" {
  filename         = "${path.root}/../app/lambda.zip"
  function_name    = "CyrstalVisionChatBot"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("${path.root}/../app/lambda.zip")
  runtime          = "python3.8"
  environment {
    variables = {
      WHATSAPP_ACCESS_TOKEN = var.whatsapp_access_token
      PHONE_NUMBER_ID       = var.phone_number_id
      WEBHOOK_VERIFY_TOKEN  = var.webhook_verify_token
    }
  }
}

# resource "aws_lambda_permission" "allow_s3_invoke" {
#   statement_id  = "AllowS3Invoke"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.function.function_name
#   principal     = "s3.amazonaws.com"
#   source_arn    = var.bucket_arn
# }
