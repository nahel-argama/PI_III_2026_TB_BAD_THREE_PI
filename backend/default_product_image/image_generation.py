import base64
import io
from dataclasses import dataclass

import httpx
import requests
from PIL import Image
import google.genai as genai
import google.genai.types as types

import config.settings as env


@dataclass(frozen=True)
class ImageGenerationFailure:
    pass


@dataclass(frozen=True)
class ImageGenerationSuccess:
    image_bytes: bytes
    format: str
    mime_type: str
    size: int


def generate_product_image_cloudflare(
    product_name: str,
) -> ImageGenerationSuccess | ImageGenerationFailure:
    prompt = f"""
    Fotografia profissional de alimentos de {product_name}.

    A imagem deve conter APENAS o produto agrícola "{product_name}".

    Produto único centralizado no quadro.
    Fundo branco.
    Altamente realista.
    Cores naturais.
    Iluminação de estúdio.
    Textura detalhada.

    Sem texto.
    Sem rótulos.
    Sem marca d'água.
    Sem embalagem.
    Sem pessoas.
    Sem objetos adicionais.
    Sem outros produtos.
    """

    headers = {
        "Authorization": f"Bearer {env.CF_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt,
        "width": 256,
        "height": 192,
    }

    url = f"{env.CF_ENDPOINT}/{env.CF_ACCOUNT_ID}/ai/run/{env.CF_MODEL}"

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return ImageGenerationFailure()

    try:
        data = response.json()
        result = data.get("result", {})
        image_base64 = result.get("image")

        image_bytes = base64.b64decode(image_base64)
    except Exception as e:
        return ImageGenerationFailure()

    if not image_bytes:
        return ImageGenerationFailure()

    try:
        image = Image.open(io.BytesIO(image_bytes))
        image_format = image.format or "JPEG"
        mime_type = Image.MIME.get(image_format, "image/jpeg")

        return ImageGenerationSuccess(
            image_bytes=image_bytes,
            format=image_format,
            mime_type=mime_type,
            size=len(image_bytes),
        )
    except Exception as e:
        return ImageGenerationFailure()


def generate_product_image_gemini(
    product_name: str,
) -> ImageGenerationSuccess | ImageGenerationFailure:
    try:
        client = genai.Client(
            api_key=env.GEMINI_KEY,
        )
        prompt = f"""
        Forneça a URL de uma imagem de fotografia do produto '{product_name}'.

        Requisitos:
        - Retorne APENAS a URL bruta da imagem.
        - NÃO inclua nenhuma formatação em markdown, nenhuma explicação adicional, nenhum texto.
        - Procure por uma image com o nome do produto no link, quero que vocẽ faça uma busca
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        url = response.text.strip()

        if not url.startswith("http://") and not url.startswith("https://"):
            return ImageGenerationFailure()
    except Exception:
        return ImageGenerationFailure()

    try:
        img_response = requests.get(url, timeout=10)
        img_response.raise_for_status()
        image_bytes = img_response.content
    except Exception:
        return ImageGenerationFailure()

    if not image_bytes:
        return ImageGenerationFailure()

    try:
        image = Image.open(io.BytesIO(image_bytes))
        image_format = image.format or "JPEG"
        mime_type = Image.MIME.get(image_format, "image/jpeg")

        return ImageGenerationSuccess(
            image_bytes=image_bytes,
            format=image_format,
            mime_type=mime_type,
            size=len(image_bytes),
        )
    except Exception:
        return ImageGenerationFailure()


def generate_product_image(
    product_name: str,
) -> ImageGenerationSuccess | ImageGenerationFailure:
    return generate_product_image_cloudflare(product_name)
