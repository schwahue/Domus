from flask import Blueprint, render_template, request, flash, url_for, redirect, session, jsonify
from sqlalchemy import true
from app.models.product import Product
from app.models.listing import Listing
from app import listing_schema, listings_schema
import boto3, logging
from werkzeug.utils import secure_filename

import os
from app import db, dropzone, app

router = Blueprint('router', __name__, template_folder='templates')

# This will help to render the navigation bar items [(href, id, caption)]
# Set active_page = id
pages = [('router.index', 'index', 'Index')]
admin_pages = [('router.admin_ticket', 'ticketing', 'Ticketing')]



# Put aws resource here for now
s3 = boto3.resource('s3')


@router.route('/')
def index():
    return render_template("index.html", navigation_bar = pages, active_page='index'), 200

@router.route('/admin')
def admin_index():
    return render_template("admin-index.html", navigation_bar = admin_pages), 200

ticketList = [('abc01', 'this is a ticket blah blah', 'resolved')]

@router.route('/admin/ticketing')
def admin_ticket():
    return render_template("admin-ticketing.html",  navigation_bar = admin_pages,
                                                    active_page='ticketing',
                                                    ticketList = ticketList ), 200


# W

@router.route('/user/login', methods=('GET', 'POST'))
def simple_login():
    if request.method == "GET":
        # flash("Hello there!", "primary")
        # flash("Howdy!", "success")
        # flash("Howdy2!", "warning")
        # flash("Howdy3!", "danger")
        print("GET login page")
    elif request.method == "POST":
        email = request.form["form_email"]
        password = request.form["form_password"]
        if email != "user@email.com" or password != "1234":
            print(f"Email input is {email} \nPassword Input is {password}")  
            flash('Invalid credentials provided', 'danger')
        if password == "secret":
            print("Session obj:")
            print(session)
        else:
            session["param1"] = email
            return redirect(url_for('router.success_page'))     
    return render_template("property/login.html")

# Login success page
@router.route('/user/success')
def success_page():
    special_value = session.get("param1")
    return render_template("property/success.html", special_value=special_value)


# Seller console
@router.route('/user/sellerconsole', methods=['GET'])
def view_seller_console():
    return render_template("property/sellerconsole.html")






# Create Listing
@router.route('/user/createlisting', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':

        # Retrieve form data
        listing_name = request.form["form_listing_name"]
        listing_description = request.form["form_listing_description"]
        listing_price = request.form["form_listing_price"]
        listing_price_type = request.form["form_listing_price_type"]
        listing_type = request.form["form_listing_type"]
        listing_property_type = request.form["form_property_type"]

        # Get single file
        #photo = request.files["form_photo"]

        # Get multiple files
        photo_list = request.files.getlist("form_photo")
        virtual_tour_url = request.form["form_virtual_tour_url"]

        # 
        district = request.form["form_district"]
        address = request.form["form_address"]
        bedroom = request.form["form_bedroom"]
        listed_by = "Wilfred Huang"

        bucket_name = 'ecp-bucket1227'
        bucket_key = 'something1337a'

        url = ""

        upload_image_check = False  
        # Photo
        if photo_list:
            for photo in photo_list:
                print(photo.filename)

                if (photo.content_type != "image/jpeg"):

                    upload_image_check = False
                else:
                    upload_image_check = True

        if (upload_image_check == True):
            if photo_list: 
                for photo in photo_list:
                    mimetype = photo.content_type
                    filename = secure_filename(photo.filename)
                    url += f'https://{bucket_name}.s3.amazonaws.com/{filename};'
                    s3.meta.client.upload_file(filename, bucket_name, filename, ExtraArgs={"ContentType": mimetype})
            flash(f"Successful upload to S3", "success")
        else:
            flash('Only image files in .jpg format are allowed', 'danger')
            return redirect(url_for('router.create_listing'))



        # Remove ; from last url
        url = url[:-1]

        new_listing = Listing(listing_name, listing_description, listing_price, listing_price_type, listing_type, listing_property_type, url, virtual_tour_url, district, address, bedroom, listed_by)
        db.session.add(new_listing)
        db.session.commit()

    return render_template("property/create_listing.html")


#  View all listing
@router.route('/user/viewlisting/', methods=['GET'])
def view_all_listing():
    all_listings = Listing.query.all()
    result = listings_schema.dump(all_listings)
    # for i in result:
    #     print("=== Housing ===")
    #     print(i["property_type"])
    #     print(i["price"])
    #     print(i["name"])
    #     print(i["id"])
    return render_template("property/seller_listings.html", result=result)


#  View specific listing
@router.route('/user/viewlisting/<id>', methods=['GET', 'POST'])
def view_listing(id):
    # Get back listing object
    print(id)
    listing = Listing.query.get(id)
    print(listing)
    print(listing.name)
    return render_template("property/view_listing.html", listing=listing)


# Delete listing
@router.route('/user/deletelisting/<id>', methods=['GET', 'POST','DELETE'])
def delete_listing(id):
    if request.method == 'POST':
        print("bar")
        listing = Listing.query.get(id)
        name = listing.name
        db.session.delete(listing)
        db.session.commit()
        flash(f"Deleted Listing: {name} ", "danger")
    return redirect(url_for('router.view_all_listing'))

# Update a listing [Incomplete]
@router.route('/user/updatelisting/<id>', methods=['GET', 'POST','PUT'])
def update_listing(id):
    listing = Listing.query.get(id)
    if request.method == 'GET':
        print("")
    if request.method == 'POST':
        listing_name = request.form["form_listing_name"]
        listing_description = request.form["form_listing_description"]
        listing_price = request.form["form_listing_price"]
        listing_price_type = request.form["form_listing_price_type"]
        listing_type = request.form["form_listing_type"]
        listing_property_type = request.form["form_property_type"]

        photo_list = request.files.getlist("form_photo")
        virtual_tour_url = request.form["form_virtual_tour_url"]

        
        district = request.form["form_district"]
        address = request.form["form_address"]
        bedroom = request.form["form_bedroom"]
        listed_by = "Wilfred Huang"



        
        bucket_name = 'ecp-bucket1227'
        bucket_key = 'something1337a'

        url = ""

        upload_image_check = False  
        # Photo
        if photo_list:
            for photo in photo_list:
                print(photo.filename)
                if (photo.content_type != "image/jpeg"):
                    upload_image_check = False
                else:
                    upload_image_check = True

        if (upload_image_check == True):
            if photo_list: 
                for photo in photo_list:
                    mimetype = photo.content_type
                    filename = secure_filename(photo.filename)
                    url += f'https://{bucket_name}.s3.amazonaws.com/{filename};'
                    s3.meta.client.upload_file(filename, bucket_name, filename, ExtraArgs={"ContentType": mimetype})
            flash(f"Successful upload to S3", "success")
        else:
            flash('Only image files in .jpg format are allowed', 'danger')
            return redirect(url_for('router.create_listing'))


        # Remove ; from last url
        url = url[:-1]

        # Update Info here
        listing.name = listing_name 
        listing.description = listing_description
        listing.price = listing_price
        listing.price_type = listing_price_type
        listing.listing_type = listing_type
        listing.property_type = listing_property_type
        listing.s3_object_link = url
        listing.virtual_tour_url = virtual_tour_url
        listing.district = district
        listing.address = address
        listing.bedroom = bedroom
        listing.listed_by = listed_by

        db.session.commit()

        flash(f"Updated listing", "success")
        return redirect(url_for('router.view_all_listing'))



        

    return render_template("property/update_listing.html", listing=listing)



# TODO: test RDS = successful
@router.route('/user/RDS', methods=['GET'])
def test_rds():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)



# TODO: test S3 bucket upload, can only upload one thing at a time
@router.route('/user/uploads3', methods=['GET', 'POST'])
def s3_upload():
    if request.method == 'GET':
        # Print out bucket names
        for bucket in s3.buckets.all():
            print(f"Bucket Name: {bucket.name}")
    if request.method == 'POST':
        photo = request.files["form_photo"]
        print(photo)
        if photo:
            filename = secure_filename(photo.filename)
            photo.save(filename)
            #s3.meta.client.upload_file(f'{filename}', f'{bucket_name}', f'{filename}')
            flash(f"Successful upload {filename}", "info")
        return render_template("property/uploads3.html")

    return render_template("property/uploads3.html")



# Test Dropzone js
@router.route('/user/dropzone', methods=['GET', 'POST'])
def view_dropzone():
    # Single file method
    # if request.method == 'POST':
    #     f = request.files.get('file')
    #     f.save(os.path.join('', f.filename))
    #     print("Dropzone tested")

    # Multi file method
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join('', f.filename))

    return render_template("property/dropzone.html")


# Test Splide
@router.route('/user/splide', methods=['GET'])
def view_splide():
    return render_template("property/splide.html")