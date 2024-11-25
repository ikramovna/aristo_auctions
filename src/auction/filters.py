import django_filters
from .models import Auction


class AuctionFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte", label="Minimum Price")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte", label="Maximum Price")
    category = django_filters.CharFilter(field_name="category_id__name", lookup_expr="icontains", label="Category Name")
    status = django_filters.ChoiceFilter(field_name="status", choices=Auction.StatusChoices.choices, label="Status")
    auction_period = django_filters.ChoiceFilter(
        field_name="auction_period",
        choices=Auction.PeriodChoices.choices,
        label="Auction Period",
    )
    start_date = django_filters.DateFilter(field_name="auction_start_date", lookup_expr="gte",
                                           label="Start Date (After)")
    end_date = django_filters.DateFilter(field_name="auction_end_date", lookup_expr="lte", label="End Date (Before)")

    class Meta:
        model = Auction
        fields = ['status', 'auction_period', 'category', 'min_price', 'max_price', 'start_date', 'end_date']
