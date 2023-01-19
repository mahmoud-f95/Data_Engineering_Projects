import json
import boto3
import os
import urllib.parse

s3= boto3.resource('s3')
#s3=boto3.client('s3')
comprehend = boto3.client('comprehend')
firehose = boto3.client('firehose')

def lambda_handler(event, context):

    print(event)
    
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        
        obj = s3.Object(s3_bucket, s3_key)
        tweets_as_string = obj.get()['Body'].read().decode('utf-8') 
    
        tweets = tweets_as_string.split('\n')
        
        for tweet_string in tweets:
            
            if len(tweet_string) < 1:
                continue
            
            tweet = json.loads(tweet_string)
         
            
            comprehend_text = tweet['tweet_text']
        
            sentiment_response = comprehend.detect_sentiment(
                    Text=comprehend_text,
                    LanguageCode='en'
              )
            
            
                
            print(sentiment_response)
 

            sentiment_record = {
                'userid': tweet['user_name'],
                'timestamp':tweet['timestamp'],
                'location':tweet['location'],
                'text': comprehend_text,

                'sentiment': sentiment_response['Sentiment'],
                'sentimentposscore': sentiment_response['SentimentScore']['Positive'],
                'sentimentnegscore': sentiment_response['SentimentScore']['Negative'],
                'sentimentneuscore': sentiment_response['SentimentScore']['Neutral'],
                'sentimentmixedscore': sentiment_response['SentimentScore']['Mixed']
            }
            
            
            #print(sentiment_record)
            
            response = firehose.put_record(
                DeliveryStreamName='sentiment_stream',
                Record={
                    'Data': json.dumps(sentiment_record) + '\n'
                }
            )
            
           
                    

            
    return 'true'
    
    #print(sentiment_record)
    #print(type(tweets))
