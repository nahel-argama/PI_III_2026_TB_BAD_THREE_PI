import google.genai as genai

import config.settings as settings

client = genai.Client(
    api_key=settings.GEMINI_KEY,
)


def generate_product_description(product_name: str) -> str:
    prompt = f"""
    Gere a descrição para o produto '{product_name}'.

    - É um produto de ecommerce do contexto agronômico
    - Máximo de 40 palavras.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text
