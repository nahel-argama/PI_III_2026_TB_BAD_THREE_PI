import os
import django

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from category.models import Category

CATEGORIES = [
    "Frutas",
    "Verduras",
    "Legumes",
    "Grãos e Cereais",
    "Laticínios",
    "Carnes e Ovos",
    "Mel e Derivados",
    "Bebidas",
    "Doces e Geleias",
    "Temperos e Ervas",
    "Mudas e Sementes",
    "Outros"
]

def seed_categories():
    print("Iniciando a criação de categorias...")
    for name in CATEGORIES:
        category, created = Category.objects.get_or_create(name=name)
        if created:
            print(f"✅ Categoria criada: {name}")
        else:
            print(f"ℹ️ Categoria já existe: {name}")
    print("Concluído!")

if __name__ == '__main__':
    seed_categories()
