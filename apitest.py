import httplib, urllib, base64, json, time
from subprocess import call
###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = '7ffe7a3ee1844bc2aa3211c4f02bbc55'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "eastus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the eastus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'eastus.api.cognitive.microsoft.com'
guestname = "blank"
text_file = open("./database/face.dat", "r")
names = text_file.read().split(',')
uplimit = len(names)+1
# print names
# print len(names)

for i in range (1,uplimit): 

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
    filename = '/home/debian/ECE497_Final/database/'+str(i)+'.jpg'
    f = open(filename, "rb")
    body1 = f.read()
    f.close()
    
    body2 = ""
    filename = '/home/debian/ECE497_Final/1.jpg'
    f = open(filename, "rb")
    body2 = f.read()
    f.close()
    
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('eastus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body1, headers_octet)
        response1 = conn.getresponse()
        data1 = response1.read()
    
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed1 = json.loads(data1)
        # print ("Response:")
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        # print(parsed1[0]['faceId'])
        id1 = parsed1[0]['faceId']
        # conn.close()
        
        # conn = httplib.HTTPSConnection('eastus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body2, headers_octet)
        response2 = conn.getresponse()
        data2 = response2.read()
    
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed2 = json.loads(data2)
        # print ("Response:")
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        # print(parsed2[0]['faceId'])
        id2 = parsed2[0]['faceId']
        
        params3 = urllib.urlencode({
        })
        body = "{'faceId1':'"+id1+"','faceId2':'"+id2+"'}"
        # print(body)
        
        conn.request("POST", "/face/v1.0/verify?%s" %params3, body, headers_json)
        response = conn.getresponse()
        data = response.read()
    
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        # print ("Response:")
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        # print(parsed['isIdentical'])
        if(parsed['isIdentical'] == True):
            guestname = names[i-1]
            # print("WELCOME "+names[i-1])
            call(["convert", "1.jpg", "-background", "Khaki", "-pointsize", "30", "label:Welcome "+guestname+"!", 
                    "-gravity", "Center", "-append", "anno_label.jpg"])
            call(["sudo", "fbi", "-noverbose", "-T", "1", "-a", "anno_label.jpg"])
            break
        else:
            if(i == uplimit-1):
                call(["convert", "1.jpg", "-background", "Khaki", "-pointsize", "30", "label:Hmm... Can't recognize you.\nTry again!", 
                         "-gravity", "Center", "-append", "anno_label.jpg"])
                call(["sudo", "fbi", "-noverbose", "-T", "1", "-a", "anno_label.jpg"])
                conn.close()
    
    except Exception as e:
        call(["convert", "1.jpg", "-background", "Khaki", "-pointsize", "30", "label:Sorry we can't find your face\nPlease make sure your face is clear \nand try again!", 
                 "-gravity", "Center", "-append", "anno_label.jpg"])
        call(["sudo", "fbi", "-noverbose", "-T", "1", "-a", "anno_label.jpg"])
        break

    

text_file.close()    
