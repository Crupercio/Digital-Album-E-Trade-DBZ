from django.shortcuts import render, redirect, get_object_or_404
from .models import CollectibleItem, CustomerCollection, Order, Album, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm

# Create your views here.
def home(request):
    stickers = CustomerCollection.objects.all().filter(tradeable=True)

    return render(request,'home.html',{
        'stickers':stickers
    })

def about(request):
    return render(request,'about.html',{})

def category(request, foo):
    #Replace hyphens with spaces
    foo = foo.replace('-', ' ')
    try:
        #look catefory
        category = Category.objects.get(name=foo)
        stickers = CustomerCollection.objects.filter(tradeable=True, item__category=category)
        return render(request, 'category.html', {'stickers': stickers,
            'category': category})
    except:
        messages.success(request, ("That category does not exist!"))
        return redirect('home')


def sticker(request, pk):

    sticker = CollectibleItem.objects.get(id=pk)

    return render(request, 'sticker.html',{'sticker': sticker})

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in the user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have register successfully!"))
            return redirect('home')   
        else:
            messages.success(request, ("Oh no, there was a problem registering, please try again"))
            return redirect('register')
    else:
        return render(request, 'register.html',{'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
           

        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error. Please try again!"))
            return redirect('login')

    else:
        return render(request,'login.html',{})
    

def logout_user(request):
    messages.success(request, ("You have been logged out...Thanks"))
    logout(request)
    return redirect('home')

@login_required
def album_base_view(request):
    user = request.user  # Assuming the user is authenticated

    # Fetch all albums to display
    albums = Album.objects.all()

    # Pass the albums to the template
    context = {
        'albums': albums,
    }
    return render(request, 'album_base.html', context)

@login_required

def album_view(request, album_id, page_number=1):
    user = request.user  # Assuming the user is authenticated

    # Get the album by ID
    album = get_object_or_404(Album, id=album_id)

    # Retrieve collectibles for the selected page in the album
    all_items = CollectibleItem.objects.filter(album=album, page_number=page_number).order_by('position_on_page')

    # Retrieve the items that the user has collected
    collected_items = CustomerCollection.objects.filter(user=user, collected=True)
    collected_ids = collected_items.values_list('item__id', flat=True)  # List of collected item IDs

    # Retrieve the items that the user owns but has not collected
    owned_items = CustomerCollection.objects.filter(user=user, owned=True, collected=False)
    owned_ids = owned_items.values_list('item__id', flat=True)  # List of owned item IDs (not yet collected)

    # Pass the context to the template
    context = {
        'all_items': all_items,
        'collected_ids': collected_ids,
        'owned_ids': owned_ids,  # Pass the owned but not collected items
        'total_pages': CollectibleItem.objects.filter(album=album).values_list('page_number', flat=True).distinct(),
        'current_page': page_number,
        'album': album,
    }
    return render(request, 'album.html', context)


@login_required
def buy_item(request, item_id):
    item = get_object_or_404(CollectibleItem, id=item_id)
    user = request.user

    # Create an order for the item and associate it with the customer
    order = Order.objects.create(item=item, customer=user, quantity=1)
    order.shipped_status = True  # Assume the order is "shipped" immediately for simplicity
    order.save()

    # Check if the user already owns the item (but has not collected it yet)
    collection_entry, created = CustomerCollection.objects.get_or_create(user=user, item=item)

    # Update the collection status to reflect ownership
    collection_entry.owned = True  # The user now owns the item after purchase
    collection_entry.tradeable = True  # Still tradeable since it's not collected yet
    collection_entry.save()

    # Redirect back to the album page (for the corresponding album and page)
    return redirect('album_page', album_id=item.album.id, page_number=item.page_number)



# Example function to mark an item as collected
@login_required
def collect_item(user, item):
    # Find the user's collection entry for the item
    collection_entry = get_object_or_404(CustomerCollection, user=user, item=item)
    
    # Mark the item as collected
    collection_entry.mark_as_collected()

# View to handle collecting an item from the album page
@login_required
def collect_item_view(request, item_id):
    print("Collect item view triggered")  # Add this line to see if the view is reached
    if request.user.is_authenticated:
        item = get_object_or_404(CollectibleItem, id=item_id)

        # Check if the user already owns the item
        collection_entry = get_object_or_404(CustomerCollection, user=request.user, item=item)

        # Mark the item as collected
        collection_entry.mark_as_collected()

    # Redirect back to the album page
    return redirect('album_page', album_id=item.album.id, page_number=item.page_number)

