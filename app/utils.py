import os
import boto3
# import json
from flask import jsonify, request

# InstanceARN = 'arn:aws:connect:us-east-1:106294238846:instance/df42eb79-03d3-437f-ad91-a971455605c0'
# InstanceId = 'df42eb79-03d3-437f-ad91-a971455605c0'
# ContactflowID = '875fd970-edea-4b12-ad02-0092eef03723'
# ContactflowARN = 'arn:aws:connect:us-east-1:106294238846:instance/df42eb79-03d3-437f-ad91-a971455605c0/contact-flow/875fd970-edea-4b12-ad02-0092eef03723'

#Function to [GET] the contact_flow from aws.
def get_contact_flow_content(instance_id, contact_flow_id):
    # Initialize the boto3 client for Amazon Connect
    client = boto3.client(
        'connect',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN') 
    )
    try:
        # Get the content of the contact flow
        response = client.describe_contact_flow(
            InstanceId=instance_id,
            ContactFlowId=contact_flow_id
        )

        # Return the content of the contact flow
        return jsonify(response['ContactFlow']['Content'])
    except client.exceptions.ResourceNotFoundException:
        return jsonify({"error": "Contact flow not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    

#POST-DEL-NUMERO-BORRADOR-1
# def update_contact_flow_content():
#     # Retrieve AWS credentials and region from environment variables
#     aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
#     aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
#     aws_session_token = os.getenv('AWS_SESSION_TOKEN')
#     region = os.getenv('AWS_REGION')
#     client = boto3.client(
#     'connect',
#     region_name = region,
#     aws_access_key_id = aws_access_key_id,
#     aws_secret_access_key = aws_secret_access_key,
#     aws_session_token = aws_session_token )
#     try:
#         content = request.get_json()
#         phone_number = content['Parameters']['PhoneNumber']
#         response = client.update_contact_flow_content(
#             InstanceId='arn:aws:connect:us-east-1:106294238846:instance/df42eb79-03d3-437f-ad91-a971455605c0',
#             ContactFlowId='arn:aws:connect:us-east-1:106294238846:instance/df42eb79-03d3-437f-ad91-a971455605c0/contact-flow/875fd970-edea-4b12-ad02-0092eef03723',
#             Content=json.dumps({"Parameters": {"PhoneNumber":  +56945782949}})
#         )
#         return jsonify({"message": "Successfully updated contact flow content"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

