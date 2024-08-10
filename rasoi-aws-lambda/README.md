# rasoi-aws-lambda

The deployed ec2 instance becomes unresponsive after a certian period of time.
Possibly due to extreme memory (RAM) consumption. I couldn't find a way to optimize it.
This aws lambda function could hit the website periodically and check for it's availability.
If unreachable, send an email and try to reboot the ec2 instance.
This hacky solution temporarily works for now.

Later, I realized, you can set an "Alarm" to send mails and reboot ec2 instance,
if the instance is unreachable. That function is built-in to aws
Thus, THIS LAMBDA FUNCTION IS PRACTICALLY USELESS!

To deploy:
`GOOS=linux GOARCH=amd64 go build -tags lambda.norpc -o bootstrap main.go && zip rasoi-aws-lambda.zip bootstrap`
Then, upload `rasoi-aws-lambda.zip` as a zip file as new lambda function. Then, set the environment variables.
