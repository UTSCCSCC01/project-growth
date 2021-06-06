from django.db import models
from PIL import Image

# Create your models here.
class Company(models.Model):

    text_file = open("company_page/industries.txt", "r")
    list_of_industries = [(industry.strip('\n'),industry.strip('\n')) for industry in text_file.readlines()]

    #print(list_of_industries)

    list_of_sizes = [
        ("0-3","0-3"),
        ("4-6","4-6"),
        ("6-10","6-10"),
        ("10-20","10-20"),
        ("20+","20+")
    ]

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(blank=True, null=True)
    industry = models.CharField(
        choices=list_of_industries,
        max_length=1000
    )

    size = models.CharField(
        choices=list_of_sizes,
        max_length=20,
        default="0-3"
    )
    location = models.CharField(
        max_length=100,
        default="Toronto")

    website_url = models.URLField(max_length=200, blank=True, null=True)

    logo = models.ImageField(
        default="default_company_logo.png",
        blank = True,
        null = True
    )
    #TODO: Add founders field founders = models.TextField()


