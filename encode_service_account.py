from base64 import b64encode
cred_path = input("Path of the GCP creds JSON file: ")
creds = open(cred_path,'r').read()

encode_creds = b64encode(creds.encode()).decode()
open("encoded_creds",'w').write(encode_creds)