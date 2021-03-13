from django.shortcuts import render,redirect
from django.http import HttpResponse
import owncloud
import os
import json
import requests
import ipfsApi          # ipfs api
from web3 import Web3   # web3 api
import xml.etree.ElementTree as ET
from .models import meta
from .models import TodoModel
from time import sleep
from requests.auth import HTTPBasicAuth


oc = owncloud.Client('http://192.168.43.204/owncloud/') 
oc.login('admin', '1234')
 #owncloud api



# Create your views here.
import hashlib

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

def home(request):
    return render(request,'base.html')
def index(request):
    # url = "http://192.168.43.204/owncloud/ocs/v1.php/cloud/activity?=json"

    # headers = {
    #     'authorization': "Basic YWRtaW46MTIzNA==",
    #     'cache-control': "no-cache",
    #     'postman-token': "fd9890a8-9075-b1d8-1f51-94d7e32e770c"
    #     }

    # response = requests.request("GET", url, headers=headers)
    user = val()
    passw  = pas()
    x = requests.get('http://192.168.43.204/owncloud/ocs/v1.php/cloud/activity', auth=HTTPBasicAuth(user, passw))
    response = x.text
    x = meta.objects.all()
    for i in x:
        if i.username==val():
            name=i.username+".txt"
    file1 = open(name,"w")
    file1.write(response)
    file1.close()
    
    metahash = hash_file(name)
    return render(request,'base.html')
def login(request):
    user = request.POST['uname']
    password = request.POST['psw']
    if user == 'auditor' and password == '1234':
        a="auditor"
        return render(request,'Auditor.html',{'output':a,})
    else :
        oc.login(user,password)
        global val
        def val():
            return user
        global pas
        def pas():
            return password
        name = "User"
        return render(request,'files.html',{'filename':name,})

def upload(request):
    myfile = request.POST['file']
    path = os.path.join('../../../',myfile)
    
    x = oc.put_file('testdir/',path)
    x1 = TodoModel.objects.all()
    flag=1
    for i in x1:
        if(i.task == myfile):
            flag=0
    if (flag==1):
        TodoModel(task=myfile).save()
    return redirect(request.META['HTTP_REFERER'])

def upload_page(request):
    obj = oc.list("./testdir",1)
    x=[]
    for i in obj:
        x.append(i.get_name())
    return render(request,'managefiles.html',{'filename':x,})
    

def upload_Files(request):
    name = "User"
    return render(request,'result.html',{'user':name})

def download(request):
    myfile = request.GET['f']
    print(myfile)
    path = 'testdir/'+myfile
    path1= '/home/akash/Desktop/ocDownloads/'+myfile
    oc.get_file(path,path1)
    sleep(5)   #delay of 5 seconds for popup
    return redirect(request.META['HTTP_REFERER'])

def old_deletetask(request,taskpk):
    
    x = TodoModel.objects.all()
    for i in x:
        if(i.id == taskpk):
            name = i.task
    path = os.path.join('testdir/',name)
    oc.delete(path)
    TodoModel.objects.filter(id=taskpk).delete()
    return redirect(request.META['HTTP_REFERER'])


def deletetask(request):
    filename = request.POST['filename']
    print(filename)
    path = os.path.join('testdir/',filename)
    oc.delete(path)
    obj = oc.list("./testdir",1)
    x=[]
    for i in obj:
        x.append(i.get_name())
    for j in x:
        print(j)
    return render(request,'managefiles.html',{'filename':x,})
    

def web(request):
    url = "http://192.168.43.204/owncloud/ocs/v1.php/cloud/activity?=json"

    headers = {
        'authorization': "Basic YWRtaW46MTIzNA==",
        'cache-control': "no-cache",
        'postman-token': "fd9890a8-9075-b1d8-1f51-94d7e32e770c"
        }

    response = requests.request("GET", url, headers=headers)

    response = response.text
    file1 = open("myfile.txt","w")
    file1.write(response)
    file1.close()
    metahash = hash_file("myfile.txt")
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    print(metahash)
    web3.eth.defaultAccount =web3.eth.accounts[0]

    abi = json.loads('[{"constant":true,"inputs":[],"name":"hash","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_hash","type":"string"}],"name":"store","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"retrieve","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]');

    address = '0x159D6587670eA260CF7DE0C904716ffB6D560352'
    contract =  web3.eth.contract(abi=abi,address=address)

    tx_hash1=contract.functions.store(metahash).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash1)
    return render(request,'web.html',{'res':tx_receipt,})

def retrive(request):
    address = request.POST.get('quantity')

    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    web3.eth.defaultAccount =web3.eth.accounts[0]

    abi = json.loads('[{"constant":true,"inputs":[],"name":"hash","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_hash","type":"string"}],"name":"store","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"retrieve","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]');

    #address = '0x159D6587670eA260CF7DE0C904716ffB6D560352'

    mycontract= web3.eth.contract(abi = abi, address=address)

    result = mycontract.functions.retrieve().call()

    return render(request,'retrieve.html',{'res':result,})

def validate(request):
    import ipfshttpclient
    api = ipfshttpclient.connect()
    HASH = request.POST.get('hash_addr')
    ipfs_data = api.cat(HASH)
    h = hashlib.sha1(ipfs_data)
    ipfshash = h.hexdigest()
    return render(request,'ipfsdata.html',{'res':ipfs_data,'ipfshash' : ipfshash})

def ipfs_add(request):
    url = "http://192.168.43.204/owncloud/ocs/v1.php/cloud/activity?=json"

    headers = {
        'authorization': "Basic YWRtaW46MTIzNA==",
        'cache-control': "no-cache",
        'postman-token': "fd9890a8-9075-b1d8-1f51-94d7e32e770c"
        }

    response = requests.request("GET", url, headers=headers)

    response = response.text
    file1 = open("myfile.txt","w")
    file1.write(response)
    file1.close()
    api = ipfsApi.Client('127.0.0.1', 5001)
    result = api.add('myfile.txt')
    newres = result['Hash']
    return render(request,'ipfsdata.html',{'res':newres,})

def getmeta(request):

    
    url = "http://192.168.43.204/owncloud/ocs/v1.php/cloud/activity"

    headers = {
        'authorization': "Basic YWRtaW46MTIzNA==",
        'cache-control': "no-cache",
        'postman-token': "fd9890a8-9075-b1d8-1f51-94d7e32e770c"
        }

    response = requests.request("GET", url, headers=headers)

    response = response.text
    '''import xml.etree.ElementTree as ET
    

    file1 = open("myfile.txt","w")
    file1.write(response)
    file1.close()    
    mytree = ET.parse('myfile.txt')
    myroot = mytree.getroot()
    data = myroot[1]
    file1 = open("myfile.txt","w")
    for x in data:
        for y in x:
            text = str(y.text)
            file1.write(text+'\n')
            
    file1.close()  '''
    file1 = open("myfile.txt","w")
    file1.write(response)
    file1.close()    
    return render(request,'home.html')

def validation(request):
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    web3.eth.defaultAccount =web3.eth.accounts[0]
    metahash = hash_file("myfile.txt")
    abi = json.loads('[{"constant":true,"inputs":[],"name":"hash","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_hash","type":"string"}],"name":"store","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"retrieve","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]');
    address = '0x159D6587670eA260CF7DE0C904716ffB6D560352'
    mycontract= web3.eth.contract(abi = abi, address=address)
    result = mycontract.functions.retrieve().call()
    # print(metahash)
    # print(result)
    
    if metahash==result:
        return render(request,'validation_status.html',{'res':'True'})
    else :
        return render(request,'validation_status.html',{'res':'False'})

def test(request):
    x = TodoModel.objects.all()
    print(x[0].task)
    return render(request,'test.html')

def test1(request):
    x = ['akash','puneeth','amit','sumegh']
    return render(request,'test1.html',{'list':x})

def testdelete(request):
    filename = request.POST['filename']
    
    return render(request,'result.html')

def test2(request):
    x = meta.objects.all()
    for i in x:
        if i.username==val():
            print(i.metadata)



