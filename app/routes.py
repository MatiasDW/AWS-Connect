from .utils import get_contact_flow_content  # Import my function from utils.py
from flask import request
from .utils import modify_contact_flow_phone_number


#This is the END POINT is to [Get] the contact flow from AWS-Connect, you have to pass in the url the instance_id & contact_flow_id.
def define_routes(app):
    @app.route('/contact-flows/<instance_id>/<contact_flow_id>', methods=['GET'])
    def get_contact_flow(instance_id, contact_flow_id):
        return get_contact_flow_content(instance_id, contact_flow_id)

    #This is the END POINT to [Post] in the contact flow to change the phone number in the "Transfer to phone number" block.  
    @app.route('/update-contact-flow/<instance_id>/<contact_flow_id>', methods=['POST'])
    def update_contact_flow(instance_id, contact_flow_id):
       new_phone_number = request.json.get("ThirdPartyPhoneNumber")
       return modify_contact_flow_phone_number(instance_id, contact_flow_id, new_phone_number)


# def define_routes(app):
#     @app.route('/contact-flows/arn:aws:connect:us-east-1:106294238846:instance/df42eb79-03d3-437f-ad91-a971455605c0/arn:aws:connect:us-east-1:106294238846:instance/df42eb79-03d3-437f-ad91-a971455605c0/contact-flow/875fd970-edea-4b12-ad02-0092eef03723/content', methods=['POST'])
#     def route_update_contact_flow_content():
#       return update_contact_flow_content()