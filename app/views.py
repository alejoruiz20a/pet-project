from django.shortcuts import render, redirect
from .models import User, Pet
import time
from pytz import timezone
from datetime import datetime
import spacy
import random

#PARAMETROS DE BALANCEO

def index(request):
    mesage = ""
    if request.method == "POST":
        user = request.POST["user"]
        password = request.POST["password"]
        try:
            usr = User.objects.get(user = user)
            if password == usr.password:    
                request.session["user"] = user
                return redirect("pet/")
            else:
                mesage = "Password not matching."
        except: 
            mesage = "User not found."
    return render(request,'index.html',{
    "mesage":mesage
    })

def register(request):
    mesage = ""
    if request.method == "POST":
        user = request.POST['user']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        try:
            User.objects.get(user=user)
            mesage = "That username is already on use."
        except:
            if password1==password2:
                User.objects.create(user=user,password = password1,money = 0)
                mesage="You are registered now."
            else: 
                mesage="Passwords don't match."
    return render(request,'register.html',{
        "mesage":mesage
    })

nlp = spacy.load("es_core_news_sm")

# Definir patrones para identificar acciones
PATTERNS = {
    "change name" : ["change name"],
    "eat" : ["alimentar", "dar de comer", "comer","eat","feed"],
    "play" : ["jugar", "divertirse", "entretenimiento", "juego","play"],
    "clean" : ["limpiar", "bañar", "aseo", "higiene","clean"],
    "sleep" : ["dormir","sleep"],
    "work" : ["trabajar","work","get a job"],
    "kill" : ["kill kill kill"],
    "hat" : ["wear hat", "hat"]
}

def determine_action(text):
    doc = nlp(text)
    for action, keywords in PATTERNS.items():
        for keyword in keywords:
            if keyword in text:
                return action
    return 0  # Acción no reconocida

def pet(request):
    user = request.session.get("user",None)
    pet = Pet()
    console = "..."
    hat = False
    try:
        pet = Pet.objects.get(id_user=User.objects.get(user = user))
        if pet.health == 0:
            pet.delete()
            pet = Pet.objects.create(name = "Pet", image = str(random.randint(1,3)), health = 100, lasthealth = datetime.now(), happiness = 50, lasthapiness = datetime.now(), energy = 100, lastenergy = datetime.now(), hunger = 50, lasthunger = datetime.now(), shittiness = 100, lastshit = datetime.now(), age = 0, money = 0, lastjob = datetime.now(), birthday = datetime.now(), id_user = User.objects.get(user = user))
    except:
        pet = Pet.objects.create(name = "Pet", image = str(random.randint(1,3)), health = 100, lasthealth = datetime.now(), happiness = 50, lasthapiness = datetime.now(), energy = 100, lastenergy = datetime.now(), hunger = 50, lasthunger = datetime.now(), shittiness = 100, lastshit = datetime.now(), age = 0, money = 0, lastjob = datetime.now(), birthday = datetime.now(), id_user = User.objects.get(user = user))
    
    #Ajuste de hambre
    hungerDif = datetime.now().astimezone(timezone("UTC"))-pet.lasthunger
    hungerDif = int((hungerDif.total_seconds() / 60) / 3) 
    if (hungerDif>=1):
        pet.hunger -= hungerDif
        pet.lasthunger = datetime.now()
        if pet.hunger<0:
            pet.hunger = 0
    
    #Ajuste de energia
    energyDif = datetime.now().astimezone(timezone("UTC"))-pet.lastenergy
    energyDif = int((energyDif.total_seconds() / 60) / 8)
    if (energyDif>=1):
        pet.energy -= energyDif
        pet.lastenergy = datetime.now()
        if pet.energy<0:
            pet.energy = 0

    #Ajuste de higiene
    shitDif = datetime.now().astimezone(timezone("UTC"))-pet.lastshit
    shitDif = int((shitDif.total_seconds() / 60) / 5)
    if (shitDif>=1):
        pet.shittiness -= shitDif
        pet.lastshit = datetime.now()
        if pet.shittiness<0:
            pet.shittiness = 0

    #Ajuste de felicidad
    happyDif = datetime.now().astimezone(timezone("UTC"))-pet.lasthapiness
    happyDif = int((happyDif.total_seconds() / 60 ) / 4)
    if (happyDif>=1):
        pet.happiness -= happyDif
        pet.lasthapiness = datetime.now()
        if pet.happiness<0:
            pet.happiness = 0

    #Ajuste de edad
    ageDif = datetime.now().astimezone(timezone("UTC"))-pet.birthday
    ageDif = int(ageDif.days)
    if ageDif != pet.age:
        pet.age = ageDif

    if pet.health == 0:
        healthDif = datetime.now().astimezone(timezone("UTC"))-pet.lasthealth
        healthDif = int((healthDif.total_seconds/60) / 3)
        if healthDif >= 1:
            pet.happiness -= healthDif
    else: 
        pet.lasthealth=datetime.now()

    

    if request.method == "POST":
        instruction = str(request.POST['instruction'])
        respuesta = determine_action(instruction.lower())
        match(respuesta):
            case "change name":
                pet.name = instruction[instruction.index("name ") + 5:]
                console = f"It's name now is {pet.name}!"
            case "eat": 
                if pet.money>=5:
                    pet.hunger += 10
                    pet.money -= 5
                    if pet.hunger >= 100:
                        pet.hunger = 100
                        console = f"{pet.name} is now full!"
                    else:
                        console = f"{pet.name} ate something!"
                    pet.lasthunger = datetime.now()
                else: 
                    console = f"{pet.name} doesn't have enough money."
            case "play":
                pet.happiness += 20
                pet.energy -= 2
                if pet.happiness >= 100:
                    pet.happiness = 100
                    console = f"{pet.name} is happy! :)"
                else:
                    console = f"You just played with {pet.name}!"
                pet.lasthapiness = datetime.now()
            case "clean":
                pet.shittiness += 30
                pet.happiness -= 5
                if pet.shittiness >= 100:
                    pet.shittiness = 100
                    console = f"{pet.name} is clean!"
                else:
                    console = f"You cleaned {pet.name}!"
                pet.lastshit = datetime.now()
            case "sleep":
                pet.energy += 80
                pet.hunger -= 30
                if pet.energy >= 100:
                    pet.energy = 100
                    console = f"{pet.name} is full of energy!"
                else:
                    console = f"{pet.name} slept!"
                pet.lastenergy = datetime.now()
            case "work":
                earned = random.randint(1,15)
                if pet.energy >= earned//2:
                    pet.money += earned
                    pet.energy -= int(earned//2)
                    console = f"{pet.name} worked and won ${earned}!"
                else:
                    console = f"{pet.name} doesn't have enough money to work."
                if pet.energy<0:
                    pet.energy = 0
                
            case "hat":
                if hat:
                    hat = False
                else:
                    hat = True
            case "kill":
                pet.health = 0

    pet.save()

    if pet.health == 0:
        return redirect("/")

    return render(request, "pet.html", {
        "user" : user,
        "pet" : pet,
        "console" : console,
        "hat" : hat
    })

"""""
  -----   NOTAS PARA EL ALEJO DEL FUTURO   -----   
    *Hay un error en el que al eliminar un pet, sigue en la base de datos pero a la vez crea otro pet en la base de datos, haciendo un ejercito de pets.
"""""
