
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
        
        # Validation
        # if len(password) < 8:
        #     return render(request,'register.html',{'error':"Password must be at least 8 characters"})
        # if not phone.isdigit() or len(phone) != 10:
        #     return render(request,'register.html',{'error':"Phone number must be exactly 10 digits"})
        
        fs = FileSystemStorage()
        filename = fs.save(id_proof.name,id_proof)
        reg=registerr(name=name,email=email,password=password,phone=phone,student_id=filename,status="active")
        reg.save()
        return render(request,'index.html',{'message':"Registration Successful"})
    else:
        return render(request,'register.html')




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
        description=request.POST.get('description')
        location=request.POST.get('location')
        categoryname=request.POST.get('categoryname')
        date=request.POST.get('date')
        id_proof=request.FILES['item_image']
        fs = FileSystemStorage()
        filename = fs.save(id_proof.name,id_proof)
        image_features = pickle.dumps(
            extract_features(fs.path(filename))
        )
        reg=lost_table(itemname=itemname,description=description,location=location,categoryname=categoryname,date=date,item_image=filename,status="pending",user_id=request.session['uid'], image_features=image_features)
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
        description = request.POST.get('description')
        location = request.POST.get('location')
        categoryname = request.POST.get('categoryname')
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
            description=description,
            location=location,
            categoryname=categoryname,
            date=date,
            item_image=filename,
            status="pending",
            user_id=request.session['uid'],
            image_features=found_features_blob
        )

        # Compare with LOST items
        lost_items = lost_table.objects.exclude(image_features=None,status="accepted")

        for lost in lost_items:
            lost_features = pickle.loads(lost.image_features)

            score = cosine_similarity(
                found_features.reshape(1, -1),
                lost_features.reshape(1, -1)
            )[0][0]
            print("Similarity score with lost item ID", lost.id, ":", score, flush=True)

            if score >= 0.40:
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
    #query = request.GET.get('q')
    # show only active lost items (exclude accepted)
    lost_items = lost_table.objects.filter(user_id=request.session['uid'])

    # if query:
    #     sel = sel.filter(
    #         Q(itemname__icontains=query) |
    #         Q(title__icontains=query) |
    #         Q(description__icontains=query) |
    #         Q(location__icontains=query) |
    #         Q(item_type__icontains=query)
    #     )

    # for i in lost_items:
    #     for j in sel:
    #         if str(i.user_id) == str(j.id):
    #             i.user_id = j.name

    found_items = found_table.objects.filter(user_id=request.session['uid'])

    # if query:
    #     sel = sel.filter(
    #         Q(itemname__icontains=query) |
    #         Q(title__icontains=query) |
    #         Q(description__icontains=query) |
    #         Q(location__icontains=query) |
    #         Q(item_type__icontains=query)
    #     )

    # for i in found_items:
    #     for j in sel:
    #         if str(i.user_id) == str(j.id):
    #             i.user_id = j.name
    
    return render(request,'profile.html',{'i':sel,"lost_items":lost_items,"found_items":found_items})



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

def viewreq(request):
    uid = request.session.get('uid')
    is_admin = request.session.get('admin') == 'admin'
    # IMAGE-BASED SEARCH
    if request.method == "POST" and request.FILES.get("search_image"):
        print("Entered image search", flush=True)

        uploaded_image = request.FILES["search_image"]
        # Only search active lost items (exclude those marked accepted)
        items = lost_table.objects.exclude(image_features=None).exclude(status='accepted').distinct()

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
            "image_search": True,
            "uid": uid,
            "is_admin": is_admin
        })

    # TEXT SEARCH / DEFAULT VIEW
    else:
        query = request.GET.get('q')
        # show only active lost items (exclude accepted)
        sel = lost_table.objects.exclude(status='accepted')

        if query:
            sel = sel.filter(
                Q(itemname__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )

        user = registerr.objects.all()
        for i in sel:
            for j in user:
                if str(i.user_id) == str(j.id):
                    i.owner_name = j.name

        return render(request, "view_lost_item.html", {
            "result": sel,
            "image_search": False,
            "uid": uid,
            "is_admin": is_admin
        })

def viewfound(request):
    uid = request.session.get('uid')
    is_admin = request.session.get('admin') == 'admin'
    uid = request.session.get('uid')

    # IMAGE-BASED SEARCH
    if request.method == "POST" and request.FILES.get("search_image"):
        print("Entered image search", flush=True)

        uploaded_image = request.FILES["search_image"]
        # Only search active found items (exclude those marked completed or with an accepted match)
        items = found_table.objects.exclude(image_features=None).exclude(status='accepted').exclude(found_matches__request_status='accepted').distinct()

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
            "image_search": True,
            "uid": uid,
            "is_admin": is_admin
        })

    # TEXT SEARCH / DEFAULT VIEW
    else:
        query = request.GET.get('q')
        # show only active found items (exclude completed or already-accepted matches)
        sel = found_table.objects.exclude(status='accepted').exclude(found_matches__request_status='accepted').distinct()

        if query:
            sel = sel.filter(
                Q(itemname__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )

        user = registerr.objects.all()
        for i in sel:
            for j in user:
                if str(i.user_id) == str(j.id):
                    i.owner_name = j.name

        return render(request, "view_found_item.html", {
            "result": sel,
            "image_search": False,
            "message": request.GET.get('msg', ""),
            "uid": uid,
            "is_admin": is_admin
        })
    
def view_matches_for_lost(request):
    # Only show matches for lost items owned by the current user
    uid = request.session.get('uid')
    if not uid:
        return redirect(login)

    # Handle user making a request from this view
    if request.method == 'POST':
        match_id = request.POST.get('match_id')
        if match_id:
            try:
                match = item_match.objects.select_related('lost_item').get(id=match_id)
            except item_match.DoesNotExist:
                return redirect(view_matches_for_lost)

            # Only the owner of the lost item can request
            if str(match.lost_item.user_id) == str(uid):
                # Only set to requested if it's not already requested or accepted
                if match.request_status not in ('requested', 'accepted'):
                    try:
                        requester = registerr.objects.get(id=uid)
                        match.request_status = 'requested'
                        match.requested_by = requester.name
                        match.save()
                    except registerr.DoesNotExist:
                        match.request_status = 'requested'
                        match.save()
        return redirect(view_matches_for_lost)

    matches = item_match.objects.filter(
        lost_item__user_id=str(uid)
    ).exclude(request_status='accepted').select_related('found_item', 'lost_item').order_by('-similarity_score')

    # Convert similarity score to percentage for display (template shows a % sign)
    for m in matches:
        try:
            m.similarity_score = round(float(m.similarity_score) * 100, 2)
        except Exception:
            pass

    return render(request, 'matched_items.html', {
        'matches': matches
    })


def viewmatched(request):
    """Admin view to see all matched items."""
    if not request.session.get('admin'):
        return redirect(login)

    matches = item_match.objects.all().select_related('found_item', 'lost_item').order_by('-matched_on')

    # Convert similarity score to percentage for display
    for m in matches:
        try:
            m.similarity_score = round(float(m.similarity_score) * 100, 2)
        except Exception:
            pass

    return render(request, 'view_matched.html', {
        'matches': matches
    })


def request_match(request, found_id):
    """Show user's lost items to select one for requesting a match or handle the POST that creates/updates the request."""
    uid = request.session.get('uid')
    if not uid:
        return redirect(login)

    try:
        found_item = found_table.objects.get(id=found_id)
    except found_table.DoesNotExist:
        return redirect(viewfound)

    user_lost_items = lost_table.objects.filter(user_id=str(uid))

    # If no lost items for this user, redirect back with message
    if not user_lost_items.exists():
        return redirect(f"/viewfound?msg=No+lost+items+found.+Please+add+a+lost+item.")

    if request.method == 'POST':
        lost_id = request.POST.get('lost_item_id')
        try:
            lost_item = lost_table.objects.get(id=lost_id, user_id=str(uid))
        except lost_table.DoesNotExist:
            return redirect(viewfound)

        # compute similarity if possible
        sim = 0.0
        try:
            if found_item.image_features and lost_item.image_features:
                f_feat = pickle.loads(found_item.image_features)
                l_feat = pickle.loads(lost_item.image_features)
                sim = cosine_similarity(
                    f_feat.reshape(1, -1),
                    l_feat.reshape(1, -1)
                )[0][0]
        except Exception:
            sim = 0.0

        # Create or update match and mark request_status as 'requested'
        requester_name = None
        try:
            requester = registerr.objects.get(id=uid)
            requester_name = requester.name
        except registerr.DoesNotExist:
            pass

        match, created = item_match.objects.get_or_create(
            lost_item=lost_item,
            found_item=found_item,
            defaults={
                'similarity_score': round(float(sim), 4),
                'request_status': 'requested',
                'requested_by': requester_name,
            }
        )

        if not created:
            match.request_status = 'requested'
            match.requested_by = requester_name or match.requested_by
            match.similarity_score = round(float(sim), 4)
            match.save()

        # Redirect to user's matches page
        return redirect('/viewlostmatch')

    return render(request, 'select_lost_for_match.html', {
        'found_item': found_item,
        'lost_items': user_lost_items
    })


def view_received_requests(request):
    """Show incoming requests for found items uploaded by the current user."""
    uid = request.session.get('uid')
    if not uid:
        return redirect(login)

    requests_qs = item_match.objects.filter(
        found_item__user_id=str(uid),
        request_status='requested'
    ).select_related('found_item', 'lost_item')

    # Convert similarity to percentage for display
    for m in requests_qs:
        try:
            m.similarity_score = round(float(m.similarity_score) * 100, 2)
        except Exception:
            pass

    return render(request, 'received_requests.html', {
        'requests': requests_qs
    })


def accept_request(request, match_id):
    uid = request.session.get('uid')
    if not uid:
        return redirect(login)

    try:
        match = item_match.objects.select_related('found_item', 'lost_item').get(id=match_id)
    except item_match.DoesNotExist:
        return redirect(view_received_requests)

    # only owner of the found item can accept
    if str(match.found_item.user_id) != str(uid):
        return redirect(view_received_requests)

    match.request_status = 'accepted'
    match.save()

    # Mark both items as completed
    try:
        match.found_item.status = 'accepted'
        match.found_item.save()
    except Exception:
        logger.exception("Failed to update found_item status for match %s", match_id)

    try:
        match.lost_item.status = 'accepted'
        match.lost_item.save()
    except Exception:
        logger.exception("Failed to update lost_item status for match %s", match_id)

    return redirect(view_received_requests)


def reject_request(request, match_id):
    uid = request.session.get('uid')
    if not uid:
        return redirect(login)

    try:
        match = item_match.objects.select_related('found_item').get(id=match_id)
    except item_match.DoesNotExist:
        return redirect(view_received_requests)

    # only owner of the found item can reject
    if str(match.found_item.user_id) != str(uid):
        return redirect(view_received_requests)

    match.request_status = 'rejected'
    match.save()

    return redirect(view_received_requests)


def delete_lost(request, item_id):
    uid = request.session.get('uid')
    is_admin = request.session.get('admin') == 'admin'
    if not uid and not is_admin:
        return redirect(login)

    try:
        item = lost_table.objects.get(id=item_id)
    except lost_table.DoesNotExist:
        return redirect(viewreq)

    if not is_admin and str(item.user_id) != str(uid):
        return redirect(viewreq)

    # Delete associated matches
    item_match.objects.filter(lost_item=item).delete()
    item.delete()

    return redirect(viewreq)


def delete_found(request, item_id):
    uid = request.session.get('uid')
    is_admin = request.session.get('admin') == 'admin'
    if not uid and not is_admin:
        return redirect(login)

    try:
        item = found_table.objects.get(id=item_id)
    except found_table.DoesNotExist:
        return redirect(viewfound)

    if not is_admin and str(item.user_id) != str(uid):
        return redirect(viewfound)

    # Delete associated matches
    item_match.objects.filter(found_item=item).delete()
    item.delete()

    return redirect(viewfound)
