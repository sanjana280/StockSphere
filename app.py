from flask import Flask, render_template, request, redirect, url_for
from database import db
from models.product import Product
from models.category import Category
from models.supplier import Supplier
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stocksphere.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
# -----------------------------
# Temporary Admin Credentials
# -----------------------------

USERNAME = "admin"
PASSWORD = "admin123"


# -----------------------------
# Login Page
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            return redirect(url_for("dashboard"))

        else:
            return render_template(
                "login.html",
                error="Invalid Username or Password!"
            )

    return render_template("login.html")


# -----------------------------
# Dashboard
# -----------------------------

@app.route("/dashboard")
def dashboard():

    total_products = Product.query.count()

    total_categories = db.session.query(Product.category).distinct().count()

    low_stock = Product.query.filter(Product.quantity < 10).count()

    recent_products = (
        Product.query
        .order_by(Product.id.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_categories=total_categories,
        low_stock=low_stock,
        recent_products=recent_products
    )


# -----------------------------
# Products Page
# -----------------------------
@app.route("/products")
def products():

    search = request.args.get("search")

    if search:

        all_products = Product.query.filter(
            Product.name.ilike(f"%{search}%")
        ).all()

    else:

        all_products = Product.query.all()

    return render_template(
        "products.html",
        products=all_products
    )
@app.route("/add-product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        new_product = Product(
            name=request.form["name"],
            category=request.form["category"],
            price=float(request.form["price"]),
            quantity=int(request.form["quantity"])
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for("products"))

    return render_template("add_product.html")
@app.route("/edit-product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        product.name = request.form["name"]
        product.category = request.form["category"]
        product.price = float(request.form["price"])
        product.quantity = int(request.form["quantity"])

        db.session.commit()

        return redirect(url_for("products"))

    return render_template(
        "edit_product.html",
        product=product
    )
@app.route("/delete-product/<int:id>")
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)

    db.session.commit()

    return redirect(url_for("products"))
# -----------------------------
# Categories Page
# -----------------------------
@app.route("/categories")
def categories():

    all_categories = Category.query.all()

    return render_template(
        "categories.html",
        categories=all_categories
    )
@app.route("/add-category", methods=["GET", "POST"])
def add_category():

    if request.method == "POST":

        new_category = Category(
            name=request.form["name"]
        )

        db.session.add(new_category)
        db.session.commit()

        return redirect(url_for("categories"))

    return render_template("add_category.html")
@app.route("/delete-category/<int:id>")
def delete_category(id):

    category = Category.query.get_or_404(id)

    db.session.delete(category)

    db.session.commit()

    return redirect(url_for("categories"))

# -----------------------------
# Suppliers Page
# -----------------------------
@app.route("/suppliers")
def suppliers():

    all_suppliers = Supplier.query.all()

    return render_template(
        "suppliers.html",
        suppliers=all_suppliers
    )
@app.route("/add-supplier", methods=["GET", "POST"])
def add_supplier():

    if request.method == "POST":

        new_supplier = Supplier(
            name=request.form["name"],
            contact=request.form["contact"]
        )

        db.session.add(new_supplier)
        db.session.commit()

        return redirect(url_for("suppliers"))

    return render_template("add_supplier.html")
@app.route("/delete-supplier/<int:id>")
def delete_supplier(id):

    supplier = Supplier.query.get_or_404(id)

    db.session.delete(supplier)

    db.session.commit()

    return redirect(url_for("suppliers"))
# -----------------------------
# Run Flask App
# -----------------------------
with app.app_context():
    db.create_all()
if __name__ == "__main__":

    app.run(debug=True)