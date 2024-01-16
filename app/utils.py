import os
import boto3
import json
from flask import jsonify

# InstanceARN = 'arn:aws:connect:us-east-1:106294238846:instance/df42eb79-03d3-437f-ad91-a971455605c0'
# InstanceId = 'df42eb79-03d3-437f-ad91-a971455605c0'
# ContactFlowID = '875fd970-edea-4b12-ad02-0092eef03723'
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


# Function to the [POST] method, where we search for the parameter, update it and convert it back to a Json.
def modify_contact_flow_phone_number(instance_id, contact_flow_id, new_phone_number):
    print("AWS Region:", 'us-east-1')
    print("AWS Access Key ID:", os.getenv('AWS_ACCESS_KEY_ID'))
    print("AWS Secret Access Key:", os.getenv('AWS_SECRET_ACCESS_KEY'))
    print("AWS Session Token:", os.getenv('AWS_SESSION_TOKEN'))

    # Initialize the boto3 client for Amazon Connect
    client = boto3.client(
        'connect',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN') 
    )
    #Print the instance_id and contact_flow_id for debugging
    print("InstanceId:", instance_id)
    print("ContactFlowId:", contact_flow_id)
    #Get the current content of the contact flow
    try:
        current_flow = client.describe_contact_flow(InstanceId=instance_id, ContactFlowId=contact_flow_id)
        print("InstanceId:", instance_id)
        print("ContactFlowId:", contact_flow_id)
        print("Raw contact flow content:", current_flow['ContactFlow']['Content'])  # Imprimir el contenido en bruto del flujo de contacto
        flow_content = json.loads(current_flow['ContactFlow']['Content'])
        print("Parsed contact flow content:", flow_content)  # Imprimir el contenido del flujo de contacto después de json.loads
    except Exception as e:
        print("Error during API call:", e)
        return jsonify({"error": f"Error getting contact flow: {str(e)}"}), 500

    # Deeply navigate through the JSON to find and update the 'ThirdPartyPhoneNumber' parameter
    updated = False
    for action in flow_content.get('Actions', []):
        print("Inspecting action:", action)
        if action.get('Type') == 'TransferParticipantToThirdParty':
            # Navigate deeper if necessary
            parameters = action.get('Parameters', {})
            if 'ThirdPartyPhoneNumber' in parameters:
                # Update the phone number
                parameters['ThirdPartyPhoneNumber'] = new_phone_number
                updated = True
                break

    if not updated:
        return jsonify({"error": "ThirdPartyPhoneNumber not found in the contact flow"}), 404

    # Convert the modified content back to JSON
    updated_content = json.dumps(flow_content)

    # Update the contact flow in Amazon Connect with the new content
    try:
        response = client.update_contact_flow_content(
            InstanceId=instance_id,
            ContactFlowId=contact_flow_id,
            Content=updated_content
        )
        print(response)
        return jsonify({"message": "Contact flow updated successfully", "response": response})
    except Exception as e:
        return jsonify({"error": f"Error updating contact flow: {str(e)}"}), 500