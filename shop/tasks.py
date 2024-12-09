from celery import shared_task, group
from .models import Sale

@shared_task(name="Price update")
def update_price():
    sales = Sale.objects.filter(is_active=True)
    chunk_size = 100
    stock_chunks = [sales[i:i + chunk_size] for i in range(0, len(sales), chunk_size)]
    stock_chunks_ids = [[stock.id for stock in chunk] for chunk in stock_chunks]
    tasks = group(update_price_for_chunk.s(chunk) for chunk in stock_chunks_ids)
    tasks.apply_async()
    return "Price update tasks are processing"

@shared_task
def update_price_for_chunk(chunk_ids):
    sales = Sale.objects.filter(id__in=chunk_ids)
    for sale in sales:
        sale.update_price()
    return f"Processed {len(sales)} sales"