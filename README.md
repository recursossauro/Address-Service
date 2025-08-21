📍 Address-Service

Multilingual address management API for Django applications

https://img.shields.io/badge/Django-4.2-green
https://img.shields.io/badge/Python-3.10-blue
🎯 What is Address-Service?

Address-Service is a modular solution for address management in Django applications. It provides country-specific models while maintaining the linguistic and cultural authenticity of each addressing pattern.
✨ Key Features

    🌍 Country-specific models with fields in local language

    🇧🇷 Brazilian system complete in Portuguese

    🇺🇸 US system in English

    📝 Generic system with textarea for special cases

    🔌 RESTful API ready for integration

    🏗️ Modular and easy to integrate into any Django project

🗺️ Implemented Address Systems
🇧🇷 Brazilian (pt-BR)

    Formatted and validated ZIP code (CEP)

    Fields in Portuguese: logradouro, bairro, município, UF

    Brazilian state validation

🇺🇸 US (en-US)

    ZIP code support

    Fields in English: street, city, state, ZIP code

    US state validation

🌐 Generic (textarea)

    Free field for various inter

    national addresses

    Flexible solution for non-implemented countries

    No specific validation

🏗️ Architecture
text
text

address_service/
├── core/
│   ├── models.py
│   ├── api/
│   └── validators/
├── countries/
│   ├── br/              # Brazilian System
│   │   ├── models.py
│   │   └── validators.py
│   ├── us/              # US System
│   │   ├── models.py
│   │   └── validators.py
│   └── generic/         # Generic System
│       └── models.py
└── postcard/            # Demo application

🚀 How to Use
1. Installation
bash

pip install -r requirements.txt

2. Configuration
python

# settings.py
INSTALLED_APPS = [
    ...,
    'address_service.core',
    'address_service.countries.br',
    'address_service.countries.us',
    'address_service.countries.generic',
    'address_service.postcard',  # Demo only
]

3. Usage by Country
python

# Brazilian Address
from address_service.countries.br.models import BrazilianAddress

endereco_br = BrazilianAddress.objects.create(
    cep="22050-002",
    logradouro="Praia de Botafogo",
    numero="300",
    bairro="Botafogo",
    municipio="Rio de Janeiro",
    uf="RJ"
)

# US Address
from address_service.countries.us.models import USAddress

endereco_us = USAddress.objects.create(
    zip_code="10001",
    street="5th Avenue",
    number="123",
    city="New York",
    state="NY"
)

# Generic Address
from address_service.countries.generic.models import GenericAddress

endereco_generic = GenericAddress.objects.create(
    free_text="123 Main St, Toronto, ON M5V 2T6, Canada"
)

📋 Demo Application: Postal

The postcard/ directory contains a sample application demonstrating Address-Service integration in a real scenario: postcard mailing system.
🧪 Postal Purpose

    ✅ Validate the Address-Service concept

    ✅ Demonstrate real-world integration

    ✅ Test international addressing flows

    ✅ Serve as implementation reference

🔌 API Endpoints
http

GET    /api/address/br/          # Brazilian addresses
POST   /api/address/br/          # Create BR address

GET    /api/address/us/          # US addresses
POST   /api/address/us/          # Create US address

GET    /api/address/generic/     # Generic addresses
POST   /api/address/generic/     # Create generic address

🛠️ Development
Requirements

    Python 3.10+

    Django 4.2+

Development Setup
bash

git clone https://github.com/your-username/address-service.git
cd address-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

👥 Author

Leonardo Düchting de Abreu e Lima - GitHub
💡 Future Features

    More countries (Portugal, Argentina, etc.)

    Enhanced ZIP code validation

    Unified admin interface

    Address change history

Address-Service: Respecting the cultural diversity of world addresses! 🚀


