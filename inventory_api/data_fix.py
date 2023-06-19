from django.contrib.postgres.search import SearchVector

from inventory_api.models import Product

products = Product.objects.all()
for p in products:
    p.search_vector = (
            SearchVector(p.name, weight='A')
            + SearchVector(p.alternative_names, weight='B')
            + SearchVector(p.code, weight='A')
        # + SearchVector(p.category.name, weight='C')
        # + SearchVector(p.sub_category.name, weight='D')
    )
    p.save()
    print('Updated---------'+p.name)