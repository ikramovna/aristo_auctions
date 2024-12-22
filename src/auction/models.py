from ckeditor.fields import RichTextField
from django.db.models import *
from django.utils.timezone import now

from src.users.models import User


class Contact(Model):
    name = CharField(max_length=255)
    email = EmailField()
    message = TextField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class AuctionFavorite(Model):
    auction = ForeignKey('Auction', on_delete=CASCADE, related_name='favorites')
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='auction_favorites')
    liked = BooleanField(default=False)

    class Meta:
        verbose_name = 'Auction Favorite'
        verbose_name_plural = 'Auction Favorites'
        db_table = 'auction_favorite'
        unique_together = ('auction', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.auction.name}'


class Faq(Model):
    question = CharField(max_length=255)
    answer = TextField()

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        db_table = "faq"

    def __str__(self):
        return self.question


class AboutImage(Model):
    image = ImageField(upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name = "About Us Image"
        verbose_name_plural = "About Us Images"
        db_table = "about_image"


class About(Model):
    title = CharField(max_length=255)
    description = RichTextField()
    image = ManyToManyField(AboutImage, blank=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"
        db_table = "about_us"

    def __str__(self):
        return self.title


class Region(Model):
    name = CharField(max_length=255)

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        db_table = "region"

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('Region', CASCADE, related_name='district')

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        db_table = "district"

    def __str__(self):
        return self.name


class Mahalla(Model):
    name = CharField(max_length=255)
    district = ForeignKey('District', CASCADE, related_name='mahalla')

    class Meta:
        verbose_name = "Neighborhood"
        verbose_name_plural = "Neighborhoods"
        db_table = "mahalla"

    def __str__(self):
        return self.name


class Address(Model):
    region = ForeignKey('Region', CASCADE, related_name='address')
    district = ForeignKey('District', CASCADE, related_name='address')
    mahalla = ForeignKey('Mahalla', CASCADE, related_name='address')
    house = CharField(max_length=255)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        db_table = "address"

    def __str__(self):
        return f"{self.region} {self.district} {self.mahalla} {self.house}"


class Category(Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='category/', null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'category'

    def __str__(self):
        return self.name


class Auction(Model):
    class PeriodChoices(TextChoices):
        MORNING = 'morning', 'Morning'
        AFTERNOON = 'afternoon', 'Afternoon'
        EVENING = 'evening', 'Evening'

    class StatusChoices(TextChoices):
        UPCOMING = 'upcoming', 'Upcoming'
        LIVE = 'live', 'Live'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    name = CharField(max_length=255)
    location = CharField(max_length=255)
    lot_ref_num = CharField(max_length=8)
    lot_num_two = CharField(max_length=2)
    piece_title = CharField(max_length=255)
    price = IntegerField()
    current_bid = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dimensions = CharField(max_length=255, blank=True, null=True)
    framed_text = TextField(blank=True, null=True)
    description = TextField(blank=True, null=True)
    auction_start_date = DateTimeField()
    auction_end_date = DateTimeField()
    auction_period = CharField(max_length=10, choices=PeriodChoices.choices, default=PeriodChoices.AFTERNOON)
    status = CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.UPCOMING)
    artist_name = CharField(max_length=255, blank=True, null=True)
    artist_birth_date = DateField(blank=True, null=True)
    artist_death_date = DateField(blank=True, null=True)
    artist_address = TextField(blank=True, null=True)
    artist_image = ImageField(upload_to='artist_image/', blank=True, null=True)
    artist_bio = TextField(blank=True, null=True)
    date_prod = DateField(blank=True, null=True)
    image1 = ImageField(upload_to='auction_images/', blank=True, null=True)
    image2 = ImageField(upload_to='auction_images/', blank=True, null=True)
    image3 = ImageField(upload_to='auction_images/', blank=True, null=True)
    image4 = ImageField(upload_to='auction_images/', blank=True, null=True)
    video = ImageField(upload_to='auction_videos/', blank=True, null=True)

    category_id = ForeignKey('Category', CASCADE, related_name='category')
    owner = ForeignKey('users.User', CASCADE, related_name='auctions')

    body_style = CharField(max_length=255, blank=True, null=True)  # Example: Painting, Sculpture
    medium = CharField(max_length=255, blank=True, null=True)  # Example: Oil on Canvas, Watercolor
    color_scheme = CharField(max_length=255, blank=True, null=True)  # Example: Agate Grey
    condition = CharField(max_length=255, blank=True, null=True)  # Example: Brand New, Restored
    warranty = CharField(max_length=255, blank=True, null=True)  # Example: 3 Years Limited
    view = IntegerField(default=0)

    def update_status(self):

        current_time = now()
        if self.auction_end_date < current_time:
            self.status = self.StatusChoices.COMPLETED
        elif self.auction_start_date <= current_time <= self.auction_end_date:
            self.status = self.StatusChoices.LIVE
        elif current_time < self.auction_start_date:
            self.status = self.StatusChoices.UPCOMING
        else:
            self.status = self.StatusChoices.CANCELLED
        self.save()

    def get_remaining_time(self):
        """
        Calculate the remaining time for the auction.
        Returns the remaining time as a dictionary with days, hours, minutes, and seconds.
        """
        remaining_time = self.auction_end_date - now()
        if remaining_time.total_seconds() > 0:
            days = remaining_time.days
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return {
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds,
            }
        return {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}


def __str__(self):
    return self.name


class Bid(Model):
    auction = ForeignKey(Auction, on_delete=CASCADE, related_name='bids')
    user = ForeignKey(User, on_delete=CASCADE, related_name='bids')
    bid_amount = DecimalField(max_digits=10, decimal_places=2)
    bid_time = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bid_amount}"
