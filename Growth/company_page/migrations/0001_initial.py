# Generated by Django 3.2.5 on 2021-07-03 03:41

import company_page.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('industry', models.CharField(choices=[('Accounting', 'Accounting'), ('Airlines/Aviation', 'Airlines/Aviation'), ('Alternative Dispute Resolution', 'Alternative Dispute Resolution'), ('Alternative Medicine', 'Alternative Medicine'), ('Animation', 'Animation'), ('Apparel & Fashion', 'Apparel & Fashion'), ('Architecture & Planning', 'Architecture & Planning'), ('Arts & Crafts', 'Arts & Crafts'), ('Automotive', 'Automotive'), ('Aviation & Aerospace', 'Aviation & Aerospace'), ('Banking', 'Banking'), ('Biotechnology', 'Biotechnology'), ('Broadcast Media', 'Broadcast Media'), ('Building Materials', 'Building Materials'), ('Business Supplies & Equipment', 'Business Supplies & Equipment'), ('Capital Markets', 'Capital Markets'), ('Chemicals', 'Chemicals'), ('Civic & Social Organization', 'Civic & Social Organization'), ('Civil Engineering', 'Civil Engineering'), ('Commercial Real Estate', 'Commercial Real Estate'), ('Computer & Network Security', 'Computer & Network Security'), ('Computer Games', 'Computer Games'), ('Computer Hardware', 'Computer Hardware'), ('Computer Networking', 'Computer Networking'), ('Computer Software', 'Computer Software'), ('Construction', 'Construction'), ('Consumer Electronics', 'Consumer Electronics'), ('Consumer Goods', 'Consumer Goods'), ('Consumer Services', 'Consumer Services'), ('Cosmetics', 'Cosmetics'), ('Dairy', 'Dairy'), ('Defense & Space', 'Defense & Space'), ('Design', 'Design'), ('Education Management', 'Education Management'), ('E-learning', 'E-learning'), ('Electrical & Electronic Manufacturing', 'Electrical & Electronic Manufacturing'), ('Entertainment', 'Entertainment'), ('Environmental Services', 'Environmental Services'), ('Events Services', 'Events Services'), ('Executive Office', 'Executive Office'), ('Facilities Services', 'Facilities Services'), ('Farming', 'Farming'), ('Financial Services', 'Financial Services'), ('Fine Art', 'Fine Art'), ('Fishery', 'Fishery'), ('Food & Beverages', 'Food & Beverages'), ('Food Production', 'Food Production'), ('Fundraising', 'Fundraising'), ('Furniture', 'Furniture'), ('Gambling & Casinos', 'Gambling & Casinos'), ('Glass, Ceramics & Concrete', 'Glass, Ceramics & Concrete'), ('Government Administration', 'Government Administration'), ('Government Relations', 'Government Relations'), ('Graphic Design', 'Graphic Design'), ('Health, Wellness & Fitness', 'Health, Wellness & Fitness'), ('Higher Education', 'Higher Education'), ('Hospital & Health Care', 'Hospital & Health Care'), ('Hospitality', 'Hospitality'), ('Human Resources', 'Human Resources'), ('Import & Export', 'Import & Export'), ('Individual & Family Services', 'Individual & Family Services'), ('Industrial Automation', 'Industrial Automation'), ('Information Services', 'Information Services'), ('Information Technology & Services', 'Information Technology & Services'), ('Insurance', 'Insurance'), ('International Affairs', 'International Affairs'), ('International Trade & Development', 'International Trade & Development'), ('Internet', 'Internet'), ('Investment Banking/Venture', 'Investment Banking/Venture'), ('Investment Management', 'Investment Management'), ('Judiciary', 'Judiciary'), ('Law Enforcement', 'Law Enforcement'), ('Law Practice', 'Law Practice'), ('Legal Services', 'Legal Services'), ('Legislative Office', 'Legislative Office'), ('Leisure & Travel', 'Leisure & Travel'), ('Libraries', 'Libraries'), ('Logistics & Supply Chain', 'Logistics & Supply Chain'), ('Luxury Goods & Jewelry', 'Luxury Goods & Jewelry'), ('Machinery', 'Machinery'), ('Management Consulting', 'Management Consulting'), ('Maritime', 'Maritime'), ('Marketing & Advertising', 'Marketing & Advertising'), ('Market Research', 'Market Research'), ('Mechanical or Industrial Engineering', 'Mechanical or Industrial Engineering'), ('Media Production', 'Media Production'), ('Medical Device', 'Medical Device'), ('Medical Practice', 'Medical Practice'), ('Mental Health Care', 'Mental Health Care'), ('Military', 'Military'), ('Mining & Metals', 'Mining & Metals'), ('Motion Pictures & Film', 'Motion Pictures & Film'), ('Museums & Institutions', 'Museums & Institutions'), ('Music', 'Music'), ('Nanotechnology', 'Nanotechnology'), ('Newspapers', 'Newspapers'), ('Nonprofit Organization Management', 'Nonprofit Organization Management'), ('Oil & Energy', 'Oil & Energy'), ('Online Publishing', 'Online Publishing'), ('Outsourcing/Offshoring', 'Outsourcing/Offshoring'), ('Package/Freight Delivery', 'Package/Freight Delivery'), ('Packaging & Containers', 'Packaging & Containers'), ('Paper & Forest Products', 'Paper & Forest Products'), ('Performing Arts', 'Performing Arts'), ('Pharmaceuticals', 'Pharmaceuticals'), ('Philanthropy', 'Philanthropy'), ('Photography', 'Photography'), ('Plastics', 'Plastics'), ('Political Organization', 'Political Organization'), ('Primary/Secondary', 'Primary/Secondary'), ('Printing', 'Printing'), ('Professional Training', 'Professional Training'), ('Program Development', 'Program Development'), ('Public Policy', 'Public Policy'), ('Public Relations', 'Public Relations'), ('Public Safety', 'Public Safety'), ('Publishing', 'Publishing'), ('Railroad Manufacture', 'Railroad Manufacture'), ('Ranching', 'Ranching'), ('Real Estate', 'Real Estate'), ('Recreational', 'Recreational'), ('Facilities & Services', 'Facilities & Services'), ('Religious Institutions', 'Religious Institutions'), ('Renewables & Environment', 'Renewables & Environment'), ('Research', 'Research'), ('Restaurants', 'Restaurants'), ('Retail', 'Retail'), ('Security & Investigations', 'Security & Investigations'), ('Semiconductors', 'Semiconductors'), ('Shipbuilding', 'Shipbuilding'), ('Sporting Goods', 'Sporting Goods'), ('Sports', 'Sports'), ('Staffing & Recruiting', 'Staffing & Recruiting'), ('Supermarkets', 'Supermarkets'), ('Telecommunications', 'Telecommunications'), ('Textiles', 'Textiles'), ('Think Tanks', 'Think Tanks'), ('Tobacco', 'Tobacco'), ('Translation & Localization', 'Translation & Localization'), ('Transportation/Trucking/Railroad', 'Transportation/Trucking/Railroad'), ('Utilities', 'Utilities'), ('Venture Capital', 'Venture Capital'), ('Veterinary', 'Veterinary'), ('Warehousing', 'Warehousing'), ('Wholesale', 'Wholesale'), ('Wine & Spirits', 'Wine & Spirits'), ('Wireless', 'Wireless'), ('Writing & Editing', 'Writing & Editing')], max_length=1000)),
                ('size', models.CharField(choices=[('0-3', '0-3 employees'), ('4-6', '4-6 employees'), ('6-10', '6-10 employees'), ('10-20', '10-20 employees'), ('20+', '20+ employees')], default='0-3', max_length=20)),
                ('type', models.CharField(choices=[('a', 'Self-employed'), ('b', 'Public company'), ('c', 'Government agency'), ('d', 'Nonprofit'), ('e', 'Sole proprietorship'), ('f', 'Privately-held'), ('g', 'Partnership')], default='a', max_length=20)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('website_url', models.URLField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, default='logo/default_company_logo.png', null=True, upload_to='logo')),
                ('verify', models.BooleanField(default=False, help_text='I verify that I am an authorized representative of this organization and have the right to act on its behalf in the creation and management of this page. ')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=company_page.models.get_photos_upload_path)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('verify', models.BooleanField(default=False, help_text='I understand all information uploaded will be made public to the platform users. ')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company_page.company')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('tag', models.CharField(blank=True, choices=[('pitch_decks', 'Pitch Decks'), ('financial_decks', 'Financial Decks'), ('MC', 'MC'), ('founding_team', 'Founding Team'), ('other', 'other')], max_length=100, null=True)),
                ('file', models.FileField(upload_to=company_page.models.get_upload_path)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('verify', models.BooleanField(default=False, help_text='I understand all information uploaded will be made public to the platform users. ')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company_page.company')),
            ],
        ),
    ]
