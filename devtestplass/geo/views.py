from django.http import request, response, HttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
import pyrebase
import requests
import folium

# Coneccion a base de datos
def conect_db():
    config = {
        'apiKey': "AIzaSyBuScIESdm6s4-IWHF9udvbW9TFWqMpS3U",
        'authDomain': "devtestplass-997e8.firebaseapp.com",
        'databaseURL': "https://devtestplass-997e8-default-rtdb.firebaseio.com/",
        'projectId': "devtestplass-997e8",
        'storageBucket': "devtestplass-997e8.appspot.com",
        'messagingSenderId': "948343803558",
        'appId': "1:948343803558:web:612825bf0d7bbb93212e67",
    }

    firebase = pyrebase.initialize_app(config)
    database = firebase.database()
    return database


# Vista index
def index(request):
    #Conectamos a la base de datos
    database = conect_db()
    #Obtenemos los usuarios
    users = database.child('usuarios').get()
    vals = dict()
    # Recorro los usuarios para hacer un diccionario
    for user in users.each():
        vals[user.key()] = user.val()

    #Crear Mapa usando la libreria folium
    map = folium.Map(location=[4.5851325, -74.1201214], zoom_start=2)

    # Recorro la el diccionario de usuarios creado
    for key, val in vals.items():
        # folium.Marker([4.5851325, -74.1201214], tooltip='Clic for more', popup='Andrey').add_to(m)
        # verifico si tiene latitud y longitud para crear un marcador
        if 'latitud' in val.keys() and 'longitud' in val.keys():
            folium.Marker([val['latitud'], val['longitud']], tooltip='Clic for more', popup=val['nombre']).add_to(map)
    
    # Obtengo la representacion html del objeto mapa
    map = map._repr_html_()
    context = {
        'map':map,
        'title': 'Index'
    }
    return render(request, 'geo/index.html', context )

# Funcion de creado
def push(request):
    #conecto a la base de datos
    database = conect_db()
    #creo el data
    data = {
        'id': request.POST.get('id'),
        'nombre': request.POST.get('name'),
        'apellido': request.POST.get('surname'),
        'direccion': request.POST.get('address'),
        'ciudad': request.POST.get('city'),
        'estadogeo': 'No Georreferenciado',
    }
    #Valido si tiene un id, de no ser asi no creo ningun registro
    if request.POST.get('id'):
        create = database.child('usuarios').push(data)

    return render(request, 'geo/crear.html')

# Vista lista
def list(request):
    #conecto a la base de datos
    database = conect_db()

    # Recorro los usuarios para hacer un diccionario
    users = database.child('usuarios').get()
    vals = dict()
    for user in users.each():
        vals[user.key()] = user.val()
    
    context = {
        'values': vals,
        'title': 'Lista'
        }
    return render(request, 'geo/listar.html', context )

#Funcion de borrado
def delete(request):
    #Conecto a la base de datos
    database = conect_db()

    #Verifico si es el metodo post y obtengo la key a borrar
    if request.method == 'POST':
        key = request.POST.get('key')  
        database.child('usuarios').child(key).remove()

    #Listo los usuarios
    users = database.child('usuarios').get()   

    # Recorro los usuarios para hacer un diccionario
    vals = dict()
    for user in users.each():
        vals[user.key()] = user.val()
    
    context = {
        'values': vals,
        'title': 'Lista'
        }

    return render(request, 'geo/listar.html', context )

def update(request):
    #Conecto a la base de datos
    database = conect_db()
    #Verifico si es el metodo post y obtengo la key a atualizar
    if request.method == 'POST':
        key = request.POST.get('key')          
        data = {
            'longitud': request.POST.get('longitude'),
            'latitud': request.POST.get('latitude'),
            'estadogeo': 'Georreferenciado',
        }
        database.child('usuarios').child(key).update(data)

    users = database.child('usuarios').get()   
    #Listo los usuarios
    vals = dict()
    for user in users.each():
        vals[user.key()] = user.val()
    # Recorro los usuarios para hacer un diccionario
    context = {
        'values': vals,
        'title': 'Lista'
        }

    return render(request, 'geo/listar.html', context )