'''A quick python program to grab the 2 tokens from Cisco IMC via XML, and then manually launch the Java Console without requiring Flash'''
import requests
import os

my_cimc = "192.168.20.2"
my_user = "admin"
my_pass = "C1sc01234"
response=""
requests.packages.urllib3.disable_warnings() 

data = """<aaaLogin inName='""" + my_user + """' inPassword='""" + my_pass + """'></aaaLogin>"""

try:
    response = requests.post('''https://''' + my_cimc + '''/nuova''', data=data, verify=False, timeout=10)
    aaa = response.content
    #print(response.content)
    my_cookie = str(aaa).split('''"''')[5]
    
    #data = '''<configResolveClass cookie="''' + my_cookie + '''" inHierarchical="false" classId="computeRackUnit"/>'''
    #
    #response2 = requests.post('https://10.18.180.14/nuova', data=data, verify=False)
    #print(response2.content)
    
    data = '''<aaaGetComputeAuthTokens  cookie="''' + my_cookie + '''" />'''
    response = requests.post('''https://''' + my_cimc + '''/nuova''', data=data, verify=False)
    
    bbb=response.content
    #print(response.content)
    out_tokens = str(bbb).split('''"''')[3]
    
    token1 = out_tokens.split(",")[0]
    token2= out_tokens.split(",")[1]
    #print(token1)
    #print(token2)
    
    print("attempting to run the following command which does require java to be installed on your mac...\n")
    my_command = '''javaws "https://''' + my_cimc + '''/kvm.jnlp?cimcAddr=''' + my_cimc + '''&tkn1=''' + token1 + '''&tkn2=''' + token2 + '''"'''
    print(my_command)
    
    os.system(my_command + " >/dev/null 2>&1")

except:
    response = "Did not get a proper response from " + my_cimc
    print(response)