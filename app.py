from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "gunita_secret"

# =========================
# MENU DATA
# =========================
MENU = {
    "coffee": [
        {"id": 1, "name": "Matcha Latte", "price": 120, "img": "matchalatte.png", "tagline": "Tahimik na higop, payapang gunita."},
        {"id": 2, "name": "Kapeng Barako", "price": 100, "img": "barako.png", "tagline": "Matapang na kape, alaalang nananatili"},
        {"id": 3, "name": "Cappuccino", "price": 130, "img": "cappuccino.png", "tagline": "Bula ng saya sa bawat higop."},
        {"id": 4, "name": "Espresso", "price": 90, "img": "espresso.png", "tagline": "Maikli man, matindi ang gunita."},
        {"id": 5, "name": "Ube Latte", "price": 140, "img": "ubelatte.png", "tagline": "Tamis ng ube, lambing ng alaala."},
        {"id": 6, "name": "Hazelnut", "price": 150, "img": "hazelnut.jpg", "tagline": "Matamis na alaala sa bawat higop."},
    ],

    "frappe": [
        {"id": 7, "name": "Caramel Frappe", "price": 140, "img": "caramelF.jpg", "tagline": "Matamis na sandaling babalik-balikan."},
        {"id": 8, "name": "Chocolate Frappe", "price": 140, "img": "chocolateF.jpg", "tagline": "Lasa ng comfort sa bawat tagpo."},
        {"id": 9, "name": "Cookies & Cream Frappe", "price": 130, "img": "cookies&creamF.jpg", "tagline": "Masayang gunita sa bawat blend."},
        {"id": 10, "name": "Ube Frappe", "price": 150, "img": "ubeF.jpg", "tagline": "Kulay at tamis ng pagka-Pilipino."},
        {"id": 11, "name": "Strawberry Frappe", "price": 145, "img": "strawberryF.jpg", "tagline": "Preskong tamis na nakakakilig."},
        {"id": 12, "name": "Vanilla Frappe", "price": 155, "img": "vanilla.jpg", "tagline": "Preskong panaginip sa bawat lagok."},
    ],

    "pastries": [
        {"id": 13, "name": "Cinnamon Roll", "price": 90, "img": "pastries.jpg", "tagline": "Init at tamis ng umagang gunita."},
        {"id": 14, "name": "Chocolate Muffin", "price": 80, "img": "muffin.jpg", "tagline": "Malambing na tsokolate"},
        {"id": 15, "name": "Cheesy Ensaymada", "price": 120, "img": "ensaymada.jpg", "tagline": "Klasikong sarap na parang tahanan."},
        {"id": 16, "name": "Brownie", "price": 85, "img": "brownies.jpg", "tagline": "Siksik na tamis, siksik na alaala."},
        {"id": 17, "name": "Cassava", "price": 70, "img": "cassava.jpg", "tagline": "Tradisyong Pinoy na may lambing."},
        {"id": 18, "name": "Egg Tart", "price": 95, "img": "eggtart.jpg", "tagline": "Isang kagat, isang alaala ng tayo."},
    ]
}

# =========================
# CART BADGE COUNTER (IMPORTANT)
# =========================
@app.context_processor
def cart_counter():
    cart = session.get("cart", [])
    total_items = sum(item.get("qty", 1) for item in cart)
    return dict(cart_count=total_items)

# =========================
# HOME
# =========================
@app.route('/')
def home():
    return render_template('home.html')

# =========================
# MENU PAGE
# =========================
@app.route('/menu')
def menu_page():
    return render_template('menu.html', menu=MENU)

# =========================
# GET CART
# =========================
def get_cart():
    return session.setdefault("cart", [])

# =========================
# ADD TO CART
# =========================
@app.route("/add/<category>/<int:item_id>")
def add_to_cart(category, item_id):

    cart = get_cart()

    item = next((x for x in MENU[category] if x["id"] == item_id), None)

    if item:
        for c in cart:
            if c["id"] == item_id:
                c["qty"] = c.get("qty", 1) + 1
                break
        else:
            cart.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "img": item["img"],
                "qty": 1
            })

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("menu_page"))

# =========================
# INCREASE QTY
# =========================
@app.route("/increase/<int:item_id>")
def increase_qty(item_id):

    cart = get_cart()

    for item in cart:
        if item["id"] == item_id:
            item["qty"] = item.get("qty", 1) + 1
            break

    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

# =========================
# DECREASE QTY
# =========================
@app.route("/decrease/<int:item_id>")
def decrease_qty(item_id):

    cart = get_cart()

    for item in cart:
        if item["id"] == item_id:
            item["qty"] = item.get("qty", 1) - 1

            if item["qty"] <= 0:
                cart.remove(item)
            break

    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

# =========================
# CART PAGE
# =========================
@app.route("/cart")
def cart():

    cart = get_cart()

    for item in cart:
        item.setdefault("qty", 1)

    total = sum(item["price"] * item["qty"] for item in cart)

    session["cart"] = cart
    session.modified = True

    return render_template("cart.html", cart=cart, total=total)

# =========================
# REMOVE ITEM
# =========================
@app.route("/remove/<int:item_id>")
def remove_item(item_id):

    cart = get_cart()
    cart = [item for item in cart if item["id"] != item_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))

# =========================
# CHECKOUT
# =========================
@app.route("/checkout", methods=["POST"])
def checkout():
    session.pop("cart", None)
    return "<h2>Order Submitted ☕ Thank you for ordering at Gunita Coffee!</h2>"

# =========================
# RESET CART
# =========================
@app.route("/reset-cart")
def reset_cart():
    session.pop("cart", None)
    return "Cart reset successful"

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port, debug=True)