from app import app
from flask import render_template, redirect, url_for, request
import os
from app.models.product import Product

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/extract', methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        product = Product(product_id)
        product.extract_product()

        if product.product_name == None:
            error = True
            return render_template("extract.html.jinja", error=error)
        else:
            product.process_stats()
            product.draw_charts()
            product.save_opinions()
            product.save_stats()
            return redirect(url_for("product", product_id=product_id))
    else:
        return render_template("extract.html.jinja")

@app.route('/products')
def products():
    products = [filename.split(".")[0] for filename in os.listdir("app/opinions")]
    for i in range(0, len(products)):
        products[i] = Product(products[i])
        products[i].read_from_json()
    return render_template("products.html.jinja", products=products)

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id): 
    product = Product(product_id)
    product.read_from_json()
    opinions = product.opinions_to_df()
    stats = product.stats_to_dict()
    return render_template("product.html.jinja", stats=stats, product_id=product_id, opinions_tables=[opinions.to_html(classes='data')], opinions_titles=opinions.columns.values)