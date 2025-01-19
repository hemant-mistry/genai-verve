from flask import Flask, request, jsonify
from flask_cors import CORS
import langflowsetup
import os
app = Flask(__name__)
CORS(app)
import json

@app.route("/api/getresponse", methods=['POST'])
def get_response():
    data = request.get_json()

    productDescription = data.get('productDescription')
    customerSegment = data.get('customerSegment')
    adLocation = data.get('adLocation')
    competitor = data.get('competitor')

    message = json.dumps({
        'productDescription' : productDescription,
        'customerSegment' : customerSegment,
        'adLocation' : adLocation,
        'competitor': competitor,
    }, indent=4)



    
    ctr = langflowsetup.start_flow(message,endpoint=os.getenv("CTR_URL"),passcode=os.getenv('CTR_TOKEN'))
    
    hooks = langflowsetup.start_flow(message,endpoint=os.getenv("HOOKS_URL"),passcode=os.getenv('HOOKS_TOKEN'))

    analysis = langflowsetup.start_flow(message,endpoint=os.getenv("ANALYSIS_URL"),passcode=os.getenv('ANALYSIS_TOKEN'))
    return jsonify({"ctr": ctr, 'hooks': hooks, 'analysis': analysis})

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True)