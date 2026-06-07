import os
import django
from django.db import transaction

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from users.models import User
from producer.models import Producer
from retailer.models import Retailer
from address.models import Address
from wishlist.models import Wishlist

# Define Brazilian Regions and Address details
REGIONS = [
    {
        "region": "Norte",
        "state": "AM",
        "city": "Manaus",
        "postal_code": "69000000",
        "street": "Avenida Eduardo Ribeiro",
        "number": "100",
        "neighborhood": "Centro",
        "latitude": -3.119027,
        "longitude": -60.021736,
    },
    {
        "region": "Nordeste",
        "state": "PE",
        "city": "Recife",
        "postal_code": "50030230",
        "street": "Avenida Alfredo Lisboa",
        "number": "200",
        "neighborhood": "Bairro do Recife",
        "latitude": -8.063138,
        "longitude": -34.871197,
    },
    {
        "region": "Centro-Oeste",
        "state": "DF",
        "city": "Brasília",
        "postal_code": "70070600",
        "street": "Via S1",
        "number": "S/N",
        "neighborhood": "Zona Cívico-Administrativa",
        "latitude": -15.800000,
        "longitude": -47.860000,
    },
    {
        "region": "Sudeste",
        "state": "SP",
        "city": "São Paulo",
        "postal_code": "01001000",
        "street": "Praça da Sé",
        "number": "300",
        "neighborhood": "Sé",
        "latitude": -23.550520,
        "longitude": -46.633308,
    },
    {
        "region": "Sul",
        "state": "PR",
        "city": "Curitiba",
        "postal_code": "80020100",
        "street": "Rua XV de Novembro",
        "number": "400",
        "neighborhood": "Centro",
        "latitude": -25.428400,
        "longitude": -49.273300,
    }
]

# Define user details
PRODUCERS_DATA = [
    {
        "name": "Produtor do Norte",
        "email": "produtor.norte@example.com",
        "trade_name": "Frutas Tropicais da Amazônia",
        "document_type": "CNPJ",
        "document_number": "11111111111111",
    },
    {
        "name": "Produtor do Nordeste",
        "email": "produtor.nordeste@example.com",
        "trade_name": "Mel e Derivados do Sertão",
        "document_type": "CPF",
        "document_number": "11111111111",
    },
    {
        "name": "Produtor do Centro-Oeste",
        "email": "produtor.centro_oeste@example.com",
        "trade_name": "Grãos e Cereais Planalto",
        "document_type": "CNPJ",
        "document_number": "22222222222222",
    },
    {
        "name": "Produtor do Sudeste",
        "email": "produtor.sudeste@example.com",
        "trade_name": "Laticínios e Ovos da Mantiqueira",
        "document_type": "CPF",
        "document_number": "22222222222",
    },
    {
        "name": "Produtor do Sul",
        "email": "produtor.sul@example.com",
        "trade_name": "Legumes e Verduras dos Pampas",
        "document_type": "CNPJ",
        "document_number": "33333333333333",
    }
]

RETAILERS_DATA = [
    {
        "name": "Varejista do Norte",
        "email": "varejista.norte@example.com",
        "trade_name": "Supermercado Tacacá",
        "document_type": "CNPJ",
        "document_number": "44444444444444",
    },
    {
        "name": "Varejista do Nordeste",
        "email": "varejista.nordeste@example.com",
        "trade_name": "Mercadinho Asa Branca",
        "document_type": "CPF",
        "document_number": "44444444444",
    },
    {
        "name": "Varejista do Centro-Oeste",
        "email": "varejista.centro_oeste@example.com",
        "trade_name": "Sacolão Cerrado",
        "document_type": "CNPJ",
        "document_number": "55555555555555",
    },
    {
        "name": "Varejista do Sudeste",
        "email": "varejista.sudeste@example.com",
        "trade_name": "Hortifruti Paulistano",
        "document_type": "CPF",
        "document_number": "55555555555",
    },
    {
        "name": "Varejista do Sul",
        "email": "varejista.sul@example.com",
        "trade_name": "Armazém Pinheiral",
        "document_type": "CNPJ",
        "document_number": "66666666666666",
    }
]

DEFAULT_PASSWORD = "teste123"

def seed_users():
    print("Iniciando a criação de produtores e varejistas...")
    
    # 1. Create Producers
    for i, data in enumerate(PRODUCERS_DATA):
        email = data["email"]
        if User.objects.filter(email=email).exists():
            print(f"ℹ️ Produtor já existe: {email}")
            continue
            
        region_addr = REGIONS[i]
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    password=DEFAULT_PASSWORD,
                    name=data["name"],
                    user_type=User.USER_TYPE_PRODUCER,
                    is_active=True,
                    is_staff=False
                )
                
                producer = Producer.objects.create(
                    user=user,
                    document_type=data["document_type"],
                    document_number=data["document_number"],
                    trade_name=data["trade_name"]
                )
                
                address = Address.objects.create(
                    user=user,
                    street=region_addr["street"],
                    number=region_addr["number"],
                    neighborhood=region_addr["neighborhood"],
                    city=region_addr["city"],
                    state=region_addr["state"],
                    postal_code=region_addr["postal_code"],
                    latitude=region_addr["latitude"],
                    longitude=region_addr["longitude"]
                )
                
                print(f"✅ Produtor criado no {region_addr['region']}: {email} (Trade Name: {data['trade_name']})")
        except Exception as e:
            print(f"❌ Erro ao criar produtor {email}: {e}")

    # 2. Create Retailers
    for i, data in enumerate(RETAILERS_DATA):
        email = data["email"]
        if User.objects.filter(email=email).exists():
            print(f"ℹ️ Varejista já existe: {email}")
            continue
            
        region_addr = REGIONS[i]
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    password=DEFAULT_PASSWORD,
                    name=data["name"],
                    user_type=User.USER_TYPE_RETAILER,
                    is_active=True,
                    is_staff=False
                )
                
                retailer = Retailer.objects.create(
                    user=user,
                    document_type=data["document_type"],
                    document_number=data["document_number"],
                    trade_name=data["trade_name"]
                )
                
                # Retailer also needs a Wishlist
                Wishlist.objects.get_or_create(retailer=retailer)
                
                address = Address.objects.create(
                    user=user,
                    street=region_addr["street"],
                    number=region_addr["number"],
                    neighborhood=region_addr["neighborhood"],
                    city=region_addr["city"],
                    state=region_addr["state"],
                    postal_code=region_addr["postal_code"],
                    latitude=region_addr["latitude"],
                    longitude=region_addr["longitude"]
                )
                
                print(f"✅ Varejista criado no {region_addr['region']}: {email} (Trade Name: {data['trade_name']})")
        except Exception as e:
            print(f"❌ Erro ao criar varejista {email}: {e}")

    print("Concluído!")

if __name__ == '__main__':
    seed_users()
