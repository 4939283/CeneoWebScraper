from app import app
from flask import render_template, redirect, url_for, request, send_file
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
        product.extract_name()
        if product.product_name == None:
            error = True
            return render_template("extract.html.jinja", error=error)
        else:
            product.extract_opinions()
            product.calculate_stats()
            product.draw_charts()
            product.export_opinions()
            product.export_product()
            return redirect(url_for("product", product_id=product_id))
    else:
        return render_template("extract.html.jinja")

@app.route('/products')
def products():
    products = [filename.split(".")[0] for filename in os.listdir("app/opinions")]
    for i in range(0, len(products)):
        products[i] = Product(products[i])
        products[i].import_product()
    return render_template("products.html.jinja", products=products)

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id):
    product = Product(product_id)
    product.import_product()
    opinions = product.opinions_to_dict()
    stats = product.stats_to_dict()
    return render_template("product.html.jinja", stats=stats, product_id=product_id, opinions=opinions)
    
@app.route('/charts/<product_id>')
def charts(product_id):
    return render_template("charts.html.jinja", product_id=product_id)

@app.route('/download_json/<product_id>')
def download_json(product_id):
    return send_file(f"opinions\{product_id}.json",
                     mimetype='text/json',
                     attachment_filename=f'{product_id}.json',
                     as_attachment=True)
