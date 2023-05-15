import redis
from django.conf import settings
from .models import Product

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender(object):

    def get_product_key(self, id):
        return f"product:{id}:purchased_with"

    def products_bought(self, products):
        product_ids = [p.id for p in products]

        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(self.get_product_key(product_id),
                              1, with_id)

    def suggest_products_for(self, products, max_result=6):
        product_ids = [p.id for p in products]

        if len(products) == 1:
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0, -1, desc=True)[:max_result]

        else:
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)

            keys = [self.get_product_key(id) for id in product_ids]

            r.zunionstore(tmp_key, keys)

            r.zrem(tmp_key, *product_ids)
            # GET filtered products.
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_result]
            r.delete(tmp_key)

        suggested_products_ids = [int(id) for id in suggestions]
        # Get recomenderd products and sort it.
        suggested_products = list(Product.objects.filter \
                                      (id__in=suggested_products_ids))

        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id))

        return suggested_products

    def clear_purchases(self):

        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))