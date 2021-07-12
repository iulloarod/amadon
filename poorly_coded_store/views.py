from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    if "spent_amazon" not in request.session:
        request.session["spent_amazon"] = 0
    if "n_items" not in request.session:
        request.session["n_items"] = 0
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)


def payment(request):
    if request.method == "POST":
        prod_id= Product.objects.filter(id=int(request.POST["id"]))
        pro_data = prod_id.all().values("price")
        quantity_from_form = int(request.POST["quantity"])
        total_charge = quantity_from_form * pro_data[0]["price"]
        print(total_charge)
        Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
        last_order= Order.objects.last()
        print(last_order.id)
        request.session["n_items"] = request.session["n_items"] + int(quantity_from_form)
        request.session["spent_amazon"] = request.session["spent_amazon"] + int(total_charge)
        context ={
            "id": last_order.id,
        }
        return redirect ("/checkout/"+str(last_order.id))


def checkout(request, id):
    order_id = Order.objects.get(id=id)
    if request.method == "GET":
        context= {
            "total": order_id.total_price,
            "n_items": request.session["n_items"],
            "spent_amazon": request.session["spent_amazon"],
        }
        return render(request, "store/checkout.html", context)