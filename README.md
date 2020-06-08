## S3
- Create an S3 bucket named *pdap-transcribe* set for static website hosting, and set with public access.
- Change the download link at the header of the html file to be `https://{bucket-name}.s3.{location}.amazonaws.com/transcript.txt`.
- Upload everything in the bucket folder to your S3 bucket.
- Go to the site and see if it displays correctly.

## Lambda
- Create an AWS lambda function for Python 3.8, giving it a custom role with the ability to modify S3 buckets and write into Cloudwatch (for debugging). Upload the `lambda_handler.py` code from this repo.
- Go down into the settings and change the timeout to at least 20 seconds.
- Test that it works for test JSON input.

## API Gateway
- Build a new REST API.
- Create a resource and name it anything.
- Create a POST method, with integration type Lambda Function. Make sure it's in the same region as your lambda function. Enter your lambda function name and hit save.
- In the method execution tab, click TEST to see if it's properly connected to the lambda function.
- Enable CORS.
- Deploy the API
- The link you want looks like `https://{random chars}.{resource}-api.{location}.amazonaws.com/{deployment name}/{resource}`. Click on your builds and then POST to find it.
Test it using `test1.sh` after inserting your API url into the CURL command.
- If your requests fail, setup cloudwatch logs for the API in the settings tab to check what's happening under the hood.

## S3, again
- Put your API url in the global variable at the top of `scripts.js` and upload that to the bucket.

## Even better
- I didn't do this but if you want to connect AWS Transcribe to this, the information could go *audio file from site > AWS API Gateway > Step function (AWS Transcribe > Lambda)*. Probably some other ways to do it too.
