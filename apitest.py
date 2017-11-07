import httplib, urllib, base64, json, time

###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = '97ce17233dbb4b9ab1189e344cf63dd4'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'westcentralus.api.cognitive.microsoft.com'

text_file = open("face.dat", "r")
names = text_file.read().split(',')
print names
print len(names)

for i in range (1,5): 
    print("wsb"+ str(i))

    # Request headers.
    headers_octet = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    
    headers_json = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    
    # Request parameters.
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': '',
    })
    
    # The URL of a JPEG image to analyze.
    # body1 = "{'url':'http://hairstyles.thehairstyler.com/hairstyle_views/front_view_images/4603/original/Zach-Quinto.jpg'}"
    # body2 = "{'url':'https://d24v5oonnj2ncn.cloudfront.net/wp-content/uploads/2015/06/11095458/Eli-Roth.jpg'}"
    
    body1 = ""
    filename = '/home/debian/final/ECE497_Final/'+str(i)+'.jpg'
    f = open(filename, "rb")
    body1 = f.read()
    f.close()
    
    body2 = ""
    filename = '/home/debian/final/1.jpg'
    f = open(filename, "rb")
    body2 = f.read()
    f.close()
    
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body1, headers_octet)
        response1 = conn.getresponse()
        data1 = response1.read()
    
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed1 = json.loads(data1)
        print ("Response:")
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        print(parsed1[0]['faceId'])
        id1 = parsed1[0]['faceId']
        # conn.close()
        
        # conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body2, headers_octet)
        response2 = conn.getresponse()
        data2 = response2.read()
    
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed2 = json.loads(data2)
        print ("Response:")
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        print(parsed2[0]['faceId'])
        id2 = parsed2[0]['faceId']
        
        params3 = urllib.urlencode({
        })
        body = "{'faceId1':'"+id1+"','faceId2':'"+id2+"'}"
        print(body)
        
        conn.request("POST", "/face/v1.0/verify?%s" %params3, body, headers_json)
        response = conn.getresponse()
        data = response.read()
    
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))
        # print(parsed['isIdentical'])
        if(parsed['isIdentical'] == True):
            print("WELCOME "+names[i-1])
            break
        else:
            conn.close()
    
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    time.sleep(2)
    

text_file.close()    
# conn.close()