import boto3, os, time, datetime, sys, json
from datetime import date
from botocore.exceptions import ClientError

iam = boto3.client('iam')

def lambda_handler(event, context):
    email_70_list = []
    email_80_list = []
    email_90_list = []
    
    # print("All IAM user emails that have AccessKeys 30 days or older")
    unique_user_list = (iam.list_users()['Users'])
    for userlist in unique_user_list:
        userKeys = iam.list_access_keys(UserName=userlist['UserName'])
        for keyValue in userKeys['AccessKeyMetadata']:
            UserAccessKeyID = keyValue['AccessKeyId']
            IAMUserName = keyValue['UserName']
            #print(f"IAMUserName IAM Users:{len(IAMUserName)}: {IAMUserName}")
            if keyValue['Status'] == 'Active':
                currentdate = date.today()
                active_days = currentdate - keyValue['CreateDate'].date()
                #print ("The active days details are: ", active_days)
                #print ("datetime details are: ", datetime.timedelta(days=15))
                
                # if Access key age is greater then or equal to 70 days, send warning
                if active_days == datetime.timedelta(days=int(os.environ['days_70'])):
                    userTags = iam.list_user_tags(UserName=keyValue['UserName'])
                    email_tag = list(filter(lambda tag: tag['Key'] == 'email', userTags['Tags']))
                    if(len(email_tag) == 1):
                        email = email_tag[0]['Value']
                        email_70_list.append(email)
                        print("This User: ", IAMUserName, ", with the email: ", email, ", is having access key age is 70 days")      
                        
                        email_unique = list(set(email_70_list))
                        print("Email list: ", email_unique)
                        RECIPIENTS = email_unique
                        SENDER = os.environ['sender_email']
                        AWS_REGION = os.environ['region']
                        SUBJECT_70 = os.environ['SUBJECT_70']
                        BODY_TEXT_70 = os.environ['BODY_TEXT_70']
                        BODY_HTML_70 = os.environ['BODY_HTML_70']           
                        CHARSET = "UTF-8"
                        client = boto3.client('ses',region_name=AWS_REGION)
                        try:
                            response = client.send_email(
                                Destination={
                                    'ToAddresses': RECIPIENTS,
                                },
                                Message={
                                    'Body': {
                                        'Html': {
                                            'Charset': CHARSET,
                                            'Data': BODY_HTML_70,
                                        },
                                        'Text': {
                                            'Charset': CHARSET,
                                            'Data': BODY_TEXT_70,
                                        },
                                    },
                                    'Subject': {
                                        'Charset': CHARSET,
                                        'Data': SUBJECT_70,
                                    },
                                },
                                Source=SENDER,
                            )
                        except ClientError as e:
                            print(e.response['Error']['Message'])
                        else:
                            print("Email sent! Message ID:"),
                            print(response['MessageId'])
    
                # if Access Key Age is greater then 80 days, send email alert
                if active_days == datetime.timedelta(days=int(os.environ['days_80'])):
                    userTags = iam.list_user_tags(UserName=keyValue['UserName'])
                    email_tag = list(filter(lambda tag: tag['Key'] == 'email', userTags['Tags']))
                    if(len(email_tag) == 1):
                        email = email_tag[0]['Value']
                        email_80_list.append(email)
                        print("The User: ", IAMUserName, ", with the email: ", email, ", is having access key age is 80 days")
    
                        email_unique = list(set(email_80_list))
                        print("Email list: ", email_unique)
                        RECIPIENTS = email_unique
                        SENDER = os.environ['sender_email']
                        print("Sender: ", SENDER)
                        AWS_REGION = os.environ['region']
                        SUBJECT_80 = os.environ['SUBJECT_80']
                        BODY_TEXT_80 = os.environ['BODY_TEXT_80']
                        BODY_HTML_80 = os.environ['BODY_HTML_80']            
                        CHARSET = "UTF-8"
                        client = boto3.client('ses',region_name=AWS_REGION)
                        try:
                            response = client.send_email(
                                Destination={
                                    'ToAddresses': RECIPIENTS,
                                },
                                Message={
                                    'Body': {
                                        'Html': {
                                            'Charset': CHARSET,
                                            'Data': BODY_HTML_80,
                                        },
                                        'Text': {
                                            'Charset': CHARSET,
                                            'Data': BODY_TEXT_80,
                                        },
                                    },
                                    'Subject': {
                                        'Charset': CHARSET,
                                        'Data': SUBJECT_80,
                                    },
                                },
                                Source=SENDER,
                            )
                        except ClientError as e:
                            print(e.response['Error']['Message'])
                        else:
                            print("Email sent! Message ID:"),
                            print(response['MessageId'])
    
                # if Access Key Age is greater then 90 days, send email alert and inactive access keys
                if active_days >= datetime.timedelta(days=int(os.environ['days_90'])):
                    userTags = iam.list_user_tags(UserName=keyValue['UserName'])
                    email_tag = list(filter(lambda tag: tag['Key'] == 'email', userTags['Tags']))
                    user1_tag = list(filter(lambda tag: tag['Key'] == 'UserType', userTags['Tags']))
                    if(len(email_tag) == 1):
                        email = email_tag[0]['Value']
                        email_90_list.append(email)
                        print("The User: ", IAMUserName, ", with the email: ", email, ", is having access key age is greater then 90 days")
                        
                        if(len(user1_tag) == 1):
                            user1tag = user1_tag[0]['Value']
                            if user1tag == "Employee":
                                iam.update_access_key(AccessKeyId=UserAccessKeyID,Status='Inactive',UserName=IAMUserName)
                                print("Status has been updated to Inactive")
    
                        email_unique = list(set(email_90_list))
                        print("Email list: ", email_unique)
                        RECIPIENTS = email_unique
                        SENDER = os.environ['sender_email']
                        print("Sender: ", SENDER)
                        AWS_REGION = os.environ['region']
                        SUBJECT_90 = os.environ['SUBJECT_90']
                        BODY_TEXT_90 = os.environ['BODY_TEXT_90']
                        BODY_HTML_90 = os.environ['BODY_HTML_90']          
                        CHARSET = "UTF-8"
                        client = boto3.client('ses',region_name=AWS_REGION)
                        try:
                            response = client.send_email(
                                Destination={
                                    'ToAddresses': RECIPIENTS,
                                },
                                Message={
                                    'Body': {
                                        'Html': {
                                            'Charset': CHARSET,
                                            'Data': BODY_HTML_90,
                                        },
                                        'Text': {
                                            'Charset': CHARSET,
                                            'Data': BODY_TEXT_90,
                                        },
                                    },
                                    'Subject': {
                                        'Charset': CHARSET,
                                        'Data': SUBJECT_90,
                                    },
                                },
                                Source=SENDER,
                            )
                        except ClientError as e:
                            print(e.response['Error']['Message'])
                        else:
                            print("Email sent! Message ID:"),
                            print(response['MessageId'])
