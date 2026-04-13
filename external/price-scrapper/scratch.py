import asyncio

import app.data as data


async def main():
    products = await data.get_products_names()
    print(products)


if __name__ == "__main__":
    asyncio.run(main())
