"""Sales analytics dashboard for admin."""
from datetime import timedelta
from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, IntegerField, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce, TruncDate, TruncMonth
from django.shortcuts import render
from django.utils import timezone

from apps.catalog.models import Product, ProductVariant, Promotion
from apps.orders.models import WhatsAppOrder, WhatsAppOrderItem


def _order_revenue_subquery():
    """Subquery: sum of (qty * unit_price) of items in an order."""
    return (
        WhatsAppOrderItem.objects
        .filter(order_id=OuterRef('pk'))
        .annotate(line=F('quantity') * F('unit_price'))
        .values('order_id')
        .annotate(total=Sum('line'))
        .values('total')
    )


def _order_revenue_with_discount():
    """Revenue of an order after applying discount."""
    return F('subtotal') - F('discount_amount')


@staff_member_required
def dashboard(request):
    now = timezone.now()
    last_30 = now - timedelta(days=30)
    last_7 = now - timedelta(days=7)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    revenue_sub = _order_revenue_subquery()

    all_orders_qs = WhatsAppOrder.objects.annotate(
        revenue=Coalesce(Subquery(revenue_sub), Decimal('0'), output_field=IntegerField()),
        revenue_after_discount=F('revenue') - F('discount_amount'),
    )
    all_orders = all_orders_qs.all()
    paid_q = all_orders.exclude(status='cancelled')
    orders_30 = all_orders.filter(created_at__gte=last_30)
    orders_7 = all_orders.filter(created_at__gte=last_7)
    orders_month = all_orders.filter(created_at__gte=month_start)

    rev_total = paid_q.aggregate(s=Sum('revenue_after_discount'))['s'] or Decimal('0')
    rev_30 = orders_30.exclude(status='cancelled').aggregate(s=Sum('revenue_after_discount'))['s'] or Decimal('0')
    rev_month = orders_month.exclude(status='cancelled').aggregate(s=Sum('revenue_after_discount'))['s'] or Decimal('0')
    paid_count_30 = orders_30.exclude(status='cancelled').count()
    avg_ticket_30 = (rev_30 / paid_count_30) if paid_count_30 else Decimal('0')

    metrics = {
        'total_orders': all_orders.count(),
        'orders_30': orders_30.count(),
        'orders_7': orders_7.count(),
        'orders_month': orders_month.count(),
        'revenue_total': rev_total,
        'revenue_30': rev_30,
        'revenue_month': rev_month,
        'avg_ticket_30': avg_ticket_30,
    }

    status_counts = dict(
        all_orders.values_list('status').annotate(c=Count('id')).values_list('status', 'c')
    )
    for status_code, _ in WhatsAppOrder.STATUS_CHOICES:
        metrics[f'status_{status_code}'] = status_counts.get(status_code, 0)

    top_products = list(
        WhatsAppOrderItem.objects
        .filter(order__created_at__gte=last_30)
        .values('product_name_snapshot')
        .annotate(
            qty=Sum('quantity'),
            revenue=Sum(F('quantity') * F('unit_price')),
        )
        .order_by('-qty')[:10]
    )

    sales_by_day_qs = (
        paid_q.filter(created_at__gte=last_30)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('revenue_after_discount'))
        .order_by('day')
    )
    sales_by_day_labels = [s['day'].strftime('%d/%m') for s in sales_by_day_qs]
    sales_by_day_values = [float(s['total'] or 0) for s in sales_by_day_qs]

    sales_by_month_qs = (
        paid_q.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('revenue_after_discount'))
        .order_by('month')
    )
    sales_by_month_labels = [s['month'].strftime('%b %Y') for s in sales_by_month_qs]
    sales_by_month_values = [float(s['total'] or 0) for s in sales_by_month_qs]

    low_stock = ProductVariant.objects.filter(
        stock__lte=F('low_stock_threshold'),
        is_active=True,
    ).select_related('product').order_by('stock')[:20]

    low_stock_count = ProductVariant.objects.filter(
        stock__lte=F('low_stock_threshold'),
        is_active=True,
    ).count()
    out_of_stock_count = ProductVariant.objects.filter(stock=0, is_active=True).count()

    recent_orders = WhatsAppOrder.objects.all().order_by('-created_at')[:10]

    return render(request, 'admin/dashboard.html', {
        'metrics': metrics,
        'top_products': top_products,
        'sales_by_day_labels': sales_by_day_labels,
        'sales_by_day_values': sales_by_day_values,
        'sales_by_month_labels': sales_by_month_labels,
        'sales_by_month_values': sales_by_month_values,
        'low_stock': low_stock,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'recent_orders': recent_orders,
        'title': 'Dashboard',
        'page_title': 'Dashboard',
    })
