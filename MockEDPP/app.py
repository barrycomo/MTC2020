#!/usr/bin/python
from flask import Flask
from flask import jsonify
from flask import request
import base64
import fileinput
import json
import os.path

app = Flask(__name__)

def authorized(auth):
    # DO NOT USE THIS IN PRODUCTION
    contents = ""
    with open('auth.txt', 'r') as auth_file:
        contents = auth_file.read()
    if contents == base64.b64decode(auth[6:]).decode():
        return True
    else:
        return False

def setHeaderValues(headers):
    XRequestID = ''
    XCorrelationID = ''
    XBusinessCorrelationId = ''
    XWorkflowCorrelationId = ''

    if 'X-Request-ID' in headers:
        XRequestID = headers['X-Request-ID']
    if 'X-Correlation-ID' in headers:
        XCorrelationID = headers['X-Correlation-ID']
    if 'X-BusinessCorrelationId' in headers:
        XBusinessCorrelationId = headers['X-BusinessCorrelationId']
    if 'X-WorkflowCorrelationId' in headers:
        XWorkflowCorrelationId = headers['X-WorkflowCorrelationId']
    return XRequestID, XCorrelationID, XBusinessCorrelationId, XWorkflowCorrelationId    

@app.route('/api/v1/institutions/<InstitutionId>/environments/<InstitutionEnvironment>/products/<ProductCode>/EDPP/verification', methods = ['POST'])
def verification(InstitutionId, InstitutionEnvironment, ProductCode):
    data = request.json

    XRequestID, XCorrelationID, XBusinessCorrelationId, XWorkflowCorrelationId = setHeaderValues(request.headers)

    if authorized(request.headers['Authorization']) == False:
        return jsonify({}), 401, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./verification/400.json'):
        error400 = []
        with open('./verification/400.json', 'r') as e400:
            error400 = json.load(e400)
        return jsonify(error400), 400, { 
            'X-Request-ID': XRequestID, 
            'X-Correlation-ID': XCorrelationID,
            'X-Messages': 'true',
            'X-BusinessCorrelationId': XBusinessCorrelationId,
            'X-WorkflowCorrelationId': XWorkflowCorrelationId
        }

    if os.path.exists('./verification/403.json'):
        return jsonify({}), 403, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./verification/404.json'):
        return jsonify({}), 404, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./verification/413.json'):
        return jsonify({}), 413, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./verification/422.json'):
        return jsonify({}), 422, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    with open('./data/master.json', 'r') as mFile:
        master = json.load(mFile)

    recs = []
       
    for key in master:
        if (master[key]['LastName']).lower() == (data['LastName']).lower():
            recs.append(key)
            if data['FirstName'] != '' and (master[key]['FirstName']).lower() != (data['FirstName']).lower():
                recs.remove(key)
                break
            if data['TaxId'] != '' and master[key]['TaxId'] != data['TaxId']:
                recs.remove(key)
                break
            if data['DriverLicenseId'] != '' and master[key]['DriverLicenseId'] != data['DriverLicenseId']:
                recs.remove(key)
                break
            if data['DriverLicenseIssueState'] != '' and master[key]['DriverLicenseIssueState'] != data['DriverLicenseIssueState']:
                recs.remove(key)
                break
            if data['AccountId'] != '' and master[key]['AccountId'] != data['AccountId']:
                recs.remove(key)
                break
            if data['AccountType'] != '' and master[key]['AccountType'] != data['AccountType']:
                recs.remove(key)
                break

    products = []
    for item in recs:
        products.append({"Products": { "Code": "EDPP", "Description": "EDPP", "Id": item, "Status": "Active"}})

    status = []
    with open('./verification/messagestatuses.json', 'r') as mstatus:
        status = json.load(mstatus)

    return jsonify({
        "MessageStatuses": status,
        "Product": products
        }), 200, { 
                'X-Request-ID': XRequestID, 
                'X-Correlation-ID': XCorrelationID,
                'X-Messages': 'false',
                'X-BusinessCorrelationId': XBusinessCorrelationId,
                'X-WorkflowCorrelationId': XWorkflowCorrelationId
            }

@app.route('/api/v1/institutions/<InstitutionId>/environments/<InstitutionEnvironment>/products/<ProductCode>/EDPP/collection', methods = ['GET', 'DELETE'])
def collection(InstitutionId, InstitutionEnvironment, ProductCode):
    XRequestID, XCorrelationID, XBusinessCorrelationId, XWorkflowCorrelationId = setHeaderValues(request.headers)
    
    if authorized(request.headers['Authorization']) == False:
        return jsonify({}), 401, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./collection/400.json'):
        error400 = []
        with open('./collection/400.json', 'r') as e400:
            error400 = json.load(e400)
        return jsonify(error400), 400, { 
            'X-Request-ID': XRequestID, 
            'X-Correlation-ID': XCorrelationID,
            'X-Messages': 'true',
            'X-BusinessCorrelationId': XBusinessCorrelationId,
            'X-WorkflowCorrelationId': XWorkflowCorrelationId
        }

    if os.path.exists('./collection/403.json'):
        return jsonify({}), 403, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./collection/413.json'):
        return jsonify({}), 413, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./collection/422.json'):
        return jsonify({}), 422, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    product = ''
    if 'product' in request.args:
        product = request.args['product']
    personid = ''
    if 'personid' in request.args:
        personid = request.args['personid']
    if request.method == 'GET':
        try:
            with open('./data/' + personid + '.json') as file:
                contents = json.load(file)
        except FileNotFoundError:
            return jsonify({}), 404, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }
        return jsonify(contents), 200, { 
                'X-Request-ID': XRequestID, 
                'X-Correlation-ID': XCorrelationID,
                'X-Messages': 'false',
                'X-BusinessCorrelationId': XBusinessCorrelationId,
                'X-WorkflowCorrelationId': XWorkflowCorrelationId
            }
    elif request.method == 'DELETE':
        # Yes, this is bad code
        masterfile = open('./data/master.json', 'r')
        masterdata = json.load(masterfile)
        masterfile.close()
        masterfile = open('./data/master.json', 'w')
        del masterdata[personid]
        json.dump(masterdata, masterfile, indent=4)
        masterfile.close()
        with open('./data/' + personid + '.json') as file:
            contents = json.load(file)
        os.remove('./data/' + personid + '.json')

        return jsonify({
            "MessageStatuses": [
                {
                    "Code": "string",
                    "Category": "string",
                    "Description": "string",
                    "Element": "string",
                    "ElementValue": "string",
                    "Location": "string"
                }
            ],
            "DictionaryDataResponse": contents['DictionaryData']
            }), 200, { 
                'X-Request-ID': XRequestID, 
                'X-Correlation-ID': XCorrelationID,
                'X-Messages': 'false',
                'X-BusinessCorrelationId': XBusinessCorrelationId,
                'X-WorkflowCorrelationId': XWorkflowCorrelationId
            }

@app.route('/api/v1/institutions/<InstitutionId>/environments/<InstitutionEnvironment>/products/EDPP/status', methods = ['GET'])
def status(InstitutionId, InstitutionEnvironment):
    XRequestID, XCorrelationID, XBusinessCorrelationId, XWorkflowCorrelationId = setHeaderValues(request.headers)

    if authorized(request.headers['Authorization']) == False:
        return jsonify({}), 401, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./status/400.json'):
        error400 = []
        with open('./status/400.json', 'r') as e400:
            error400 = json.load(e400)
        return jsonify(error400), 400, { 
            'X-Request-ID': XRequestID, 
            'X-Correlation-ID': XCorrelationID,
            'X-Messages': 'true',
            'X-BusinessCorrelationId': XBusinessCorrelationId,
            'X-WorkflowCorrelationId': XWorkflowCorrelationId
        }

    if os.path.exists('./status/403.json'):
        return jsonify({}), 403, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./status/404.json'):
        return jsonify({}), 404, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./status/413.json'):
        return jsonify({}), 413, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./status/422.json'):
        return jsonify({}), 422, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    with open('./status/200.json', 'r') as file:
        contents = json.load(file)
    return jsonify(contents), 200, { 
                'X-Request-ID': XRequestID, 
                'X-Correlation-ID': XCorrelationID,
                'X-Messages': 'false',
                'X-BusinessCorrelationId': XBusinessCorrelationId,
                'X-WorkflowCorrelationId': XWorkflowCorrelationId
            }

@app.route('/api/v1/institutions/<InstitutionId>/environments/<InstitutionEnvironment>/products/EDPP/status/version', methods = ['GET'])
def version(InstitutionId, InstitutionEnvironment):
    XRequestID, XCorrelationID, XBusinessCorrelationId, XWorkflowCorrelationId = setHeaderValues(request.headers)

    if authorized(request.headers['Authorization']) == False:
        return jsonify({}), 401, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./version/400.json'):
        error400 = []
        with open('./version/400.json', 'r') as e400:
            error400 = json.load(e400)
        return jsonify(error400), 400, { 
            'X-Request-ID': XRequestID, 
            'X-Correlation-ID': XCorrelationID,
            'X-Messages': 'true',
            'X-BusinessCorrelationId': XBusinessCorrelationId,
            'X-WorkflowCorrelationId': XWorkflowCorrelationId
        }

    if os.path.exists('./version/403.json'):
        return jsonify({}), 403, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./version/404.json'):
        return jsonify({}), 404, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./version/413.json'):
        return jsonify({}), 413, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    if os.path.exists('./version/422.json'):
        return jsonify({}), 422, { 'X-Correlation-ID': XCorrelationID, 'X-Request-ID': XRequestID }

    with open('./version/200.json', 'r') as file:
        contents = json.load(file)
    return jsonify(contents), 200, { 
                'X-Request-ID': XRequestID, 
                'X-Correlation-ID': XCorrelationID,
                'X-Messages': 'false',
                'X-BusinessCorrelationId': XBusinessCorrelationId,
                'X-WorkflowCorrelationId': XWorkflowCorrelationId
            }

if __name__ == '__main__':
    app.run(host='0.0.0.0')