import loguru
from databases import Database
from asyncio import run
import queries
import models
import asyncio

PORT=5432
HOST="localhost"
DB_NAME="postgress"
USER="postgres"
PASSWORD="postgres"


async def postgres_connection() -> Database:
    db = Database(
        url=f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}",
    )
    await db.connect()
    loguru.logger.debug("Returning postgres connection")
    return db


async def create_tables(conn: Database) -> None:
    await conn.execute(
        query=queries.DROP_COUNTRY
    )
    await conn.execute(
        query=queries.DROP_WEBSITE
    )
    await conn.execute(
        query=queries.DROP_CATEGORY
    )
    await conn.execute(
        query=queries.CREATE_TABLE_COUNTRY
    )
    await conn.execute(
        query=queries.CREATE_TABLE_CATEGORY
    )
    await conn.execute(
        query=queries.CREATE_TABLE_WEBSITE
    )
    loguru.logger.debug("Tables created")


async def populate_tables(conn: Database) -> None:
    await conn.execute(
        query=queries.POPULATE_COUNTRY
    )
    await conn.execute(
        query=queries.POPULATE_CATEGORY
    )
    await conn.execute(
        query=queries.POPULATE_WEBSITE
    )


async def get_category_popularity(conn: Database) -> list[models.CategoryPopularity]:
    data = await conn.fetch_all(
        query=queries.CATEGORY_TYPE_POPULARITY
    )
    return [models.CategoryPopularity.parse_obj(i) for i in data]


async def get_country_impact(conn: Database) -> list[models.CountryWebsiteAmount]:
    data = await conn.fetch_all(
        query=queries.COUNTRY_IMPACT
    )
    return [models.CountryWebsiteAmount.parse_obj(i) for i in data]


async def get_country_most_popular_categories(conn: Database) -> list[models.CountryMostPopularCategory]:
    data = await conn.fetch_all(
        query=queries.COUNTRY_MOST_POPULAR_CATEGORY
    )
    return [models.CountryMostPopularCategory.parse_obj(i) for i in data]


async def print_data(conn: Database) -> None:
    category_popularity = await get_category_popularity(conn=conn)
    for i in category_popularity:
        print(f"\nPrinting entity:{i.__class__.__name__}")
        print(f"{i}\n")
    country_impact = await get_country_impact(conn=conn)
    for i in country_impact:
        print(f"\nPrinting entity:{i.__class__.__name__}")
        print(f"{i}\n")
    most_popular_categories = await get_country_most_popular_categories(conn=conn)
    for i in most_popular_categories:
        print(f"\nPrinting entity:{i.__class__.__name__}")
        print(f"{i}\n")


async def main() -> None:
    conn = await postgres_connection()
    await create_tables(conn=conn)
    await populate_tables(conn=conn)
    await print_data(conn=conn)


def run_main() -> None:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    run(main=main())


if __name__ == "__main__":
    run_main()
