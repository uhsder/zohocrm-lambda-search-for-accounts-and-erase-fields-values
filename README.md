# Brief description

This function takes value from API Gateway and removes specific items from fields in ZohoCrm

# Environment variables setup

Lambda function uses 3 env. variables: **s3_bucket**, **file_with_zoho_token** and **refresh_token**.

s3_bucket - you S3 bucket with *file_with_zoho_token* which contains latest zoho token

file_with_zoho_token - actual file with token

refresh_token - this one should be generated through [Zoho](https://www.zoho.com/crm/help/api/v2/#OAuth2_0)
