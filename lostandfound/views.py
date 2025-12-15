
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
#from django.urls import reverse
from  django.core.files.storage import FileSystemStorage
from .models import *
from django.db.models import Q
import pickle
from utils.image_features import extract_features
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)
        

# def viewreq(request):
#     items = lost_table.objects.exclude(image_features=None)

#     # Image-based search
#     if request.method == "POST" and request.FILES.get("search_image"):
#         uploaded_image = request.FILES["search_image"]

#         temp_path = "media/temp_search.jpg"
#         with open(temp_path, "wb+") as f:
#             for chunk in uploaded_image.chunks():
#                 f.write(chunk)

#         query_features = extract_features(temp_path)

#         scored_items = []
#         for item in items:
#             db_features = pickle.loads(item.image_features)
#             score = cosine_similarity(
#                 query_features.reshape(1, -1),
#                 db_features.reshape(1, -1)
#             )[0][0]

#             if score > 0.7:  # similarity threshold
#                 scored_items.append((score, item))

#         scored_items.sort(reverse=True, key=lambda x: x[0])
#         items = [item for _, item in scored_items]

#     return render(request, "view_lost_item.html", {
#         "result": items
#     })


def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')

def reg(request):
    return render(request,'register.html')

def registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        id_proof=request.FILES['student_id']
        fs = FileSystemStorage()
        filename = fs.save(id_proof.name,id_proof)
        reg=registerr(name=name,email=email,password=password,phone=phone,student_id=filename,status="pending")
        reg.save()
    return render(request,'index.html',{'message':"Registration Successful"})




def login(request):
    return render(request,'login.html')

def addlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email == 'admin@gmail.com' and password =='admin':
        request.session['logintdetail'] = email
        request.session['admin'] = 'admin'
        return redirect(index)

    elif registerr.objects.filter(email=email,password=password).exists():
        userdetails=registerr.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['uid'] = userdetails.id
        
        return redirect(index)
        
    else:
        return render(request, 'login.html', {'success':'Invalid email id or Password'})
    
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first)




def cat(request):
    return render(request,'category.html')

def addcat(request):
    if request.method=="POST":
        category_name=request.POST.get('category_name')
        reg=cat_tbl(category_name=category_name)
        reg.save()
    return render(request,'index.html',{'message':"Category Added Successful"})

def lostt(request):
    sel=cat_tbl.objects.all()
    return render(request,'lost_item.html',{'result':sel})

def found(request):
    sel=cat_tbl.objects.all()
    return render(request,'found_item.html',{'result':sel})

def addlostt(request):
    if request.method=="POST":
        itemname=request.POST.get('itemname')
        title=request.POST.get('title')
        description=request.POST.get('description')
        item_type=request.POST.get('item_type')
        location=request.POST.get('location')
        category_id=request.POST.get('category_id')
        date=request.POST.get('date')
        id_proof=request.FILES['item_image']
        fs = FileSystemStorage()
        filename = fs.save(id_proof.name,id_proof)
        image_features = pickle.dumps(
            extract_features(fs.path(filename))
        )
        reg=lost_table(itemname=itemname,title=title,description=description,item_type=item_type,location=location,category_id=category_id,date=date,item_image=filename,status="pending",user_id=request.session['uid'], image_features=image_features)
        reg.save()
    return render(request,'index.html',{'message':"item Added Successful"})

# def addfound(request):
#     if request.method=="POST":
#         itemname=request.POST.get('itemname')
#         title=request.POST.get('title')
#         description=request.POST.get('description')
#         item_type=request.POST.get('item_type')
#         location=request.POST.get('location')
#         category_id=request.POST.get('category_id')
#         date=request.POST.get('date')
#         id_proof=request.FILES['item_image']
#         fs = FileSystemStorage()
#         filename = fs.save(id_proof.name,id_proof)
#         image_features = pickle.dumps(
#             extract_features(fs.path(filename))
#         )
#         reg=found_table(itemname=itemname,title=title,description=description,item_type=item_type,location=location,category_id=category_id,date=date,item_image=filename,status="pending",user_id=request.session['uid'], image_features=image_features)
#         reg.save()
#     return render(request,'index.html',{'message':"item Added Successful"})

def addfound(request):
    if request.method == "POST":

        itemname = request.POST.get('itemname')
        title = request.POST.get('title')
        description = request.POST.get('description')
        item_type = request.POST.get('item_type')
        location = request.POST.get('location')
        category_id = request.POST.get('category_id')
        date = request.POST.get('date')
        id_proof = request.FILES['item_image']

        fs = FileSystemStorage()
        filename = fs.save(id_proof.name, id_proof)
        image_path = fs.path(filename)

        # Extract features for FOUND item
        found_features = extract_features(image_path)
        found_features_blob = pickle.dumps(found_features)

        found_item = found_table.objects.create(
            itemname=itemname,
            title=title,
            description=description,
            item_type=item_type,
            location=location,
            category_id=category_id,
            date=date,
            item_image=filename,
            status="pending",
            user_id=request.session['uid'],
            image_features=found_features_blob
        )

        # Compare with LOST items
        lost_items = lost_table.objects.exclude(image_features=None)

        for lost in lost_items:
            lost_features = pickle.loads(lost.image_features)

            score = cosine_similarity(
                found_features.reshape(1, -1),
                lost_features.reshape(1, -1)
            )[0][0]

            if score >= 0.75:
                item_match.objects.get_or_create(
                    lost_item=lost,
                    found_item=found_item,
                    defaults={
                        'similarity_score': round(float(score), 4)
                    }
                )

        return render(request, 'index.html', {
            'message': "Item added successfully. Possible matches checked."
        })

    return render(request, 'index.html')




def profile(request):
    sel=registerr.objects.get(id=request.session['uid'] )
    return render(request,'profile.html',{'i':sel})



def update_myprofile(request, id):
    i = registerr.objects.get(id=id)   # MUST use get()
    return render(request, "update_profile.html", {"i": i})


def update_profile(request, id):

    i = registerr.objects.get(id=id)

    if request.method == "POST":
        i.name = request.POST.get('name')
        i.email = request.POST.get('email')
        i.phone = request.POST.get('phone')
        i.password = request.POST.get('password')
        i.status = request.POST.get('status')

        if request.FILES.get('student_id'):
            i.student_id = request.FILES.get('student_id')

        i.save()
        return redirect(profile)

    return render(request, "update_profile.html", {"i": i})

def viewstudentreq(request):
    sel=registerr.objects.all()
    return render(request,'viewstudent.html',{'result':sel})


def studreqreject(request,id):
    s=registerr.objects.get(id=id)
    s.status='rejected'
    s.save()
    return redirect(viewstudentreq)


def studreqaccept(request,id):
    s=registerr.objects.get(id=id)
    s.status='accepted'
    s.save()
    return redirect(viewstudentreq)

# def viewreq(request):
#     logger.info("Entered viewreq")
#     print("Entered viewreq")
#     # Image-based search
#     if request.method == "POST" and request.FILES.get("search_image"):
#         print("Entered image search")
#         uploaded_image = request.FILES["search_image"]

#         temp_path = "media/temp_search.jpg"
#         with open(temp_path, "wb+") as f:
#             for chunk in uploaded_image.chunks():
#                 f.write(chunk)

#         query_features = extract_features(temp_path)

#         scored_items = []
#         for item in items:
#             db_features = pickle.loads(item.image_features)
#             score = cosine_similarity(
#                 query_features.reshape(1, -1),
#                 db_features.reshape(1, -1)
#             )[0][0]

#             if score > 0.7:  # similarity threshold
#                 scored_items.append((score, item))

#         print("Scored Items:", scored_items)

#         scored_items.sort(reverse=True, key=lambda x: x[0])
#         items = [item for _, item in scored_items]

#         return render(request, "view_found_item.html", {
#             "result": scored_items,
#             "image_search": True
#         })

#         return render(request, "view_lost_item.html", {
#             "result": items
#         })
#     else:
#         query = request.GET.get('q')

#         sel = lost_table.objects.all()

#         if query:
#             sel = sel.filter(
#                 Q(itemname__icontains=query) |
#                 Q(title__icontains=query) |
#                 Q(description__icontains=query) |
#                 Q(location__icontains=query) |
#                 Q(item_type__icontains=query)
#             )

#         user = registerr.objects.all()

#         for i in sel:
#             for j in user:
#                 if str(i.user_id) == str(j.id):
#                     i.user_id = j.name

#         return render(request, 'view_lost_item.html', {
#             'result': sel
#         })
    
def viewreq(request):
    # IMAGE-BASED SEARCH
    if request.method == "POST" and request.FILES.get("search_image"):
        print("Entered image search", flush=True)

        uploaded_image = request.FILES["search_image"]
        items = lost_table.objects.exclude(image_features=None)

        temp_path = "media/temp_search.jpg"
        with open(temp_path, "wb+") as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        query_features = extract_features(temp_path)

        scored_items = []
        for item in items:
            db_features = pickle.loads(item.image_features)

            score = cosine_similarity(
                query_features.reshape(1, -1),
                db_features.reshape(1, -1)
            )[0][0]

            if score > 0.7:
                item.similarity_score = round(float(score) * 100, 2)  # percentage
                scored_items.append(item)

        print("Matched items:", len(scored_items), flush=True)

        # Sort by similarity score (descending)
        scored_items.sort(key=lambda x: x.similarity_score, reverse=True)

        return render(request, "view_lost_item.html", {
            "result": scored_items,
            "image_search": True
        })

    # TEXT SEARCH / DEFAULT VIEW
    else:
        query = request.GET.get('q')
        sel = lost_table.objects.all()

        if query:
            sel = sel.filter(
                Q(itemname__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(item_type__icontains=query)
            )

        user = registerr.objects.all()
        for i in sel:
            for j in user:
                if str(i.user_id) == str(j.id):
                    i.user_id = j.name

        return render(request, "view_lost_item.html", {
            "result": sel,
            "image_search": False
        })

def viewfound(request):
    # IMAGE-BASED SEARCH
    if request.method == "POST" and request.FILES.get("search_image"):
        print("Entered image search", flush=True)

        uploaded_image = request.FILES["search_image"]
        items = found_table.objects.exclude(image_features=None)

        temp_path = "media/temp_search.jpg"
        with open(temp_path, "wb+") as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        query_features = extract_features(temp_path)

        scored_items = []
        for item in items:
            db_features = pickle.loads(item.image_features)

            score = cosine_similarity(
                query_features.reshape(1, -1),
                db_features.reshape(1, -1)
            )[0][0]

            if score > 0.7:
                item.similarity_score = round(float(score) * 100, 2)  # percentage
                scored_items.append(item)

        print("Matched items:", len(scored_items), flush=True)

        # Sort by similarity score (descending)
        scored_items.sort(key=lambda x: x.similarity_score, reverse=True)

        return render(request, "view_found_item.html", {
            "result": scored_items,
            "image_search": True
        })

    # TEXT SEARCH / DEFAULT VIEW
    else:
        query = request.GET.get('q')
        sel = found_table.objects.all()

        if query:
            sel = sel.filter(
                Q(itemname__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(item_type__icontains=query)
            )

        user = registerr.objects.all()
        for i in sel:
            for j in user:
                if str(i.user_id) == str(j.id):
                    i.user_id = j.name

        return render(request, "view_found_item.html", {
            "result": sel,
            "image_search": False
        })
    
def view_matches_for_lost(request):
    matches = item_match.objects.filter().select_related('found_item').order_by('-similarity_score')

    return render(request, 'matched_items.html', {
        'matches': matches
    })





def reqreject(request,id):
    s=lost_table.objects.get(id=id)
    s.status='rejected'
    s.save()
    return redirect(viewreq)

def reqaccept(request,id):
    s=lost_table.objects.get(id=id)
    s.status='accepted'
    s.save()
    return redirect(viewreq)


