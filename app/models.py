from sqlalchemy import Column, Integer, String, Numeric, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CloudCost(Base):
    __tablename__ = "cloud_costs"

    id = Column(Integer, primary_key=True)
    cloud_provider = Column(String)
    account_name = Column(String)
    service = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    cost_amount = Column(Numeric)

    __table_args__ = (
        UniqueConstraint(
            "cloud_provider",
            "account_name",
            "service",
            "year",
            "month",
            name="unique_cost_record"
        ),
    )


class Savings(Base):
    __tablename__ = "savings"

    id = Column(Integer, primary_key=True)
    cloud_provider = Column(String)
    account_name = Column(String)
    period_type = Column(String)  # weekly / monthly / yearly
    period_value = Column(String)
    projected_cost = Column(Numeric)
    actual_cost = Column(Numeric)
    savings = Column(Numeric)
