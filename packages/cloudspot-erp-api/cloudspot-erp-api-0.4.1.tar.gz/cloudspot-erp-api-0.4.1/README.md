# Cloudspot API wrapper
Basic wrapper for the Cloudspot ERP API.

# Use cases
This wrapper has two use cases:
1. Authenticate and authorize users on an external app, linked to Cloudspot ERP
2. Get data (products, clients,...) from a company that is present on the Cloudspot ERP

# Getting started

### Install

Install with pip.

```python
pip install cloudspot-erp-api
```

### Import

Depending on your use case, you'll need to import either ```CloudspotERP_UserAPI``` or ```CloudspotERP_CompanyAPI```.

```python
# Use case 1
from cloudspot.api import CloudspotERP_UserAPI

# Use case 2
from cloudspot.api import CloudspotERP_CompanyAPI
```

# Functionalities

## CloudspotERP_UserAPI

**This class is used to authenticate and authorize a user on an external app.**

### Setup

When setting up the class, one parameter is expected: the name/slug of the external application.
This is a crucial and important step. This name/slug is used to determine what application is making the request and what permissions are linked to it.
By using a wrong name/slug, your users will be able to authenticate themselves if their credentials are correct but the permissions will not be mapped correctly. This may lead to giving users too much or too little permissions on the external application.

```python
from cloudspot.api import CloudspotERP_UserAPI
api = CloudspotERP_UserAPI('[NAME_OF_EXTERNAL_APP]')
```

### Authentication and authorization

After setting up the connection, you can use the ```api``` to send requests to the Cloudspot ERP.
Users that are trying to log in will give their username and password. Send this username and password to the ERP to validate their credentials.
If correct, the ERP will return a token and the user's permissions for the external application. If not correct, a ```BadCredentials``` error will be raised.

```python
try:
    api.authenticate(username, password)
except BadCredentials as e:
    print(e)
```

If a request is succesful, you can retrieve the returned token and permissions by using ```api.token``` and ```api.permissions``` respectively.

```python
token = api.token
for perm in api.permissions.items():
    print(perm.permission) # Contains the slug of the permission
```

### Retrieving permissions

You can retrieve the permissions of an user by using the ```api``` object.

If you've already authenticated the user before using the ```api```, you do not need to supply a token to the function.
If you're using a new ```api``` object and want to retrieve the permissions for a specific token without authenticating first, you can supply the token to the function.

If succesful, the permissions will be attached to ```api.permissions``` and overwrite any previous permissions.

Retrieve permissions by authenticating first.

```python

api.authenticate(username, password)
api.get_permissions()
    
for perm in api.permissions.items():
    print(perm.permission)
```

Retrieve permissions by supplying a token. You can catch the error ```NoValidToken``` to handle a token that is not valid.

```python

try:
    api.get_permissions(token)
except NoValidToken as e:
    print(e)
    
for perm in api.permissions.items():
    print(perm.permission)
```

### Retrieving user info

By default, an empty ```User``` object will be attached to the ```api```. You can retrieve the object with ```api.user```.
To populate the ```User```, you need to execute the function ```api.get_user()``` first.

The ```User``` object has three attributes: ```first_name```, ```last_name``` and ```email```.

If you've already authenticated the user before using the ```api```, you do not need to supply a token to the function.
If you're using a new ```api``` object and want to retrieve the user for a specific token without authenticating first, you can supply the token to the function.

If succesful, the user will be attached to ```api.user``` and overwrite any previous user.

Retrieve user by authenticating first.

```python

api.authenticate(username, password)
api.get_user()
    
print(user.first_name)
```

Retrieve user by supplying a token. You can catch the error ```NoValidToken``` to handle a token that is not valid.

```python

try:
    api.get_user(token)
except NoValidToken as e:
    print(e)
    
print(user.first_name)
```


### Basic example

In the below example we'll demonstrate a simple external application where a user can log into.
The credentials of the user will be verified by the ERP and, if succesful, will return a token and the permissions.

This example is written in Django.

#### Login

```html
<!-- login.html -->
<!-- This is the first view that the user will see and use to log in to the application -->
<html>
<head>
    <title>Login</title>
</head>
<body>

    <h1>Login external app</h1>

    <form method="POST">
    {% csrf_token %}

    <p>
        <label>Username</label>
        <input type="text" name="username" />
    </p>

    <p>
        <label>Password</label>
        <input type="password" name="password" />
    </p>

    <p>
        <input type="submit" value="Login" />
    </p>

</form>
</body>
</html>
```

#### Dashboard

```html
<!-- dashboard.html -->
<!-- This page is shown after the user has succesfully logged in. It will show the returned token and permissions. -->
<html>
<head>
    <title>Login</title>
</head>
<body>

    <h1>Welcome!</h1>

    <p>
        Token: {{ token }}
    </p>
    
    <p>
        Permissions:<br>

        {% for perm in perms %}
            {{ perm }} <br>
        {% endfor %}
    </p>
</body>
</html>
```

#### View

```python
from django.http import HttpResponse
from django.shortcuts import render

from django.views import View

from cloudspot.api import CloudspotERP_UserAPI
from cloudspot.constants.errors import BadCredentials

class LoginView(View):
    template_name = 'login.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        api = CloudspotERP_UserAPI('timeapp')
        
        try:
            api.authenticate(username, password)
        except BadCredentials as e:
            return HttpResponse(e)
        
        data = { 'token' : api.token }
        
        perms = []
        for perm in api.permissions.items():
            perms.append(perm.permission)
            
        data['perms'] = perms
        
        return render(request, 'dashboard.html', data)
```

#### Testing the example

We have created a user in the ERP with the following permissions:

![ERP permissions](docs/external-app-erp-permissionsforuser.PNG)

We go to our external application and log in:

![External app Login](docs/external-app-login.PNG)

If our credentials are correct, we go to the dashboard and see our token and permissions:

![External app Dashboard](docs/external-app-dashboard.PNG)

If our credentials are incorrect, we get the following message:

![External app BadCredentials](docs/external-app-badcredentials.PNG)


## CloudspotERP_CompanyAPI

**This class is used to retrieve data from a company.**

### Setup

When setting up the class, one parameter is expected: the generated API token of the company.
This token can be generated by an ERP administrator for a specific company.
A token can have the right to:
- See all products
- See all clients

```python
from cloudspot.api import CloudspotERP_CompanyAPI
api = CloudspotERP_CompanyAPI('[TOKEN]')
```

After setting up the connection, you can use the ```api``` to send requests to the Cloudspot ERP.

### All products
Below method will allow you to retrieve all the products that are available inside the ERP and are linked to the company by the token.
The ```.list()``` method will return one ```Artikels``` object, which is a list containing one or multiple ```Artikel``` objects.

```python
artikels = api.artikels.list()

for artikel in artikels.items():
    print('naam: ', artikel.naam)
```

#### Available attributes

Following attributes are available for the ```Artikel``` object:

| Attribute        | Type | Remarks |
| ------------- | ------------- | ------------- |
| naam  | string | Name of the product |
| beschrijving  | text | Long description of the product |
| SKU  | string | Stock Keeping Unit |
| voorraad_bijhouden  | string | Can only contain one of these three values: "NIET" / "FYSIEK" / "DIGITAAL" |
| op_voorraad  | float | How many units are currently in stock, only applicable of voorraad_bijhouden is "FYSIEK" |
| product_url  | url | External URL with the product information |
| verkoopprijs_excl  | float | Sales price, excl. VAT |
| verkoopprijs_incl  | float | Sales price, incl. VAT |
| inkoopprijs_excl  | float | Purchase price, excl. VAT |
| inkoopprijs_incl  | float | Purchase price, incl. VAT |
| BTW  | float | Percentage of VAT applicable to the product |
| bestellingtype  | string | Can only contain one of these two values: "IDEAAL" / "BESTELLING" |
| units_per_bestelling  | float | Minimum amount of units needed for an order to the vendor |
| status  | string | Can only contain one of these three values: "ZICHTBAAR" / "NIET_VERKOOPBAAR" / "GEDEACTIVEERD" |

### All clients
Below method will allow you to retrieve all the clients that are available inside the ERP and are linked to the company by the token.
The ```.list()``` method will return one ```Klanten``` object, which is a list containing one or multiple ```Klant``` objects.

```python
klanten = api.klanten.list()

for klant in klanten.items():
    print('voornaam: ', klant.voornaam)
```

#### Available attributes

Following attributes are available for the ```Klant``` object:

| Attribute        | Type | Remarks |
| ------------- | ------------- | ------------- |
| klantennummer  | integer | Client number/reference |
| aanspreektitel  | string | Can only contain one of these two values: "Mijnh." / "Mevr." |
| voornaam  | string | First name of client |
| achternaam  | string | Last name of client |
| straat  | string | Street |
| huisnummer  | string | House number |
| busnummer  | string | Box number |
| postcode  | string | Zipcode |
| plaats  | string | Place/region |
| land  | string | Two letter country code (ex. BE/NL/FR/...) |
| geboortedatum  | date | Birthday of client |
| geboorteplaats  | string | Place of birth |
| is_bedrijf  | boolean | Indicates wether the client is a company or not. True = client is a company, False = client is not a company |
| bedrijfsnaam  | string | Name of the company. Only applicable if is_bedrijf is True |
| BTW_nummer  | string | VAT number of the company. Only applicable if is_bedrijf is True |
| ondernemingsnummer  | string | KBO number of the company. Only applicable if is_bedrijf is True |


### Error handling
Basic error handling has been added.
You can check if an error has occured during a call by checking the hasError attribute on the object.
If the hasError attribute has been set to True, an Error object will be attached to the error attribute of the same object.
The Error object contains one attribute: message. This will contain the error message.

```python
artikels = api.artikels.list()

if artikels.hasError:
    print('error: ', artikels.error.message)
```