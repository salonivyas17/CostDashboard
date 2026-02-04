from sqlalchemy.orm import Session
from app.models import CloudCost, Savings

def calculate_annual_savings(db: Session, account, provider):
    costs = (
        db.query(CloudCost)
        .filter(
            CloudCost.account_name == account,
            CloudCost.cloud_provider == provider
        )
        .order_by(CloudCost.year.desc(), CloudCost.month.desc())
        .limit(3)
        .all()
    )

    if len(costs) < 3:
        return

    avg_monthly = sum(c.cost_amount for c in costs) / 3
    projected = avg_monthly * 12

    savings = Savings(
        cloud_provider=provider,
        account_name=account,
        period_type="yearly",
        period_value="annual",
        projected_cost=projected,
        actual_cost=0,
        savings=projected
    )

    db.add(savings)
    db.commit()
