from pydantic import BaseModel


class CategoryPopularity(BaseModel):
    count: int
    category_type: str


class CountryWebsiteAmount(BaseModel):
    count: int
    country_name: str


class CountryMostPopularCategory(BaseModel):
    category_count: int
    country_name: str
    category_type: str
