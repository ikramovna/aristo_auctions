from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from src.auction.models import *


@admin.register(Region)
class RegionModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name")
    filter = ("name",)
    ordering = ("id",)


@admin.register(District)
class DistrictModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "region")
    ordering = ("id",)


@admin.register(Mahalla)
class MahallaModelAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "district")
    ordering = ("id",)


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
        "category_id__name",  # Filter by category name
        "owner__username",  # Filter by owner username
    )
    ordering = ("-auction_start_date",)
    search_fields = ("name", "owner__username", "category_id__name", "artist_name")
    date_hierarchy = "auction_start_date"  # Adds a date-based navigation bar
    list_editable = ("status", "price")  # Makes these fields editable directly in the list view


@admin.register(Bid)
class BidAdmin(ImportExportModelAdmin):
    list_display = ("id", "auction", "user", "bid_amount", "timestamp")
    list_filter = ("auction__name", "user__username")
    ordering = ("-timestamp",)
    search_fields = ("auction__name", "user__username")


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
