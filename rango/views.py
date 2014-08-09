
# from django.http import HttpResponse
from django.template import RequestContext
import time
import datetime as Datetime
from datetime import datetime
from rango.models import Category,Page,decode_url,UserProfile,User
from rango.forms import CategoryForm,UserForm,UserProfileForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from rango.bing_search import run_query




def index(request):
    context = RequestContext(request)
    if request.session.get('last_visit'):
                # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
  

    # Render and return the rendered response back to the user.
    return render_to_response('rango/index.html',get_cat_list(), context)


def category(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_cat_list()['cat_list']
    category_name = decode_url(category_name_url)

    context_dict = {'cat_list': cat_list, 'category_name': category_name}

    try:
        category = Category.objects.get(name=category_name)

                # Add category to the context so that we can access the id and likes
        context_dict['category'] = category

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
    except Category.DoesNotExist:
                pass

    return render_to_response('rango/category.html', context_dict, context)
 
def page(request,page_title_url):
    context=RequestContext(request)
    page_title=page_title_url.replace('_','')
    context_dict={'page_title':page_title}
    try:
        page=Page.objects.filter(page=page)
    except Page.DoesNotExist:
        pass
    return render_to_response('rango/page.html',context_dict,context)  

def rango(request):
    current_time=time.asctime()      
    return render_to_response('rango/rango.html',{'current_time':current_time},)

def static(request):
    context=RequestContext(request)
    context_dict={'boldmessage':'ths is static page.'}
    return render_to_response('rango/static.html',context_dict,context)

def about(request):
    context=RequestContext(request)
    wake_up_time=time_difference()
    if request.session.get('last_visit'):
        last_visit_time=request.session.get('last_visit')
        count =request.session.get('visits')
        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] += 1
            request.session['last_visit'] = str(datetime.now())

    else:
        last_visit_time=False
        count = 0
    condict={'wake_time':wake_up_time, 'count':count,'last_visit':last_visit_time}   
          
          
        
    
    return render_to_response('rango/about.html',condict,context)

def time_difference():
    a=time.localtime()
    b=Datetime.datetime.now()
    seconds=(b-Datetime.datetime(a[0],a[1],a[2],2,0,0,0)).seconds
    hours=seconds//60//60
    minutes=seconds//60%60
    seconds=seconds%60
    return '%s hours %s minutes %s seconds'%(hours,minutes,seconds)

def add_category(request):
    context=RequestContext(request)
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form=CategoryForm()
        
    return render_to_response('rango/add_category.html',{'form':form},context)

from rango.forms import PageForm

def add_page(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)
            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('rango/add_category.html', {}, context)

            # Also, create a default value for the number of views.
            page.views = 0
            # With this, we can then save our new model instance.
            page.save()
            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()
    return render_to_response( 'rango/add_page.html',
            {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form},
             context)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.

    return render_to_response(
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    # If the request is a HTTP POST, try to pull out the relevant information. 
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('rango/log_in.html', {}, context)
    
def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")    
    else:
        return HttpResponse("You are not logged in.")
    
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')


def search(request):
    context = RequestContext(request)
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render_to_response('rango/search.html', {'result_list': result_list}, context)




@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = get_cat_list()['cat_list']
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('rango/profile.html', context_dict, context)

    
    
def track_url(request):
    context = RequestContext(request)
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return HttpResponseRedirect(url)

from django.contrib.auth.decorators import login_required

@login_required
def like_category(request):
    context = RequestContext(request)
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        if category:
            likes = category.likes + 1
            category.likes =  likes
            category.save()

    return HttpResponse(likes)
def suggest_category(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']

        cat_list = get_category_list(8, starts_with)

        return render_to_response('rango/category_list.html', {'cat_list': cat_list }, context)
      
        


    
def decode_url(name_url):
    return name_url.replace('_',' ')
def encode_url(url):
    return url.replace(' ','_')
def get_cat_list():   
    category_list = Category.objects.all()
    for category in category_list:
        category.url = encode_url(category.name)
    context_dict = {'categories': category_list}
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
    context_dict['cat_list']=category_list
    
    return context_dict
def get_category_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
                cat_list = Category.objects.filter(name__istartswith=starts_with)
        else:
                cat_list = Category.objects.all()

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        for cat in cat_list:
                cat.url = encode_url(cat.name)

        return cat_list





