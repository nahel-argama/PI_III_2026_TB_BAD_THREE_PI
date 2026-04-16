import asyncio

import app.data as data


async def main():
    products = await data.get_daily_products_names(data.get_today_filename())
    print(products)


if __name__ == "__main__":
    asyncio.run(main())
