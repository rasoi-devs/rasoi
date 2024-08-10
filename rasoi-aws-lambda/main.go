// The deployed ec2 instance becomes unresponsive after a certian period of time.
// Possibly due to extreme memory (RAM) consumption. I couldn't find a way to optimize it.
// This aws lambda function could hit the website periodically and check for it's availability.
// If unreachable, send an email and try to reboot the ec2 instance.
// This hacky solution temporarily works for now.

// Later, I realized, you can set an "Alarm" to send mails and reboot ec2 instance,
// if the instance is unreachable. That function is built-in to aws
// Thus, THIS LAMBDA FUNCTION IS PRACTICALLY USELESS!

// To deploy:
// `GOOS=linux GOARCH=amd64 go build -tags lambda.norpc -o bootstrap main.go && zip rasoi-aws-lambda.zip bootstrap`
// Then, upload `rasoi-aws-lambda.zip` as a zip file as new lambda function. Then, set the environment variables.

package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-lambda-go/lambdacontext"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/ses"
	"github.com/aws/aws-sdk-go-v2/service/ses/types"
	// "github.com/davecgh/go-spew/spew"
)

// environment variables
var FE_URL string = os.Getenv("FE_URL")
var BE_URL string = os.Getenv("BE_URL")
var EC2_INSTANCE_ID string = os.Getenv("EC2_INSTANCE_ID")
var RECEPIENT_EMAIL string = os.Getenv("RECEPIENT_EMAIL")
var SENDER_MAIL = RECEPIENT_EMAIL

type Result struct {
	FeReachable bool `json:"FeReachable"`
	BeReachable bool `json:"BeReachable"`
	RebootDone  bool `json:"RebootDone"`
}

var ec2Svc *ec2.Client
var sesSvc *ses.Client
var httpClient = http.Client{
	Timeout: 3 * time.Second,
}

// var instancePrivateIp string

func init() {
	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalln("Unable to load SDK config:", err)
	}
	ec2Svc = ec2.NewFromConfig(cfg)
	sesSvc = ses.NewFromConfig(cfg)

	// // get private ip (TODO: using private ip saves cost?)
	// result, err := ec2Svc.DescribeAddresses(
	// 	context.TODO(), &ec2.DescribeAddressesInput{
	// 		Filters: []types.Filter{
	// 			{
	// 				Name:   aws.String("instance-id"),
	// 				Values: []string{EC2_INSTANCE_ID},
	// 			},
	// 		},
	// 	},
	// )
	// if err != nil {
	// 	log.Fatalln("Unable to load instance private IP:", EC2_INSTANCE_ID, err)
	// }
	// instancePrivateIp = *result.Addresses[0].PrivateIpAddress
}

func checkReachable(url string, wg *sync.WaitGroup, resultChan chan<- bool) {
	defer wg.Done()
	resp, err := httpClient.Get(url)
	reachable := err == nil && resp.StatusCode == 200
	log.Println("Reachable:", reachable, "Target:", url, "err:", err)
	// return reachable, err
	resultChan <- reachable
}

func rebootInstance() bool {
	log.Println("Reboot EC2", EC2_INSTANCE_ID)

	_, err := ec2Svc.RebootInstances(context.TODO(), &ec2.RebootInstancesInput{
		InstanceIds: []string{EC2_INSTANCE_ID},
	})
	if err != nil {
		log.Println("Unable to reboot instance", EC2_INSTANCE_ID, err)
		return false
	}

	// resp, _ := middleware.GetRequestIDMetadata(resp.ResultMetadata)
	log.Println("Reboot done", EC2_INSTANCE_ID)
	return true
}

func sendMail(reachableFe bool, reachableBe bool, rebbotDone bool) {
	message := fmt.Sprintf("FE Reachable: %v\nBE Reachable: %v\nReboot done: %v\n", reachableFe, reachableBe, rebbotDone)

	input := &ses.SendEmailInput{
		Destination: &types.Destination{
			CcAddresses: []string{},
			ToAddresses: []string{
				RECEPIENT_EMAIL,
			},
		},
		Message: &types.Message{
			Body: &types.Body{
				Text: &types.Content{
					Charset: aws.String("UTF-8"),
					Data:    &message,
				},
			},
			Subject: &types.Content{
				Charset: aws.String("UTF-8"),
				Data:    aws.String("[rasoi aws lambda] reboot trigger"),
			},
		},
		Source: aws.String(SENDER_MAIL),
	}

	res, err := sesSvc.SendEmail(context.TODO(), input)

	if err != nil {
		log.Println("Unable to send mail", err.Error())
	} else {
		log.Println("Email sent, messageId:", *res.MessageId)
	}
}

func HandleRequest(ctx context.Context, event events.CloudWatchEvent) (*Result, error) {
	log.Println("Invoked", lambdacontext.FunctionName, lambdacontext.FunctionVersion)
	// log.Println("Args", event.Detail)
	// log.Println("Args Type", event.DetailType)

	// check reachability fe and be parallelly
	reachableFeC := make(chan bool, 1)
	reachableBeC := make(chan bool, 1)
	var wg sync.WaitGroup

	wg.Add(2)
	go checkReachable(FE_URL, &wg, reachableFeC)
	go checkReachable(BE_URL, &wg, reachableBeC)
	wg.Wait()

	reachableFe := <-reachableFeC
	reachableBe := <-reachableBeC

	rebootDone := false
	if !(reachableFe && reachableBe) {
		// reboot ec2
		rebootDone = rebootInstance()
		sendMail(reachableFe, reachableBe, rebootDone)
	}

	return &Result{
		FeReachable: reachableFe,
		BeReachable: reachableBe,
		RebootDone:  rebootDone,
	}, nil
}

func main() {
	lambda.Start(HandleRequest)
}
