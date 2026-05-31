import base64
import io
from dataclasses import dataclass

import requests
from PIL import Image

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


def generate_product_image(
    product_name: str,
) -> ImageGenerationSuccess | ImageGenerationFailure:
    prompt = f"""
    Professional food photography of {product_name}.

    The image must contain ONLY the agricultural product "{product_name}".

    Single product centered in the frame.
    White background.
    Highly realistic.
    Natural colors.
    Studio lighting.
    Detailed texture.

    No text.
    No labels.
    No watermark.
    No packaging.
    No people.
    No additional objects.
    No other products.
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
