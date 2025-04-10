import pandas as pd

def get_merchant_insights(merchant_id, data):
    df = data[data['merchant_id'] == merchant_id]

    total_orders = df['order_id'].nunique()
    total_sales = df['order_value'].sum()
    avg_order_value = df['order_value'].mean()
    top_items = (
        df.groupby('item_name')['order_id'].count()
        .sort_values(ascending=False)
        .head(3)
    )

    alerts = []
    if avg_order_value < 15:
        alerts.append("Your average order value is below RM15. Consider offering bundles or set meals.")
    if total_orders < 30:
        alerts.append("Low order count this month. Boost visibility with promotions.")

    return {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "avg_order_value": avg_order_value,
        "top_items": top_items.to_dict(),
        "alerts": alerts
    }
