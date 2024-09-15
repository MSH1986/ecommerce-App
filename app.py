from flask import Flask, flash, redirect, render_template, request, url_for
from database.connect import creat_connection
import os
from  utils.clients_utils import clients_display
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
app.secret_key = 'your-secure-secret-key'  # Required for session handling

connection = creat_connection()

# Define the upload folder path
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the maximum file size to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Define allowed extensions for uploaded files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard/index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('dashboard/about.html')


# ------------- Start section Clients ------------

@app.route('/clients', methods=['GET'])
def clients_display():
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users_table"
    cursor.execute(query)
    records = cursor.fetchall()
    return render_template('dashboard/clients/clients.html', clients=records)

@app.route('/profileClient/<int:client_id>', methods= ['GET'])
def show_client(client_id):
     # Fetch the Clients 
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users_table WHERE id=%s"
    cursor.execute(query, (client_id,))
    user = cursor.fetchone()
   
    # Render the form with existing product data and sorted categories
    return render_template('dashboard/clients/show_client.html', client=user)


@app.route('/delete_client/<int:client_id>')
def delete_client(client_id):
    # Logic to delete a category
    try:
        cursor = connection.cursor()
        query = '''DELETE FROM users_table WHERE id=%s'''
        cursor.execute(query, (client_id,))
        connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()

    return redirect(url_for('clients_display'))

# ------------- End section Clients ------------
# --------------------------------------------------------------
# ------------- Start section Products (Add Product, Add Category, Delete Category)------------
@app.route('/addNewProduct', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        price = request.form['price']
        
        # Check if a file is part of the POST request
        if 'photo' not in request.files:
            flash('No photo part in the request', 'error')
            return redirect(request.url)
        
        file = request.files['photo']
        
        # If the user does not select a file
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        # Save the file if it has a valid extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Store only the filename in the database, not the full path
            photo_filename = filename
           
            # Insert the data into the database
            try:
                cursor = connection.cursor()
                query = '''INSERT INTO products_table (name, category, description, price, photo) 
                           VALUES (%s, %s, %s, %s, %s)'''
                cursor.execute(query, (name, category, description, price, photo_filename))
                connection.commit()
                flash('Product added successfully', 'success')

            except Exception as e:
                print(f"An Error occurred: {e}")
                flash('An error occurred while adding the product.', 'error')
            finally:
                cursor.close()

            # Redirect to the product display page
            return redirect(url_for('products_display'))

        else:
            flash('Invalid file type. Allowed types are png, jpg, jpeg, gif', 'error')
            return redirect(request.url)
    
    # If it's a GET request, fetch categories
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM categories_table"
    cursor.execute(query)
    records = cursor.fetchall()
    
    # Sort categories alphabetically by `name_category`
    sorted_categories = sorted(records, key=lambda x: x['name_category'])
    
    # Render the product add form
    return render_template('dashboard/add_product.html', categories=sorted_categories)

@app.route('/addNewCategory', methods=['POST'])
def add_category():
    category = request.form['category']
    try:
        cursor = connection.cursor()
        query = '''INSERT INTO categories_table (name_category) VALUES (%s)'''
        cursor.execute(query, (category,))
        connection.commit()

    except Exception as e:
        print(f"An Error occurred: {e}")
    finally:
        cursor.close()

    # Redirect to the product display page
    return redirect(url_for('add_product'))

@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    # Logic to delete a category
    try:
        cursor = connection.cursor()
        query = '''DELETE FROM categories_table WHERE id=%s'''
        cursor.execute(query, (category_id,))
        connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()

    return redirect(url_for('add_product'))
# -------------Ent section Products -----------------------------------------------------------


@app.route('/products', methods=['GET'])
def products_display():
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM products_table"
    cursor.execute(query)
    records = cursor.fetchall()
    return render_template('dashboard/products.html', products=records)


@app.route('/editProduct/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    cursor = connection.cursor(dictionary=True)

    # Fetch the product data for pre-filling the form
    query = "SELECT * FROM products_table WHERE id = %s"
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        price = request.form['price']

        # Handle photo upload
        photo = request.files['photo']
        
        # If a new photo is uploaded, use the new one
        if photo and photo.filename != '':
            filename = secure_filename(photo.filename)  # Make the filename safe
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)  # Save the photo in the 'uploads' folder
            photo_filename = filename  # Use the new filename in the database
        else:
            # No new photo uploaded, so keep the existing one
            photo_filename = product['photo']

        # Update the product details, including the photo filename
        update_query = '''UPDATE products_table 
                          SET name = %s, category = %s, description = %s, price = %s, photo = %s 
                          WHERE id = %s'''
        cursor.execute(update_query, (name, category, description, price, photo_filename, product_id))
        connection.commit()
        
        return redirect(url_for('products_display'))

    # Fetch the categories for the dropdown
    query2 = "SELECT * FROM categories_table"
    cursor.execute(query2)
    categories = cursor.fetchall()
    sorted_categories = sorted(categories, key=lambda x: x['name_category'])
    
    # Render the form with existing product data and sorted categories
    return render_template('dashboard/edit_product.html', categories=sorted_categories, product=product)



if __name__ == '__main__':
    app.run(debug=True)