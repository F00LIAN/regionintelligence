from pydantic import BaseModel
from typing import Optional, List

ecommerce_schema = {
    "properties": {
        "item_title": {"type": "string"},
        "item_price": {"type": "number"},
        "item_extra_info": {"type": "string"}
    },
    "required": ["item_name", "price", "item_extra_info"],
}


class SchemaNewsWebsites(BaseModel):
    news_headline: str
    news_short_summary: str

class SchemaEcommerceWebsites(BaseModel):
    item_title: str
    item_price: float
    item_extra_info: str

class SchemaCityWebsites(BaseModel):
    commission_name: Optional[str] = None
    agenda_link: Optional[str] = None
   # meeting_date: Optional[str] = None

class CityInfo(BaseModel):
    city_name: str
    commissions: List[SchemaCityWebsites]

class PrimegovCityInfo(BaseModel):
    title: str
    date: str
    link: str
