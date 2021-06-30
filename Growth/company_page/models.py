from django.db import models

# Create your models here.
class Company(models.Model):

    text_file = open("static/industries.txt", "r")
    list_of_industries = [(industry.strip('\n'),industry.strip('\n')) for industry in text_file.readlines()]

    #print(list_of_industries)

    list_of_sizes = [
        ("0-3","0-3 employees"),
        ("4-6" ,"4-6 employees"),
        ("6-10","6-10 employees"),
        ("10-20","10-20 employees"),
        ("20+","20+ employees")
    ]

    list_of_types = [
        ('a', "Self-employed"),
        ('b', "Public company"),
        ('c', "Government agency"),
        ('d', "Nonprofit"),
        ('e', "Sole proprietorship"),
        ('f', "Privately-held"),
        ('g', "Partnership"),
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

    type = models.CharField(
        choices=list_of_types,
        max_length=20,
        default="a"
    )

    location = models.CharField(
        max_length=100,
        null = True,
        blank=True
    )

    website_url = models.URLField(
        max_length=200,
        blank=True,
        null=True ,
    )

    logo = models.ImageField(
        default="img/default_company_logo.png",
        upload_to='img',
        blank = True,
        null = True
    )

    verify = models.BooleanField(
        default=False,
        help_text = "I verify that I am an authorized representative of this organization "
                    "and have the right to act on its behalf in the creation and management of this page. "
        #TODO: Make it a widget

    )


    #how it will be printed out
    def __str__(self):
        return self.name