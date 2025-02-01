from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from admin_soft.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from .models import Post, Like, Comment
from .form import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
import razorpay 
from core.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
# Create your views here.
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import razorpay 
import json
from random import choice
import os
from django.contrib import messages
from core.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
# Create your views here.
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

# Create your views here.
# Initialize the Gemini API client with your API key
genai.configure(api_key="AIzaSyC_4JPl40GzSFWMNGTKSXcK8ELQjpOC5b0")
model = genai.GenerativeModel("gemini-1.5-flash")

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('communityFeed')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form,'segment':'createPost'})

# View for displaying the feed (all posts)
@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts, 'segment':'communityFeed'})

# View for liking a post
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # If the post is already liked, unlike it
    return redirect('communityFeed')

# View for adding a comment
@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('communityFeed')

def payment(request):
  data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
  payment = client.order.create(data=data)
  print(payment)
  payment_order_id=payment['id']
  context={
    'amount': 100, 'api_key':RAZORPAY_API_KEY, 'order_id':payment_order_id
  }
  return render(request,'payment.html',context)
# Pages

import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings
import seaborn as sns

csv_path = os.path.join(settings.BASE_DIR, 'store.csv')

# Load the data
data = pd.read_csv(csv_path)

# Create a directory to store the plots if it doesn't exist
plot_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# Helper function to save plots
def save_plot(fig, filename):
    path = os.path.join(plot_dir, filename)
    fig.savefig(path)
    plt.close(fig)

def generate_statistics():
    # 1. Product Distribution by Gender
    fig1, ax1 = plt.subplots()
    data['gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax1)
    ax1.set_ylabel('')
    ax1.set_title('Product Distribution by Gender')
    save_plot(fig1, 'gender_distribution.png')

    # 2. Top 5 Most Common Article Types
    fig2, ax2 = plt.subplots()
    data['articleType'].value_counts().head(5).plot(kind='bar', ax=ax2)
    ax2.set_title('Top 5 Most Common Article Types')
    ax2.set_ylabel('Count')
    save_plot(fig2, 'top_article_types.png')

    # 3. Base Colour Popularity
    fig3, ax3 = plt.subplots()
    data['baseColour'].value_counts().head(10).plot(kind='bar', ax=ax3)
    ax3.set_title('Top 10 Base Colours')
    ax3.set_ylabel('Count')
    save_plot(fig3, 'base_colour_popularity.png')

    # 4. Product Availability by Season
    fig4, ax4 = plt.subplots()
    data['season'].value_counts().plot(kind='bar', ax=ax4)
    ax4.set_title('Product Availability by Season')
    ax4.set_ylabel('Count')
    save_plot(fig4, 'availability_by_season.png')

    # 5. Top 5 Most Popular Product Names
    fig5, ax5 = plt.subplots()
    data['productDisplayName'].value_counts().head(5).plot(kind='bar', ax=ax5)
    ax5.set_title('Top 5 Product Names')
    ax5.set_ylabel('Count')
    save_plot(fig5, 'top_product_names.png')

    # 6. Usage Distribution (Casual vs. Formal)
    fig6, ax6 = plt.subplots()
    data['usage'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax6)
    ax6.set_ylabel('')
    ax6.set_title('Usage Distribution (Casual vs. Formal)')
    save_plot(fig6, 'usage_distribution.png')

    # 7. Gender Preference for Specific Article Types
    fig7, ax7 = plt.subplots()
    pd.crosstab(data['articleType'], data['gender']).head(10).plot(kind='bar', ax=ax7)
    ax7.set_title('Gender Preference for Article Types')
    ax7.set_ylabel('Count')
    save_plot(fig7, 'gender_article_types.png')

    # 8. Article Types per Season
    fig8, ax8 = plt.subplots()
    pd.crosstab(data['articleType'], data['season']).plot(kind='bar', stacked=True, ax=ax8)
    ax8.set_title('Article Types per Season')
    ax8.set_ylabel('Count')
    save_plot(fig8, 'article_types_per_season.png')

    # 9. Base Colour Preference by Gender
    fig9, ax9 = plt.subplots()
    pd.crosstab(data['baseColour'], data['gender']).head(10).plot(kind='bar', ax=ax9)
    ax9.set_title('Base Colour Preference by Gender')
    ax9.set_ylabel('Count')
    save_plot(fig9, 'base_colour_gender.png')

    # 10. Missing Values Visualization
    fig10, ax10 = plt.subplots()
    sns.heatmap(data.isnull(), cbar=False, cmap='viridis', ax=ax10)
    ax10.set_title('Missing Values Heatmap')
    save_plot(fig10, 'missing_values_heatmap.png')

# Call the function to generate the plots




def index(request):
    # Pass the image paths to the template
    img_urls = get_all_image_urls()
    context = {
        'segment': 'index',
        'image_urls': img_urls,
    }

    print(context)

    return render(request, 'pages/index.html', context)

def billing(request):
  return render(request, 'pages/billing.html', { 'segment': 'billing' })

# Chatbot view
def chatbot(request):
    return render(request, 'pages/chatbot.html', { 'segment': 'chatbot' })

# ECO FRIENDLY PRODUCT CART
def eco_friendly_view(request):
    return render(request, 'pages/ecofriendly.html') 

PRODUCTS = [
    {'id': 1, 'name': 'Coco Cola', 'price': 39.99, 'image': 'img/cococola.jpg'},
    {'id': 2, 'name': 'Samsung Watch', 'price': 49.99, 'image': 'img/samsung.jpg'},
    {'id': 3, 'name': 'JBL Speaker', 'price': 89.99, 'image': 'img/jbl.jpg'},
    {'id': 4, 'name': 'Whey Protien', 'price': 24.99, 'image': 'img/whey.jpg'},
    {'id': 5, 'name': 'Power Bar', 'price': 59.99, 'image': 'img/powerbar.jpg'},
    {'id': 6, 'name': 'Nike Shoes', 'price': 69.99, 'image': 'img/nike.jpgx`'},
    {'id': 7, 'name': 'Red Bull', 'price': 79.99, 'image': 'img/redbull.jpg'},
]

def product_list(request):
    # Render the product page with a list of products
    return render(request, 'pages/product_page.html', {'products': PRODUCTS, 'segment':'ecostore'})


from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def toggle_event_status(request, event_name):
    try:
        # Reference the specific event in Firebase using the event name
        event_ref = db.reference(f'Events/{event_name}')
        event_data = event_ref.get()

        if not event_data:
            return JsonResponse({'error': 'Event not found'}, status=404)

        # Toggle the event status
        new_status = 'live' if event_data.get('status') == 'close' else 'close'
        event_ref.update({'status': new_status})

        return JsonResponse({'status': new_status})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def add_to_cart(request, product_id):
    # Find the product by ID
    product = next((item for item in PRODUCTS if item['id'] == product_id), None)

    if product:
        # Get the current cart session or initialize a new cart
        cart = request.session.get('cart', [])
        
        # Add product to the cart
        cart.append(product)
        
        # Update the cart session
        request.session['cart'] = cart

    return redirect('ecostore')
def view_cart(request):
    # Retrieve cart from the session
    cart = request.session.get('cart', [])

    # Calculate total price of all items in the cart
    total_price = sum(item['price'] for item in cart)

    return render(request, 'pages/cart.html', {'cart': cart, 'total_price': total_price})

def remove_from_cart(request, product_id):
    # Retrieve cart from the session
    cart = request.session.get('cart', [])

    # Remove the product with the specified product_id
    cart = [item for item in cart if item['id'] != product_id]

    # Update the cart session
    request.session['cart'] = cart

    return redirect('cart')



























# Function to handle chatbot interaction
@csrf_exempt  # You may want to add proper CSRF protection in a real production app
def chat_with_gemini(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '')

        if user_input:
            try:
                # Send the user's input to the Gemini API
                response = model.generate_content("Give response in 5 to 10 lines for the following question. The question is as follows: "+user_input)
                print(response.text)
                gemini_response = response.text  # Get the bot's last response

                # Return the response as JSON
                return JsonResponse({
                    'status': 'success',
                    'message': gemini_response
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    })

# Load clothes data from the JSON file
def load_clothes_data():
    json_file_path = os.path.join(os.path.dirname(__file__), 'clothes_data.json')
    with open(json_file_path, 'r') as f:
        clothes_data = json.load(f)
    return clothes_data


from random import sample

def recommend_clothes(clothes_data, clothing_type, season, color, max_results=5):
    # Convert the dict into a list of items
    clothes_list = list(clothes_data.values())
    
    # Filter the dataset based on exact matches
    exact_matches = [
        item for item in clothes_list
        if item['type'].lower() == clothing_type.lower() and
           item['season'].lower() == season.lower() and
           item['color'].lower() == color.lower()
    ]
    
    # If exact matches found, return up to max_results
    if exact_matches:
        return sample(exact_matches, min(len(exact_matches), max_results))
    
    # If no exact match, relax the color filter
    close_matches = [
        item for item in clothes_list
        if item['type'].lower() == clothing_type.lower() and
           item['season'].lower() == season.lower()
    ]
    
    # If close matches found, return up to max_results
    if close_matches:
        return sample(close_matches, min(len(close_matches), max_results))
    
    # If no matches at all, return an empty list
    return []



def get_clothing_recommendation(request):
    if request.method == 'POST':
        # Get user input from POST request
        clothing_type = request.POST.get('clothing_type')
        season = request.POST.get('season')
        color = request.POST.get('color')
        
        # Load clothes data from the JSON file
        clothes_data = load_clothes_data()
        
        # Call the recommendation function
        recommended_items = recommend_clothes(clothes_data, clothing_type, season, color)
        
        if recommended_items:
            # Render the recommendation with the list of items
            return render(request, 'pages/recommendation.html', {
                'items': recommended_items,
                'segment': 'recommend'
            })
        else:
            # If no match is found, return a message
            return render(request, 'pages/recommendation.html', {
                'message': 'No suitable clothing items found based on your preferences.',
                'segment': 'recommend'
            })
    
    # If GET request, render the input form
    return render(request, 'pages/clothing_form.html', { 'segment': 'recommend' })


def passItOver_view(request):
    try:
        # Reference to Firebase Realtime Database
        donate_ref = db.reference('donateItems')
        resell_ref = db.reference('resellItems')

        # Fetch donateItems and resellItems from Firebase
        donate_items = donate_ref.get()
        resell_items = resell_ref.get()

        # If there's no data, make sure we don't pass None
        donate_items = donate_items if donate_items else {}
        resell_items = resell_items if resell_items else {}

        # Pass the data to the template
        context = {
            'segment': 'passitover',
            'donate_items': donate_items,
            'resell_items': resell_items,
        }

        return render(request, 'pages/passItOver.html', context)
    
    except Exception as e:
        return render(request, 'pages/passItOver.html', {
            'segment': 'passitover',
            'error': str(e)
        })


def resellItem(request):
   return render(request, 'pages/resellItemForm.html')

def donateItem(request):
   return render(request, 'pages/donateItemForm.html')


# Add Resell and Donate Item

from firebase_admin import storage, db

import hashlib
import uuid

# def addItem(request):
#     if request.method == 'POST':
#         try:
#             # Get data from request
#             item_name = request.POST.get('item_name')
#             item_cost = request.POST.get('item_cost')
#             item_type = request.POST.get('item_type')
#             item_image = request.FILES.get('item_image')
#             action_type = request.POST.get('action_type')  # either 'resell' or 'donate'
            
#             # Generate a unique filename for the image
#             filename = f"{uuid.uuid4()}_{item_image.name}"

#             # Upload image to Firebase Storage
#             bucket = storage.bucket()
#             blob = bucket.blob(f"items/{filename}")
#             blob.upload_from_file(item_image, content_type=item_image.content_type)
#             blob.make_public()  # Make the image publicly accessible
#             image_url = blob.public_url

#             # Prepare data to store in Firebase Realtime Database
#             data = {
#                 'item_name': item_name,
#                 'item_cost': item_cost,
#                 'item_type': item_type,
#                 'image_url': image_url,
#                 'action_type': action_type
#             }

#             # Add data to Firebase Realtime Database
#             ref = db.reference(f"{action_type}Items")  # action_type can be 'resell' or 'donate'
#             ref.push(data)  # Push the data into the appropriate node (resellItems or donateItems)

#             JsonResponse({"status": "success", "message": "Item added successfully", "data": data})

#             return redirect('/passItOver')

        
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)})

import hashlib
import uuid

def addItem(request):
    if request.method == 'POST':
        try:
            # Get data from request
            item_name = request.POST.get('item_name')
            item_cost = request.POST.get('item_cost')
            item_type = request.POST.get('item_type')
            item_image = request.FILES.get('item_image')
            action_type = request.POST.get('action_type')  # either 'resell' or 'donate'

            # Compute the hash of the image file (using SHA256 or MD5)
            hasher = hashlib.md5()
            for chunk in item_image.chunks():
                hasher.update(chunk)
            image_hash = hasher.hexdigest()

            # Check if the hash already exists in the database
            ref = db.reference(f"{action_type}Items")
            existing_items = ref.order_by_child('image_hash').equal_to(image_hash).get()

            if existing_items:
                return JsonResponse({"status": "error", "message": "Image already exists."})

            # Reset the file pointer to the beginning of the file before uploading
            item_image.seek(0)

            # Generate a unique filename for the image
            filename = f"{uuid.uuid4()}_{item_image.name}"

            # Upload image to Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob(f"items/{filename}")
            blob.upload_from_file(item_image, content_type=item_image.content_type)
            blob.make_public()  # Make the image publicly accessible
            image_url = blob.public_url

            # Prepare data to store in Firebase Realtime Database
            data = {
                'item_name': item_name,
                'item_cost': item_cost,
                'item_type': item_type,
                'image_url': image_url,
                'image_hash': image_hash,  # Store the hash in the database
                'action_type': action_type
            }

            # Add data to Firebase Realtime Database
            ref.push(data)  # Push the data into the appropriate node (resellItems or donateItems)

            JsonResponse({"status": "success", "message": "Item added successfully", "data": data})
            return redirect('/passItOver')


        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})




def tables(request):
  return render(request, 'pages/tables.html', { 'segment': 'tables' })

def vr(request):
  return render(request, 'pages/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'pages/rtl.html', { 'segment': 'rtl' })

def profile(request):
    try:
        print(request.session)
        # Reference to Firebase Realtime Database
        donate_ref = db.reference('donateItems')
        resell_ref = db.reference('resellItems')

        # Fetch donateItems and resellItems from Firebase
        donate_items = donate_ref.get()
        resell_items = resell_ref.get()

        # If there's no data, make sure we don't pass None
        donate_items = donate_items if donate_items else {}
        resell_items = resell_items if resell_items else {}

        # Pass the data to the template
        context = {
            'segment': 'profile',
            'donate_items': donate_items,
            'resell_items': resell_items,
        }
        return render(request, 'pages/profile.html', context)
    except Exception as e:
        return render(request, 'pages/profile.html', {
            'segment': 'passitover',
            'error': str(e)
        })


def logout_view(request):
    logout(request)
    request.session.pop('user_role', None)
    request.session.pop('user_email', None)
    return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm


def mirror(request):
   return render(request, 'pages/mirror.html', {'segment':'mirror'})


def wardrobe(request):
    try:
        closet_ref = db.reference(f"{request.user.id}_closet")

        # Fetch donateItems and resellItems from Firebase
        closet_items = closet_ref.get()

        # If there's no data, make sure we don't pass None
        closet_items = closet_items if closet_items else {}

        # Reference to the items_worn node in Firebase
        worn_items_ref = db.reference("items_worn")

        # Fetch all worn items
        worn_items = worn_items_ref.get()

        # If no items found, initialize as empty
        if not worn_items:
            worn_items = {}


        # Pass the data to the template
        context = {
            'segment': 'wardrobe',
            'closet_items': closet_items,
            'worn_items': worn_items,
        }

        return render(request, 'pages/wardrobe.html', context)
    
    except Exception as e:
        return render(request, 'pages/wardrobe.html', {
            'segment': 'wardrobe',
            'error': str(e)
        })
   

import hashlib
from django.http import JsonResponse

def add_dress(request):
    if request.method == 'POST':
        try:
            # Get data from request
            item_name = request.POST.get('item_name')
            item_type = request.POST.get('item_type')
            item_image = request.FILES.get('item_image')
            item_tag = request.POST.get('item_tag')  # either 'resell' or 'donate'

            # Read the image file and calculate its hash (MD5 in this case)
            image_hash = hashlib.md5(item_image.read()).hexdigest()
            item_image.seek(0)  # Reset file pointer after reading it for hash

            # Check if an image with the same hash already exists in Firebase
            ref = db.reference(f"{request.user.id}_closet")
            existing_items = ref.get()

            # Handle case where there are no existing items (NoneType)
            if existing_items is not None:
                # Iterate through existing items and check if the hash matches
                for key, value in existing_items.items():
                    if value.get('image_hash') == image_hash:
                        return JsonResponse({"status": "error", "message": "This image already exists in your wardrobe."})

            # Generate a unique filename for the image
            filename = f"{uuid.uuid4()}_{item_image.name}"

            # Upload image to Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob(f"items/{filename}")
            blob.upload_from_file(item_image, content_type=item_image.content_type)
            blob.make_public()  # Make the image publicly accessible
            image_url = blob.public_url

            # Prepare data to store in Firebase Realtime Database
            data = {
                'item_name': item_name,
                'item_type': item_type,
                'image_url': image_url,
                'item_tag': item_tag,
                'image_hash': image_hash  # Store the image hash to avoid duplicates in the future
            }

            # Add data to Firebase Realtime Database
            ref.push(data)  # Push the data into the user's closet

            JsonResponse({"status": "success", "message": "Item added successfully", "data": data})
            return redirect('wardrobe')

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return render(request, 'pages/add_dress.html')


import os
import cv2
import cvzone
from django.http import StreamingHttpResponse
from cvzone.PoseModule import PoseDetector

# Initialize video capture
cap = cv2.VideoCapture(0)
detector = PoseDetector()

# Setup for shirt and pants overlay
shirtFolderPath = "home/Resources/Shirts"  # Update with your correct path
pantsFolderPath = "home/Resources/Pants"   # Update with your correct path
listShirts = os.listdir(shirtFolderPath)
listPants = os.listdir(pantsFolderPath)
shirtRatioHeightWidth = 581 / 440
pantsNumber = 0  # Default pants number

# Function to calculate shirt coordinates
def get_shirt_coordinates(img, bboxInfo):
    bbox = bboxInfo["bbox"]
    center = bboxInfo["center"]

    shirt_width = int(bbox[2] * 0.8)
    shirt_height = int(shirt_width * shirtRatioHeightWidth)

    x1 = max(0, center[0] - shirt_width // 2)
    y1 = max(0, bbox[1] + bbox[3] // 6)

    return x1, y1, shirt_width, shirt_height

# Function to calculate pants coordinates
def get_pants_coordinates(img, bboxInfo, shirt_width):
    bbox = bboxInfo["bbox"]
    center = bboxInfo["center"]

    pants_width = int(shirt_width * 1.5)
    pants_height = int(pants_width * (3 / 2))

    x1 = max(0, center[0] - pants_width // 2)
    y1 = max(0, bbox[1] + int(bbox[3] * 0.5))

    return x1, y1, pants_width, pants_height

# Function to generate video frames
def generate_frames():
    global pantsNumber

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findPose(img, draw=False)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

        if bboxInfo:
            # Process shirt
            x1_shirt, y1_shirt, shirt_width, shirt_height = get_shirt_coordinates(img, bboxInfo)
            try:
                imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[0]), cv2.IMREAD_UNCHANGED)
                if imgShirt is None:
                    raise FileNotFoundError(f"Failed to load shirt image: {listShirts[0]}")
                imgShirt = cv2.resize(imgShirt, (shirt_width, shirt_height))
                img = cvzone.overlayPNG(img, imgShirt, (x1_shirt, y1_shirt))
            except Exception as e:
                print(f"Error processing shirt overlay: {e}")

            # Process pants
            x1_pants, y1_pants, pants_width, pants_height = get_pants_coordinates(img, bboxInfo, shirt_width)
            try:
                imgPants = cv2.imread(os.path.join(pantsFolderPath, listPants[pantsNumber]), cv2.IMREAD_UNCHANGED)
                if imgPants is None:
                    raise FileNotFoundError(f"Failed to load pants image: {listPants[pantsNumber]}")
                imgPants = cv2.resize(imgPants, (pants_width, pants_height))
                img = cvzone.overlayPNG(img, imgPants, (x1_pants, y1_pants))
            except Exception as e:
                print(f"Error processing pants overlay: {e}")

        # Encode the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        # Yield the frame as part of an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Django view to stream the video feed
def video_feed(request):
    return StreamingHttpResponse(generate_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')



# Banner Video Feed
import os
import cv2
import cvzone
import numpy as np
from django.http import StreamingHttpResponse
from cvzone.PoseModule import PoseDetector

# Initialize video capture
cap = cv2.VideoCapture(0)
detector = PoseDetector()

# Setup for banner overlay
bannerPath = "home/Resources/Shirts/7up.png"

# Load the banner image with alpha channel support
imgBanner = cv2.imread(bannerPath, cv2.IMREAD_UNCHANGED)
if imgBanner is None:
    raise FileNotFoundError(f"Failed to load banner image: {bannerPath}")
if imgBanner.shape[2] != 4:  # Check if image has an alpha channel
    b, g, r = cv2.split(imgBanner)
    alpha = np.ones(b.shape, dtype=b.dtype) * 255  # Full opacity
    imgBanner = cv2.merge((b, g, r, alpha))  # Add alpha channel

# Function to generate video frames with banner overlay
def generate_frames_with_banner():
    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findPose(img, draw=False)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

        if bboxInfo:
            # Get face position for banner
            face_x = int(bboxInfo["bbox"][0])
            face_y = int(bboxInfo["bbox"][1])
            banner_width = 200  # Set the desired width for the banner
            banner_height = int(banner_width * imgBanner.shape[0] / imgBanner.shape[1])  # Maintain aspect ratio

            # Resize the banner
            imgBannerResized = cv2.resize(imgBanner, (banner_width, banner_height))

            # Position the banner beside the face
            banner_x = face_x + bboxInfo["bbox"][1]  # Place it to the right of the face
            banner_y = face_y  # Align it with the face vertically

            # Overlay the banner with alpha channel
            img = cvzone.overlayPNG(img, imgBannerResized, (banner_x, banner_y))

        # Encode the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        # Yield the frame as part of an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Django view to stream the video feed with banner overlay
def video_feed_with_banner(request):
    return StreamingHttpResponse(generate_frames_with_banner(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


from django.utils import timezone


def worn_today(request, key):
    try:
        # Get the current timestamp
        timestamp = timezone.now()

        # Reference to the item's node in Firebase
        item_ref = db.reference(f"items_worn/{key}")

        # Retrieve the existing counter from Firebase (initialize to 0 if not found)
        item_data = item_ref.get()

        # Initialize the counter if no data exists
        if item_data and 'counter' in item_data:
            counter = item_data['counter']
        else:
            counter = 0

        # Increment the counter
        counter += 1

        # Prepare the data to store in Firebase (timestamp and updated counter)
        data = {
            'timestamp': str(timestamp),
            'counter': counter,
        }

        # Save the updated data under "items_worn/{key}" (will overwrite counter, keep history separately if needed)
        item_ref.update(data)  # Updates the counter and timestamp

        # Optionally, keep a separate history log (if needed)
        item_ref.child('history').push({
            'timestamp': str(timestamp),
            'counter': counter,
        })

        # Return success response
        JsonResponse({"status": "success", "message": "Item worn today", "data": data})
        return redirect('wardrobe')

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})




def viewModel(request):
    return render(request, 'pages/view_model.html')











# Authentication
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        user_role = request.POST.get('user_role')
        user_email = request.POST.get('user_email')
        password = request.POST.get('password')

        if not user_role or not user_email or not password:
            messages.error(request, "All fields are required.")
            return redirect('/accounts/login/')

        try:
            # Replace dots in the email to match the storage format
            sanitized_email = user_email.replace('.', ',')
            # Retrieve user data from Firebase
            user_ref = db.reference(f'Users/{user_role}/{sanitized_email}')
            user_data = user_ref.get()

            if user_data and user_data.get('password') == password:
                uid = user_data.get('uid')
                role = user_data.get('role')
                email = user_data.get('email') # Get the UID from Firebase

                # Check if the user exists in Django's User model
                user, created = User.objects.get_or_create(username=uid)

                if created:
                    # Set the password and save the user if it was just created
                    user.set_password(password)  # It's better to hash the password
                    user.save()
                
                # Authenticate and log in the user using UID
                user = authenticate(request, username=uid, password=password)

                if user:
                    django_login(request, user)
                    request.session['user_role'] = role
                    request.session['user_email'] = email
                    messages.success(request, "Login successful!")
                    return redirect('/')  # Redirect to the user's dashboard or home page
                else:
                    messages.error(request, "Authentication failed.")
                    return redirect('/accounts/login/')
            else:
                # Invalid credentials
                messages.error(request, "Invalid email or password.")
                return redirect('/accounts/login/')

        except Exception as e:
            messages.error(request, f"Error logging in: {str(e)}")
            return redirect('/accounts/login/')
    else:
        return render(request, 'includes/login.html')


import string
import random

def generate_uid(length=5):
    """Generate a unique alphanumeric UID of specified length."""
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choice(characters) for _ in range(length))

def register(request):
    if request.method == 'POST':
        # Retrieve fields from the request
        user_role = request.POST.get('user_role')
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        password = request.POST.get('password')

        # Validate that all fields are provided
        if not user_role or not user_email or not password:
            messages.error(request, "All fields are required.")
            return redirect('/accounts/register/')

        try:
            # Create a unique alphanumeric UID
            uid = generate_uid()

            # Store user data in Firebase Realtime Database under Users/<user_role>/<UID>
            user_data = {
                "name": user_name,
                "email": user_email,
                "role": user_role,
                "uid": uid,
                # Note: Storing plain passwords is insecure, consider hashing!
                "password": password  
            }

            sanitized_email = user_email.replace('.', ',')
            # Use the Firebase Realtime Database reference
            db.reference(f'Users/{user_role}/{sanitized_email}/').set(user_data)

            # Redirect to login page upon successful registration
            messages.success(request, "Registration successful! Please log in.")
            return redirect('/accounts/login/')

        except Exception as e:
            messages.error(request, f"Error registering user: {str(e)}")
            return redirect('/accounts/register/')
    else:
        return render(request, 'accounts/register.html')


def additional_register(request):
    if request.method == 'POST':
        # Retrieve fields from the request
        user_role = request.POST.get('user_role')
        user_email = request.POST.get('user_email')
        password = request.POST.get('password')

        # Validate that all fields are provided
        if not user_role or not user_email or not password:
            messages.error(request, "All fields are required.")
            return redirect('/accounts/register/')

        try:
            # Create a unique alphanumeric UID
            uid = generate_uid()

            # Store user data in Firebase Realtime Database under Users/<user_role>/<UID>
            user_data = {
                "email": user_email,
                "role": user_role,
                "uid": uid,
                # Note: Storing plain passwords is insecure, consider hashing!
                "password": password  
            }

            sanitized_email = user_email.replace('.', ',')
            # Use the Firebase Realtime Database reference
            db.reference(f'Users/{user_role}/{sanitized_email}/').set(user_data)

            # Redirect to login page upon successful registration
            messages.success(request, "Registration successful! Please log in.")
            return redirect('/')

        except Exception as e:
            messages.error(request, f"Error registering user: {str(e)}")
            return redirect('/accounts/register/')
    else:
        return render(request, 'accounts/register.html')


def add_judge(request):
    return render(request, 'pages/add_judge.html', { 'segment': 'add_judge' })

def add_sponsor(request):
    return render(request, 'pages/add_sponsor.html', { 'segment': 'add_sponsor' })

def add_leader(request):
    return render(request, 'pages/add_leader.html', { 'segment': 'add_leader' })

from datetime import datetime

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')  # Radio button selection
        location = request.POST.get('location')
        description = request.POST.get('description')
        event_time_str = request.POST.get('event_time')  # Event time as a string

        # Convert the event_time string to a datetime object
        event_time = datetime.fromisoformat(event_time_str)

        # Files for rules and poster
        rules_file = request.FILES.get('rules')
        poster_file = request.FILES.get('poster')

        # Initialize event data with placeholders for URLs
        event_data = {
            'category': category,
            'location': location,
            'description': description,
            'rules': None,    # Placeholder for rules URL
            'poster': None,   # Placeholder for poster URL
            'event_time': event_time.isoformat(),
            'registered': {},
        }

        # Upload rules file to Firebase Storage if it exists
        if rules_file:
            bucket = storage.bucket()
            rules_blob = bucket.blob(f'rules/{name}/{rules_file.name}')
            rules_blob.upload_from_file(rules_file, content_type=rules_file.content_type)
            rules_blob.make_public()  # Make the image publicly accessible
            event_data['rules'] = rules_blob.public_url

        # Upload poster image to Firebase Storage if it exists
        if poster_file:
            bucket = storage.bucket()
            poster_blob = bucket.blob(f'posters/{name}/{poster_file.name}')
            poster_blob.upload_from_file(poster_file, content_type=poster_file.content_type)
            poster_blob.make_public()
            event_data['poster'] = poster_blob.public_url

        # Store the event data in Firebase Realtime Database
        db.reference(f'Events/{name}').set(event_data)

        # Prepare JSON response
        response_data = {
            'event_name': name,
            'category': event_data['category'],
            'location': event_data['location'],
            'description': event_data['description'],
            'rules': event_data['rules'],
            'poster': event_data['poster'],
            'event_time': event_data['event_time'],
        }

        return redirect('/accounts/create-event/')  # Redirect after successful creation

    return render(request, 'pages/create_event.html', {'segment':'create_event'})


def get_events(request):
    # Reference to the 'Events' path in Firebase Realtime Database
    events_ref = db.reference('Events')
    
    # Retrieve all events data
    events_data = events_ref.get()  # Returns a dictionary with event names as keys
    
    # Convert data into lists for outdoor and indoor events
    outdoor_events = []
    indoor_events = []

    if events_data:
        for event_name, event_info in events_data.items():
            event_info['name'] = event_name  # Add the event name to each event's data
            
            # Check the category and add to the respective list
            if event_info.get('category') == 'Outdoor':
                outdoor_events.append(event_info)
            elif event_info.get('category') == 'Indoor':
                indoor_events.append(event_info)
    
    # Pass events lists as context
    context = {
        'outdoor_events': outdoor_events,
        'indoor_events': indoor_events,
        'segment': 'view_events',
    }
    
    return render(request, 'pages/index.html', context)

from django.core.files.storage import FileSystemStorage
import csv


from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import csv
from django.conf import settings

@csrf_exempt
def register_team(request):
    # Handle form submission
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        event_name = request.POST.get('event_name')
        csv_file = request.FILES.get('csv_input')
        members = []

        if csv_file:
            # Process CSV file
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            file_path = fs.url(filename)

            with open(file_path[1:], newline='') as csvfile:  # Remove the leading slash from the URL
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 3:  # Ensure there are enough columns
                        members.append({
                            'name': row[0],
                            'contact': row[1],
                            'email': row[2],
                        })
        else:
            # Handle individual member details from the form
            member_count = int(request.POST.get('member_count', 0))
            for i in range(1, member_count + 1):
                member_name = request.POST.get(f'member{i}_name')
                member_contact = request.POST.get(f'member{i}_contact')
                member_email = request.POST.get(f'member{i}_email')

                if member_name and member_contact and member_email:
                    members.append({
                        'name': member_name,
                        'contact': member_contact,
                        'email': member_email,
                    })

        # Prepare the data to be saved in Firebase
        team_data = {
            'team_name': team_name,
            'members': members,
        }

        # Reference to the Firebase path for storing the team event
        ref_path = f'Events/{event_name}/registered/{team_name}'
        db.reference(ref_path).set(team_data)  # Store the team data in Firebase

        # Send confirmation email to each team member
        for member in members:
            member_email = member['email']
            subject = 'Team Registration Confirmation'
            message = f"Dear {member['name']},\n\n" \
                      f"Congratulations! Your team '{team_name}' has been successfully registered for the event '{event_name}'.\n" \
                      "We look forward to your participation.\n\nBest Regards,\nEvent Team"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [member_email], fail_silently=False)

        # Redirect after submission
        return redirect('/accounts/register-team')

    # If not a POST request, render the form
    events_ref = db.reference('Events')
    events_data = events_ref.get()  # Returns a dictionary with event names as keys

    # Convert data into a list of dictionaries for easier handling in templates
    events_list = []
    if events_data:
        for event_name, event_info in events_data.items():
            event_info['name'] = event_name  # Add the event name to each event's data
            events_list.append(event_info)

    # Pass events list as context
    context = {
        'events': events_list,
        'segment': 'register_teams',
    }

    return render(request, 'pages/register_team.html', context)



from collections import defaultdict
from django.urls import reverse

from django.db import transaction

@csrf_exempt
def generate_fixtures(request):
    # Fetch sports from the Firebase database
    sports = db.reference('Events/').get()
    available_sports = list(sports.keys()) if sports else []

    if request.method == "POST":
        selected_sport = request.POST.get("selected_sport")

        if not selected_sport:
            return render(request, 'pages/fixtures.html', {'error': "Please select a sport."})

        details = sports.get(selected_sport, {})
        registered_teams = details.get('registered', {})

        if len(registered_teams) <= 1:
            return render(request, 'pages/fixtures.html', {'error': "At least 1 team is required."})

        # Start a transaction to ensure fixture creation is atomic
        with transaction.atomic():
            # Delete existing fixtures for the selected sport
            Fixture.objects.filter(sport=selected_sport).delete()

            # Generate fixtures as a round-robin
            teams = list(registered_teams.keys())
            fixtures = []
            if len(teams) % 2 == 1:
                teams.append("Bye")

            for round_num in range(len(teams) - 1):
                round_fixtures = []
                for i in range(len(teams) // 2):
                    home = teams[i]
                    away = teams[len(teams) - 1 - i]
                    if home != "Bye" and away != "Bye":
                        fixture = Fixture.objects.create(
                            home_team=home,
                            away_team=away,
                            sport=selected_sport,
                            round_number=round_num + 1
                        )
                        round_fixtures.append(fixture)
                teams = [teams[0]] + [teams[-1]] + teams[1:-1]
                fixtures.extend(round_fixtures)

        # Redirect to the judge_fixtures page
        return redirect(reverse('judge_fixtures', args=[selected_sport]))

    # Render the form for GET request
    return render(request, 'pages/fixtures.html', {
        'available_sports': available_sports,
        'segment': 'generate_fixtures'
    })

from collections import defaultdict

from django.shortcuts import render, redirect
from .models import Fixture
from collections import defaultdict
from django.urls import reverse


from collections import defaultdict

import firebase_admin
from firebase_admin import db
from collections import defaultdict
from django.shortcuts import redirect, render

# Ensure Firebase is initialized (should be done at the start of your app)
if not firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate("path/to/your/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://your-database-name.firebaseio.com'  # Update with your Firebase DB URL
    })

def judge_fixtures(request, sport):
    if request.method == "POST":
        fixtures = Fixture.objects.filter(sport=sport)
        for fixture in fixtures:
            fixture.points_home = int(request.POST.get(f"home_points_{fixture.id}", fixture.points_home))
            fixture.points_away = int(request.POST.get(f"away_points_{fixture.id}", fixture.points_away))
            fixture.man_of_the_match = request.POST.get(f"man_of_the_match_{fixture.id}", fixture.man_of_the_match)
            fixture.save()

        # After saving fixtures, update the leaderboard and MVP in Firebase
        update_leaderboard_in_firebase(fixtures)
        
        return redirect('judge_fixtures', sport=sport)

    # Retrieve fixtures for the specified sport
    fixtures = Fixture.objects.filter(sport=sport)

    # Calculate leaderboard
    leaderboard = defaultdict(int)
    for fixture in fixtures:
        leaderboard[fixture.home_team] += fixture.points_home
        leaderboard[fixture.away_team] += fixture.points_away

    # Determine "Man of the Tournament"
    man_of_the_match_counts = defaultdict(int)
    for fixture in fixtures:
        if fixture.man_of_the_match:
            man_of_the_match_counts[fixture.man_of_the_match] += 1

    # Find the max count and identify all players with that count
    max_count = max(man_of_the_match_counts.values(), default=0)
    man_of_the_tournament = [player for player, count in man_of_the_match_counts.items() if count == max_count]

    context = {
        'fixtures': fixtures,
        'leaderboard': sorted(leaderboard.items(), key=lambda x: -x[1]),
        'man_of_the_tournament': man_of_the_tournament,
        'sport': sport,
        'default_points_home': 0,  # Default value for home points
        'default_points_away': 0,
        'default_man_of_the_match': '',
        'segment': 'judge_fixtures'
    }

    return render(request, 'pages/judge_fixtures.html', context)

def update_leaderboard_in_firebase(fixtures):
    # Reference to the 'Leaderboard' node in Firebase
    leaderboard_ref = db.reference('Leaderboard/teams')
    mvp_ref = db.reference('Leaderboard/MVP')

    # Initialize a dictionary to hold teams and their total points
    total_points = defaultdict(int)

    # Calculate total points for each team based on fixtures
    for fixture in fixtures:
        total_points[fixture.home_team] += fixture.points_home
        total_points[fixture.away_team] += fixture.points_away

    # Create a list of (team, points) and sort it by points in descending order
    sorted_teams = sorted(total_points.items(), key=lambda x: -x[1])

    # Assign points based on rankings
    team_points = {}
    if len(sorted_teams) > 0:
        team_points[sorted_teams[0][0]] = 7  # 1st place
    if len(sorted_teams) > 1:
        team_points[sorted_teams[1][0]] = 5  # 2nd place
    if len(sorted_teams) > 2:
        team_points[sorted_teams[2][0]] = 3  # 3rd place
    for team, _ in sorted_teams[3:]:
        team_points[team] = 1  # All other teams get 1 point

    # Update leaderboard in Firebase
    for team, points in team_points.items():
        # Check if the team exists in the leaderboard
        team_ref = leaderboard_ref.child(team)
        existing_points = team_ref.get() or 0
        team_ref.set(existing_points + points)  # Update with new points

    # Update MVP
    man_of_the_match_counts = defaultdict(int)
    for fixture in fixtures:
        if fixture.man_of_the_match:
            man_of_the_match_counts[fixture.man_of_the_match] += 1

    for mvp, count in man_of_the_match_counts.items():
        mvp_ref_child = mvp_ref.child(mvp)
        existing_count = mvp_ref_child.get() or 0
        mvp_ref_child.set(existing_count + count)  # Update with new count


def view_leaderboard(request):
    try:
        # References to 'Leaderboard' and 'MVP' in Firebase Realtime Database
        leaderboard_ref = db.reference('Leaderboard/teams')
        mvp_ref = db.reference('Leaderboard/MVP')

        # Retrieve leaderboard and MVP data
        leaderboard_data = leaderboard_ref.get() or {}
        mvp_data = mvp_ref.get() or {}

        # Sort leaderboard data by points in descending order
        sorted_leaderboard = sorted(leaderboard_data.items(), key=lambda x: -x[1])

        # Find MVP with the highest count
        mvp_name, mvp_count = None, 0
        if mvp_data:
            mvp_name, mvp_count = max(mvp_data.items(), key=lambda item: item[1], default=(None, 0))

        # Context for the template
        context = {
            'segment': 'leaderboard',
            'leaderboard': sorted_leaderboard,
            'mvp': {'name': mvp_name, 'count': mvp_count} if mvp_name else None
        }
        
        return render(request, 'pages/leaderboard.html', context)

    except Exception as e:
        # If an error occurs, include it in the context
        context = {
            'segment': 'leaderboard',
            'error': str(e),
        }
        return render(request, 'pages/leaderboard.html', context)


def view_fixtures(request):
    events_ref = db.reference('Events')
    
    # Retrieve all events data
    events_data = events_ref.get()  # Returns a dictionary with event names as keys
    
    # Convert data into a list of dictionaries for easier handling in templates
    events_list = []
    if events_data:
        for event_name, event_info in events_data.items():
            event_info['name'] = event_name  # Add the event name to each event's data
            events_list.append(event_info)
    

    print(events_list)
    # Pass events list as context
    context = {
        'events': events_list,
        'segment':'view_fixtures',
    }
    
    return render(request, 'pages/view_fixtures.html', context)


def item_view(request):    
    if request.method == 'POST':
        name = request.POST.get('name')
        cost = request.POST.get('cost')
        category = request.POST.get('category')  # Get the category from the form
        image = request.FILES.get('image')


        # Upload the image to Firebase Storage
        bucket = storage.bucket()
        image_blob = bucket.blob(f'images/items/{category}/{name}/{image.name}')

        # Reset the stream position to the beginning
        image.seek(0)

        # Upload the image from the file stream
        image_blob.upload_from_file(image, content_type=image.content_type)
        image_blob.make_public()  # Make the image publicly accessible

        # Prepare item data for Firebase
        item_data = {
            'name': name,
            'cost': cost,
            'image': image_blob.public_url,
            'category': category,
        }

        # Store the item data in Firebase Realtime Database
        db.reference(f'Items/{category}/{name}').set(item_data)

        return redirect('passItOver')  # Redirect to the same page to avoid resubmission



    try:
        # Fetch items from each category path in Firebase
        basic_items = db.reference('Items/basic').get() or {}
        advance_items = db.reference('Items/advance').get() or {}
        premium_items = db.reference('Items/premium').get() or {}

        # Combine all items from each category into a single list
        all_items = []
        
        # Adding each category's items to the combined list with detailed fields
        for category_items in [basic_items, advance_items, premium_items]:
            for item_id, item_data in category_items.items():
                all_items.append({
                    'name': item_data.get('name'),
                    'category': item_data.get('category'),
                    'cost': item_data.get('cost'),
                    'image': item_data.get('image'),
                })

        # Pass combined items as context
        context = {
            'items': all_items,
            'segment': 'passItOver'
        }

        return render(request, 'pages/passItOver.html', context)
    
    except Exception as e:
        # Handle any potential errors gracefully
        print(f"Error fetching items from Firebase: {e}")
        return render(request, 'pages/passItOver.html', {'items': []})



from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from django.http import HttpResponse

def generate_certificate_pdf(recipient_name, course_name, completion_date, instructor_name, organization_name,uid):
    # Create a byte stream to hold the PDF data
    buffer = io.BytesIO()
    
    # Create a canvas for the PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the PDF content
    p.drawString(100, 700, f"Certificate of Completion")
    p.drawString(100, 650, f"This certifies that")
    p.drawString(100, 600, f"{recipient_name}")
    p.drawString(100, 300, f"Uid: {uid}")
    p.drawString(100, 550, f"has completed the course")
    p.drawString(100, 500, f"{course_name}")
    p.drawString(100, 450, f"Date of Completion: {completion_date}")
    p.drawString(100, 400, f"Instructor: {instructor_name}")
    p.drawString(100, 350, f"Organization: {organization_name}")

    # Finalize the PDF
    p.showPage()
    p.save()
    
    # Move the buffer position to the beginning
    buffer.seek(0)
    
    return buffer

def certificate_view(request):
    # Retrieve users from Firebase
    users = db.reference('Users/contestant').get()
    events = db.reference('Events').get()

    # Initialize a list to store recipient names and PDFs
    certificates = []
    
    # Get a list of event names dynamically
    event_names = list(events.keys()) if events else []  # Convert to list or set to handle empty case

    # Check if users is not None and is a dictionary
    if users and isinstance(users, dict):
        for email, user_data in users.items():
            # Get user details
            recipient_name = user_data.get('name', 'Default Recipient')
            completion_date = timezone.now().strftime('%B %d, %Y')
            instructor_name = 'Jane Smith'
            organization_name = 'Your Company'
            uid = user_data.get('uid')
            print(uid)
            # Generate PDF for each user with the event names
            pdf_buffer = generate_certificate_pdf(uid, event_names, completion_date, instructor_name, organization_name,uid)

            # Add to the list (You can modify this to save or do something else with the PDF)
            certificates.append((recipient_name, pdf_buffer, uid ))

    # Render the certificates or provide download links
    context = {
        'certificates': certificates,  # Pass the list of certificates to the template
        'event_names': event_names  # Pass the list of event names to the template
    }
    
    return render(request, 'pages/certificate_template.html', context)


def download_certificate(request, recipient_name):
    # Retrieve the correct PDF for the recipient
    # This will require some logic to get the correct PDF buffer or store them in a temporary location
    # For simplicity, we will just re-generate the PDF in this example
    course_name = 'Advanced Django'
    completion_date = timezone.now().strftime('%B %d, %Y')
    instructor_name = 'Jane Smith'
    organization_name = 'Your Company'

    # Generate PDF
    pdf_buffer = generate_certificate_pdf(recipient_name, course_name, completion_date, instructor_name, organization_name)

    # Set the response
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{recipient_name}_certificate.pdf"'
    
    return response


def basic_item_view(request):
    return render(request, 'pages/basicItem.html')


def advance_item_view(request):
    return render(request, 'pages/advanceItem.html')


def premium_item_view(request):
    return render(request, 'pages/premiumItem.html')


def get_all_image_urls():
    try:
        # Reference to the 'items' node in Firebase Realtime Database
        ref = db.reference('Items')
        categories = ref.get()

        # List to store all image URLs
        image_urls = []

        # Loop through each category and gather image URLs
        for category in ['basic', 'advance', 'premium']:
            if category in categories:
                for item_key, item_data in categories[category].items():
                    if 'image' in item_data:
                        image_urls.append(item_data['image'])

        # Print all image URLs to console
        print("Image URLs:", image_urls)
        return image_urls
    except Exception as e:
        print(f"Error fetching image URLs: {e}")
        return []


@csrf_exempt
def track_image_click(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_id = data.get('image_id')

            if image_id:
                # Firebase reference to the image's click count
                click_ref = db.reference(f'Items/{image_id}/click_count')

                # Increment the click count atomically
                def increment_click_count(current_value):
                    return (current_value or 0) + 1

                click_ref.transaction(increment_click_count)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'image_id not provided'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)









def admin_register(request):
    if request.method == 'POST':
        # Retrieve fields from the request
        user_role = 'admin'
        user_email = request.POST.get('user_email')
        password = request.POST.get('password')

        # Validate that all fields are provided
        if not user_role or not user_email or not password:
            messages.error(request, "All fields are required.")
            return redirect('/accounts/register/')

        try:
            # Create a unique alphanumeric UID
            uid = generate_uid()

            # Store user data in Firebase Realtime Database under Users/<user_role>/<UID>
            user_data = {
                "email": user_email,
                "role": user_role,
                "uid": uid,
                # Note: Storing plain passwords is insecure, consider hashing!
                "password": password  
            }

            sanitized_email = user_email.replace('.', ',')
            # Use the Firebase Realtime Database reference
            db.reference(f'Users/{user_role}/{sanitized_email}/').set(user_data)

            # Redirect to login page upon successful registration
            messages.success(request, "Registration successful! Please log in.")
            return redirect('/accounts/admin-login/')

        except Exception as e:
            messages.error(request, f"Error registering user: {str(e)}")
            return redirect('/accounts/admin-register/')
    else:
        return render(request, 'auth/admin_register.html')


def admin_login(request):
    if request.method == 'POST':
        user_role = 'admin'
        user_email = request.POST.get('user_email')
        password = request.POST.get('password')

        if not user_role or not user_email or not password:
            messages.error(request, "All fields are required.")
            return redirect('/accounts/login/')

        try:
            # Replace dots in the email to match the storage format
            sanitized_email = user_email.replace('.', ',')
            # Retrieve user data from Firebase
            user_ref = db.reference(f'Users/{user_role}/{sanitized_email}')
            user_data = user_ref.get()

            if user_data and user_data.get('password') == password:
                uid = user_data.get('uid')
                role = user_data.get('role')
                email = user_data.get('email') # Get the UID from Firebase

                # Check if the user exists in Django's User model
                user, created = User.objects.get_or_create(username=uid)

                if created:
                    # Set the password and save the user if it was just created
                    user.set_password(password)  # It's better to hash the password
                    user.save()
                
                # Authenticate and log in the user using UID
                user = authenticate(request, username=uid, password=password)

                if user:
                    django_login(request, user)
                    request.session['user_role'] = role
                    request.session['user_email'] = email
                    messages.success(request, "Login successful!")
                    return redirect('/')  # Redirect to the user's dashboard or home page
                else:
                    messages.error(request, "Authentication failed.")
                    return redirect('/accounts/login/')
            else:
                # Invalid credentials
                messages.error(request, "Invalid email or password.")
                return redirect('/accounts/login/')

        except Exception as e:
            messages.error(request, f"Error logging in: {str(e)}")
            return redirect('/accounts/login/')
    else:
        return render(request, 'auth/admin_login.html')

