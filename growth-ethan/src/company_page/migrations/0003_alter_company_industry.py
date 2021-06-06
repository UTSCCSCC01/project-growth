# Generated by Django 3.2.4 on 2021-06-05 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_page', '0002_auto_20210605_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=models.CharField(choices=[('Accounting\n', 'Accounting\n'), ('Airlines/Aviation\n', 'Airlines/Aviation\n'), ('Alternative Dispute Resolution\n', 'Alternative Dispute Resolution\n'), ('Alternative Medicine\n', 'Alternative Medicine\n'), ('Animation\n', 'Animation\n'), ('Apparel & Fashion\n', 'Apparel & Fashion\n'), ('Architecture & Planning\n', 'Architecture & Planning\n'), ('Arts & Crafts\n', 'Arts & Crafts\n'), ('Automotive\n', 'Automotive\n'), ('Aviation & Aerospace\n', 'Aviation & Aerospace\n'), ('Banking\n', 'Banking\n'), ('Biotechnology\n', 'Biotechnology\n'), ('Broadcast Media\n', 'Broadcast Media\n'), ('Building Materials\n', 'Building Materials\n'), ('Business Supplies & Equipment\n', 'Business Supplies & Equipment\n'), ('Capital Markets\n', 'Capital Markets\n'), ('Chemicals\n', 'Chemicals\n'), ('Civic & Social Organization\n', 'Civic & Social Organization\n'), ('Civil Engineering\n', 'Civil Engineering\n'), ('Commercial Real Estate\n', 'Commercial Real Estate\n'), ('Computer & Network Security\n', 'Computer & Network Security\n'), ('Computer Games\n', 'Computer Games\n'), ('Computer Hardware\n', 'Computer Hardware\n'), ('Computer Networking\n', 'Computer Networking\n'), ('Computer Software\n', 'Computer Software\n'), ('Construction\n', 'Construction\n'), ('Consumer Electronics\n', 'Consumer Electronics\n'), ('Consumer Goods\n', 'Consumer Goods\n'), ('Consumer Services\n', 'Consumer Services\n'), ('Cosmetics\n', 'Cosmetics\n'), ('Dairy\n', 'Dairy\n'), ('Defense & Space\n', 'Defense & Space\n'), ('Design\n', 'Design\n'), ('Education Management\n', 'Education Management\n'), ('E-learning\n', 'E-learning\n'), ('Electrical & Electronic Manufacturing\n', 'Electrical & Electronic Manufacturing\n'), ('Entertainment\n', 'Entertainment\n'), ('Environmental Services\n', 'Environmental Services\n'), ('Events Services\n', 'Events Services\n'), ('Executive Office\n', 'Executive Office\n'), ('Facilities Services\n', 'Facilities Services\n'), ('Farming\n', 'Farming\n'), ('Financial Services\n', 'Financial Services\n'), ('Fine Art\n', 'Fine Art\n'), ('Fishery\n', 'Fishery\n'), ('Food & Beverages\n', 'Food & Beverages\n'), ('Food Production\n', 'Food Production\n'), ('Fundraising\n', 'Fundraising\n'), ('Furniture\n', 'Furniture\n'), ('Gambling & Casinos\n', 'Gambling & Casinos\n'), ('Glass, Ceramics & Concrete\n', 'Glass, Ceramics & Concrete\n'), ('Government Administration\n', 'Government Administration\n'), ('Government Relations\n', 'Government Relations\n'), ('Graphic Design\n', 'Graphic Design\n'), ('Health, Wellness & Fitness\n', 'Health, Wellness & Fitness\n'), ('Higher Education\n', 'Higher Education\n'), ('Hospital & Health Care\n', 'Hospital & Health Care\n'), ('Hospitality\n', 'Hospitality\n'), ('Human Resources\n', 'Human Resources\n'), ('Import & Export\n', 'Import & Export\n'), ('Individual & Family Services\n', 'Individual & Family Services\n'), ('Industrial Automation\n', 'Industrial Automation\n'), ('Information Services\n', 'Information Services\n'), ('Information Technology & Services\n', 'Information Technology & Services\n'), ('Insurance\n', 'Insurance\n'), ('International Affairs\n', 'International Affairs\n'), ('International Trade & Development\n', 'International Trade & Development\n'), ('Internet\n', 'Internet\n'), ('Investment Banking/Venture\n', 'Investment Banking/Venture\n'), ('Investment Management\n', 'Investment Management\n'), ('Judiciary\n', 'Judiciary\n'), ('Law Enforcement\n', 'Law Enforcement\n'), ('Law Practice\n', 'Law Practice\n'), ('Legal Services\n', 'Legal Services\n'), ('Legislative Office\n', 'Legislative Office\n'), ('Leisure & Travel\n', 'Leisure & Travel\n'), ('Libraries\n', 'Libraries\n'), ('Logistics & Supply Chain\n', 'Logistics & Supply Chain\n'), ('Luxury Goods & Jewelry\n', 'Luxury Goods & Jewelry\n'), ('Machinery\n', 'Machinery\n'), ('Management Consulting\n', 'Management Consulting\n'), ('Maritime\n', 'Maritime\n'), ('Marketing & Advertising\n', 'Marketing & Advertising\n'), ('Market Research\n', 'Market Research\n'), ('Mechanical or Industrial Engineering\n', 'Mechanical or Industrial Engineering\n'), ('Media Production\n', 'Media Production\n'), ('Medical Device\n', 'Medical Device\n'), ('Medical Practice\n', 'Medical Practice\n'), ('Mental Health Care\n', 'Mental Health Care\n'), ('Military\n', 'Military\n'), ('Mining & Metals\n', 'Mining & Metals\n'), ('Motion Pictures & Film\n', 'Motion Pictures & Film\n'), ('Museums & Institutions\n', 'Museums & Institutions\n'), ('Music\n', 'Music\n'), ('Nanotechnology\n', 'Nanotechnology\n'), ('Newspapers\n', 'Newspapers\n'), ('Nonprofit Organization Management\n', 'Nonprofit Organization Management\n'), ('Oil & Energy\n', 'Oil & Energy\n'), ('Online Publishing\n', 'Online Publishing\n'), ('Outsourcing/Offshoring\n', 'Outsourcing/Offshoring\n'), ('Package/Freight Delivery\n', 'Package/Freight Delivery\n'), ('Packaging & Containers\n', 'Packaging & Containers\n'), ('Paper & Forest Products\n', 'Paper & Forest Products\n'), ('Performing Arts\n', 'Performing Arts\n'), ('Pharmaceuticals\n', 'Pharmaceuticals\n'), ('Philanthropy\n', 'Philanthropy\n'), ('Photography\n', 'Photography\n'), ('Plastics\n', 'Plastics\n'), ('Political Organization\n', 'Political Organization\n'), ('Primary/Secondary\n', 'Primary/Secondary\n'), ('Printing\n', 'Printing\n'), ('Professional Training\n', 'Professional Training\n'), ('Program Development\n', 'Program Development\n'), ('Public Policy\n', 'Public Policy\n'), ('Public Relations\n', 'Public Relations\n'), ('Public Safety\n', 'Public Safety\n'), ('Publishing\n', 'Publishing\n'), ('Railroad Manufacture\n', 'Railroad Manufacture\n'), ('Ranching\n', 'Ranching\n'), ('Real Estate\n', 'Real Estate\n'), ('Recreational\n', 'Recreational\n'), ('Facilities & Services\n', 'Facilities & Services\n'), ('Religious Institutions\n', 'Religious Institutions\n'), ('Renewables & Environment\n', 'Renewables & Environment\n'), ('Research\n', 'Research\n'), ('Restaurants\n', 'Restaurants\n'), ('Retail\n', 'Retail\n'), ('Security & Investigations\n', 'Security & Investigations\n'), ('Semiconductors\n', 'Semiconductors\n'), ('Shipbuilding\n', 'Shipbuilding\n'), ('Sporting Goods\n', 'Sporting Goods\n'), ('Sports\n', 'Sports\n'), ('Staffing & Recruiting\n', 'Staffing & Recruiting\n'), ('Supermarkets\n', 'Supermarkets\n'), ('Telecommunications\n', 'Telecommunications\n'), ('Textiles\n', 'Textiles\n'), ('Think Tanks\n', 'Think Tanks\n'), ('Tobacco\n', 'Tobacco\n'), ('Translation & Localization\n', 'Translation & Localization\n'), ('Transportation/Trucking/Railroad\n', 'Transportation/Trucking/Railroad\n'), ('Utilities\n', 'Utilities\n'), ('Venture Capital\n', 'Venture Capital\n'), ('Veterinary\n', 'Veterinary\n'), ('Warehousing\n', 'Warehousing\n'), ('Wholesale\n', 'Wholesale\n'), ('Wine & Spirits\n', 'Wine & Spirits\n'), ('Wireless\n', 'Wireless\n'), ('Writing & Editing', 'Writing & Editing')], max_length=100),
        ),
    ]
