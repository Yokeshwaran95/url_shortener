from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class UrlShortener(Base):
    __tablename__ = "url_shortener"
    id = Column(Integer, primary_key=True, autoincrement=True)
    original_url = Column(String)
    domain_name = Column(String)
    short_url = Column(String)

    def to_json(self):
        return {
            "id": self.id,
            "original_url": self.original_url,
            "domain_name": self.domain_name,
            "short_url": self.short_url
        }

