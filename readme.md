# AWS Lambda Edsby Integration
This is an AWS Lambds function that uses [PyEdsby](https://github.com/ctrezevant/PyEdsby) to
post provided messages/links to the specified class NIDs.

This allows you to post links and messages to class feeds using simple HTTP calls, the
practical upshot of this being that you can integrate Edsby with services like IFTTT and
anything else that supports Webhooks/HTTP POSTs.

To call the function's API, select API Gateway as its trigger, ensuring you choose the "Open" policy.

Then, post the following JSON payload to its HTTP endpoint:

```json
{
  "link": "If you're posting a link, put it here. Empty if not specified.",
  "text": "The message body. Empty if not specified.",
  "username": "your Edsby username Read from config file if not specified",
  "password": "your Edsby password. Read from config file if not specified",
  "classIDs": "list,of,class,IDs. Read from config file if not specified",
  "key": "Must match key in config file."
}
```

## Prerequisites
You need to install python-requests into the lib folder. To do so, run:

```shell
pip install requests --target=./lib
```

You can then create a ZIP file for your [Lambda deployment package](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) like so:

```shell
zip -r ~/Desktop/edsby_lambda.zip ./*
```

### Suggested Lambda Configuration
- **Runtime:** Python 2.7
- **Handler:** main.handle_request
- **Memory:** 128
- **Timeout:** 5 sec
