# -*- coding: utf-8 -*-
from django.http import JsonResponse
from news.models import new,cate,newsim,newbrowse
import time

# 获取每篇新闻的请求接口
def one(request):
    # 获取该新闻的具体信息
    newid = request.GET.get("newid")
    newone = new.objects.filter(new_id=newid)[0]
    # 将用户的点击新闻信息写入数据库
    uname = request.session["username"]
    if "username" not in request.session.keys():
        return JsonResponse({"code": 0})
    newbtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    newbrowse.objects.create(user_name=uname,new_id=newid,new_browse_time=newbtime).save()
    # 获取该新闻的相似新闻
    flag = "sim"
    newsim_list = newsim.objects.filter(new_id_base=newid).order_by("-new_correlation")[:5]
    # 如果相似新闻不存在，拿该类别下的热门新闻填充
    if newsim_list.__len__() ==0:
        newsim_list = new.objects.filter(new_cate_id=newone.new_cate).order_by("-new_seenum")[:5]
        flag = "hot"
    # 拼接相似新闻信息
    newsim_list_back = list()
    for sim_one in newsim_list:
        # 记录相关度，前端按照此值进行排序
        cor = 0.0
        if flag == "sim":
            sim_one_mess = new.objects.filter(new_id=sim_one.new_id_sim)[0]
            cor = sim_one.new_correlation
        elif flag == "hot":
            cor = sim_one.new_seenum
            sim_one_mess = sim_one
        newsim_list_back.append({
            "new_id": sim_one_mess.new_id,
            "new_title": sim_one_mess.new_title,
            "new_time": sim_one_mess.new_time,
            # "new_content": str(sim_one_mess.new_content),
            # "new_seenum": sim_one_mess.new_seenum,
            # "new_disnum": sim_one_mess.new_disnum,
            "new_cate": sim_one_mess.new_cate.cate_id,
            "new_cor" : cor
        })
    # 拼接总的新闻信息
    result = {
        "code":2,
        "new_id": newone.new_id,
        "new_title": newone.new_title,
        "new_time": newone.new_time,
        "new_content": str(newone.new_content),
        "new_seenum": newone.new_seenum,
        "new_disnum": newone.new_disnum,
        "new_cate": newone.new_cate.cate_name,
        "new_sim":newsim_list_back
    }
    return JsonResponse(result)

# 获取新闻的所属类别
def cates(request):
    if "username" not in request.session.keys():
        return JsonResponse({"code": 0})
    cateslist = cate.objects.all()
    result = dict()
    result["data"]=list()
    result["code"] = 2
    for cateone in cateslist:
        result["data"].append({
            "cate_id":cateone.cate_id,
            "cate_name":cateone.cate_name
        })
    return JsonResponse(result)