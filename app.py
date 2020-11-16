from flask import Flask, render_template, request
import boto3
from werkzeug.utils import secure_filename
import time as time
from cryptography.fernet import Fernet
import os 
import sys

# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

key=b'nYGePYkhuWF-Q9XejqSyfn1EcI9ZBpVdppMrsrHuV48='

crypter= Fernet(key)

# import api


aws_access_key_id= crypter.decrypt(b'gAAAAABfryXGH4yqA15yBaF2lbNv8tPoKNZpAAHaTGImom1ZK1U9zbRwLIm4rznx6uGJgDEGcs0WDMiVt5T-D5kOm-1-LxELtJHiLx_-5g4WLbMOs2cQAFY=')
aws_access_key_id=aws_access_key_id.decode("utf-8")

aws_secret_access_key= crypter.decrypt(b'gAAAAABfryXGz7rxAkppWFdzPz0_ek_KJRIcTlNha4RoCMI-5daV1lbJO-H4E2hyjD8vv8qTgwNDgVtVZg5VmcQYETaOs30CYQKtTGFAUB41P3-VGDPGElOSALBp_N_NGzE4UCd4zWPb')
aws_secret_access_key=aws_secret_access_key.decode("utf-8")



application= app = Flask(__name__)





# aws_access_key_id='12323'
# aws_secret_access_key= ''


s3 = boto3.resource('s3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key= aws_secret_access_key,
                    # aws_session_token=keys.AWS_SESSION_TOKEN
                     )

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name='us-east-1')





BUCKET_NAME='transcriberbucket1'
# BUCKET_NAME='transcriber2.0bucket'

@app.route('/')  
def home():

    return render_template("file_upload_to_s3.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        mp3 = request.files['file']
        email=request.form['email']
        # time=time.ctime()

# #         # USED FOR CREATING THE TABLE INITIALLY
#         table = dynamodb.create_table(
#     TableName='newtable',
#     KeySchema=[
#         {
#             'AttributeName': 'email',
#             'KeyType': 'HASH'
#         }
         
#     ],
#     AttributeDefinitions=[
#              {
#             'AttributeName': 'time',
#             'AttributeType': 'S',

#             'AttributeName': 'time-number',
#             'AttributeType': 'S',

#             'AttributeName': 'email',
#             'AttributeType': 'S',

#         } 
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 1,
#         'WriteCapacityUnits': 1,
#     }

# )
        # table = dynamodb.Table('newtable')
        # Wait until the table exists.
        # table.meta.client.get_waiter('table_exists').wait(TableName='newtable')

        # IPopulating the table created with users input
        table = dynamodb.Table('newtable')
        
        table.put_item(
                Item={
        
        'email': email,
        'date': time.ctime(),
        'time-number': str(time.time()),
        
            }
        )



        # msg2 = "Transcription should "


        if mp3:

                filename = secure_filename(mp3.filename)
                mp3.save(filename)
                s3.meta.client.upload_file(filename, BUCKET_NAME, 'audioFile/%s' % (filename))
                # s3.upload_file(
                #     Bucket = BUCKET_NAME,
                #     Filename=filename,
                #     Key = filename
                # )
                msg= 'Upload Done! Your file is being proccessed and will be emailed to you shortly'


        


    return render_template("file_upload_to_s3.html",msg =msg)





if __name__ == "__main__":
    
    app.run( host="0.0.0.0",
    port=5000, debug=True)
