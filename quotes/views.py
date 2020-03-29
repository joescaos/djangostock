from django.shortcuts import render, HttpResponse, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm

# Create your views here.
import requests
import json


def home(request):

    if request.method == 'POST':
        ticker = request.POST['ticker']
        # pk_6a9bb59b7b714696a59c2c986d5d2160
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_6a9bb59b7b714696a59c2c986d5d2160")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = 'Error...'

        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {
            'ticker': "Enter a Ticker Symbol Above..."
        })


def about(request):

    return render(request, 'about.html', {

    })


def add_stock(request):

    if request.method == 'POST':
        # ticker = request.POST['ticker']
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added successfully")
            return redirect('add_stock')

    else:
        ticker = Stock.objects.all()
        output = []

        for ticker_item in ticker:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token=pk_6a9bb59b7b714696a59c2c986d5d2160")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = 'Error...'
        return render(request, 'add_stock.html', {
            'ticker': ticker,
            'output': output
        })


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted successfully"))
    return redirect('delete_stock')


def delete_stock(request):
    ticker = Stock.objects.all()

    return render(request, 'delete_stock.html', {
        'ticker': ticker,
    })
