from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.db import connection
from . models import book
import os
import sys
from hyperlpr import *
import cv2
import json


from django.http import JsonResponse

def get_corsor():
    return connection.cursor()


def index(request):
    # cursor=get_corsor()
    # cursor.execute("select id ,bookname,author from t_book");
    # books=cursor.fetchall();

    #1. 使用orm添加数据
    b=book(name='C#高级',author='YHF')
    b.save()

    #使用ORM查询 1.主键条件查询  2.其他条件
    # books=book.objects.get(pk=1) # 1
    # print(books)
    books=book.objects.filter(name='C#高级')

    #删除
    # b=book.objects.get(pk=1)
    # book.delete(b)

    #修改数据
    b=book.objects.get(pk=2)
    b.name='JAVA高级'
    b.save()

    return render(request,"index.html",context={"s":"添加成功！","books":books});


def add(request):
    if request.method=='GET':
        return render(request, "add.html");
    else:
        name = request.POST["name"];
        author = request.POST["author"];
        cursor=get_corsor();
        cursor.execute("insert into t_book(id,bookname,author) values(null,'"+name+"','"+author+"')")
        return redirect(reverse('index'))

def detail(request,id):
    cursor=get_corsor()
    cursor.execute("select * from t_book where id="+id+"")
    book=cursor.fetchone()
    return render(request, "detail.html",context={"book":book});

def delete(request):
    if request.method=='POST':
        id=request.POST['id']
        cursor=get_corsor()
        cursor.execute("delete from t_book where id=%s" % id)
        return redirect(reverse('index'))



# def upload_file(request):
#     if request.method == "POST":    # 请求方法为POST时，进行处理
#         myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
#         if not myFile:
#             return HttpResponse("no files for upload!")
#         destination = open(os.path.join("E:\\upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
#         for chunk in myFile.chunks():      # 分块写入文件
#             destination.write(chunk)
#         destination.close()
#         return JsonResponse("{'status':1,'filename':"+myFile.name+"}")
#     else:
#         return JsonResponse("{'status':1,'filename':123}")

def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join("E:\\upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse("{'status':1,'filename':"+myFile.name+"}")

def upload(request):
    file = request.FILES.get('file', None)#request.FILES取文件对象,get取最后一个
    #get_list取出文件列表
    with open(file.name, 'wb') as f:
        for line in file:
            f.write(line)
    return JsonResponse({
        'status': 'OK',
        'msg': 'upload success'
    })


def Upload(request):
    if request.method == "GET":
        return render(request, "upload.html")

    elif request.method == "POST":
        # 获取普通input标签值，即文件名
        filname = request.POST.get('fileName')
        # 获取file类型的input标签值，即文件内容
        file = request.FILES.get('fileContent')

        # 获取文件后缀名
        postfix = file.name.split('.')[1]
        # 设置本地文件路径
        file_path = os.path.join('static', filname + '.' + postfix)

        # 将上传的文件写入本地目录
        f = open(file_path, "wb")
        for chunk in file.chunks():
            f.write(chunk)
        f.close()

    return JsonResponse({
        'status': 'OK',
        'msg': 'upload success'
    })


################################################车牌接口###############################################################
def plr(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("{'status':0,'license':'ABCDE','msg':'大哥图片呢'}")
        destination = open(os.path.join("E:\\upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        ##########识别#################
        image = cv2.imread("E:\\upload\\"+myFile.name+"")
        result=HyperLPR_PlateRecogntion(image)
        if len(result)==0:
            return HttpResponse("{'status':0,'license':'ABCDE','msg':'这太难了'}")
        else:
            print(result[0][0])
            return HttpResponse("{'status':1,'license':'"+result[0][0]+"','msg':'很棒！'}")



