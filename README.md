# AWS Image Resizer Workflow

## Overview
This project implements a **serverless image processing pipeline** using **AWS Lambda**, **Step Functions**, and **S3**.  
When an image is uploaded to the `original-images-bucket-bolu`, it triggers a Step Functions workflow that resizes the image and stores the result in the `resized-images-bucket-bolu`.

## Architecture
1. **S3 (Input)** – Stores the original images.  
2. **Lambda (Resize Function)** – Uses the Pillow library to resize images.  
3. **Step Functions** – Orchestrates the resizing process and checks for success/failure.  
4. **API Gateway + Lambda (Starter Function)** – Starts the Step Function via an HTTP POST request.  
5. **S3 (Output)** – Stores the resized images.

## Components
- **Lambda functions:**
  - `resize_image` → Performs the image resizing.
  - `start_image_workflow` → Starts the Step Functions state machine.
- **Step Function state machine:**
  - Invokes the Lambda and handles success/failure transitions.
- **Buckets:**
  - Input: `original-images-bucket-bolu`
  - Output: `resized-images-bucket-bolu`

## How to Run
1. Upload an image (e.g., `unisex-premium.png`) to your input bucket.  
2. Trigger the workflow via API Gateway:
   ```bash
   curl -X POST "https://YOUR_API_URL/prod/start" \
   -H "Content-Type: application/json" \
   -d '{"bucket":"original-images-bucket-bolu","key":"unisex-premium.png"}'
3. Check the resized-images-bucket-bolu for the resized output.
    
    Key AWS Services Used
    
    AWS Lambda
    
    AWS Step Functions
    
    Amazon S3
    
    Amazon API Gateway
    
    AWS IAM (for permissions and execution roles)

Testing

    You can verify the workflow by:
    
    Checking Step Functions → Execution status should show Succeeded.
    
    Opening the output S3 bucket → The resized image file (e.g., resized-unisex-premium.jpg) should appear.

Author

    Boluwatife Malomo
