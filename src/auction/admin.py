from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from src.auction.models import *


# @admin.register(Region)
# class RegionModelAdmin(ImportExportModelAdmin):
#     list_display = ("id", "name")
#     filter = ("name",)
#     ordering = ("id",)
#
#
# @admin.register(District)
# class DistrictModelAdmin(ImportExportModelAdmin):
#     list_display = ("id", "name", "region")
#     ordering = ("id",)
#
#
# @admin.register(Mahalla)
# class MahallaModelAdmin(ImportExportModelAdmin):
#     list_display = ("id", "name", "district")
#     ordering = ("id",)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ("id", "name")
    ordering = ("id",)
    search_fields = ("name",)


@admin.register(Auction)
class AuctionAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "category_id",
        "owner",
        "status",
        "auction_start_date",
        "auction_end_date",
        "price",
        "view",
    )
    list_filter = (
        "status",
        "auction_period",
        "category_id__name",
        "artist_name",
        "auction_start_date",
        "auction_end_date",
    )
    ordering = ("-auction_start_date", "name", "price")
    search_fields = ("name", "owner__username", "category_id__name", "artist_name", "description")
    date_hierarchy = "auction_start_date"
    list_editable = ("status", "price")
    readonly_fields = ("view",)
    actions = ["mark_as_completed", "mark_as_pending"]

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected auctions as completed"

    def mark_as_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_as_pending.short_description = "Mark selected auctions as pending"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(view_count=Count('view'))

    def view_count(self, obj):
        return obj.view_count
    view_count.admin_order_field = 'view_count'
    view_count.short_description = 'View Count'

from django.db.models import Count

@admin.register(Bid)
class BidAdmin(ImportExportModelAdmin):
    list_display = ("id", "auction", "user_full_name", "bid_amount", "bid_time")
    list_filter = ("auction__name", "user__full_name", "bid_time", "bid_amount")
    ordering = ("-bid_time", "bid_amount")
    search_fields = ("auction__name", "user__full_name", "bid_amount")
    date_hierarchy = "bid_time"
    list_editable = ("bid_amount",)
    readonly_fields = ("id",)
    actions = ["mark_as_highlighted", "mark_as_regular"]

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.admin_order_field = 'user__full_name'
    user_full_name.short_description = 'User Full Name'

    def mark_as_highlighted(self, request, queryset):
        queryset.update(highlighted=True)
    mark_as_highlighted.short_description = "Mark selected bids as highlighted"

    def mark_as_regular(self, request, queryset):
        queryset.update(highlighted=False)
    mark_as_regular.short_description = "Mark selected bids as regular"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(bid_count=Count('bid_amount'))

    def bid_count(self, obj):
        return obj.bid_count
    bid_count.admin_order_field = 'bid_count'
    bid_count.short_description = 'Bid Count'


@admin.register(Faq)
class FaqModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "question", "answer")
    ordering = ("id",)


@admin.register(About)
class AboutModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "title", "description")
    ordering = ("id",)


@admin.register(AboutImage)
class AboutImageModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "image")
    ordering = ("id",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')  #
    search_fields = ('name', 'email')
    ordering = ('-created_at',)

@admin.register(AuctionFavorite)
class AuctionFavoriteAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'created_at')
    search_fields = ('auction__name', 'user__full_name')
    ordering = ('-created_at',)
