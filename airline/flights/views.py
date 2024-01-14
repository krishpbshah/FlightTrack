from django import forms
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

from django.shortcuts import render, get_object_or_404

def book(request, flight_id):
    if request.method == "POST":
        passenger_id = request.POST.get("passenger")
        if passenger_id:
            passenger = get_object_or_404(Passenger, pk=int(passenger_id))
            flight = get_object_or_404(Flight, pk=flight_id)
            passenger.flights.add(flight)
            return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
        else:
            return HttpResponseBadRequest("Bad Request: no passenger chosen")

    # Handle GET request if needed
    # ...

