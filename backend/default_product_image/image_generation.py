import os

from gradio_client import Client
from PIL import Image

import config.settings as env

client = Client("mrfakename/Z-Image-Turbo", verbose=False, token=env.AI_KEY)


class ImageGenerationFailure:
    pass


class ImageGenerationSuccess:
    def __init__(self, image_bytes: bytes, format: str, mime_type: str, size: int):
        self.image_bytes = image_bytes
        self.format = format
        self.mime_type = mime_type
        self.size = size


def generate_product_image(
    product_name: str,
) -> ImageGenerationSuccess | ImageGenerationFailure:
    prompt = """
    You must generate a product image based on the name provided. The name came from CONAB's monthly PROHORT dataset.
    (CONAB refers to the Companhia Nacional de Abastecimento, Brazil's National Supply Company, which manages and tracks
    agricultural supply and food distribution data).

    The product names are without accents and special characters, and they are in Portuguese. For example, "milho"
    means "corn", "soja" means "soybean", and "trigo" means "wheat". The product name may also include additional
    information such as the type of product (e.g., "milho em grão" means "corn in grain") or the region of production
    (e.g., "soja do mato grosso" means "soybean from Mato Grosso").

    The image must be a flat, 2D representation of the product, with a solid color background. The product should
    be centered in the image and should be easily recognizable. The image should not contain any text or logos.
    It must have a resolution of 512x512 pixels and be in PNG format.

    Generate a product image for the following product: {product_name}.
    """

    prompt = prompt.format(product_name=product_name)
    try:
        result = client.predict(
            prompt=prompt,
            height=512,
            width=512,
            num_inference_steps=9,
            seed=42,
            randomize_seed=True,
            api_name="/generate_image",
        )
    except Exception as e:
        print("Error during image generation: ", e)
        return ImageGenerationFailure()

    file_path = result[0]
    if not file_path:
        return ImageGenerationFailure()

    print("Generated image file path: ", file_path)

    try:
        image = Image.open(file_path)
        image_bytes = image.tobytes()

        return ImageGenerationSuccess(
            image_bytes=image_bytes,
            format=image.format,
            mime_type=image.get_format_mimetype(),
            size=len(image_bytes),
        )
    except Exception as e:
        print("Error reading the generated image file: ", e)
        return ImageGenerationFailure()
