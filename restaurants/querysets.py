from django.db import models


class RestaurantQuerySet(models.QuerySet):

    def random(self):
        """Returns a randomly selected Restaurant object.

        WARNING: This will be inefficient on anything but small datasets.

        Raises a DoesNotExist error when there are no available models.
        """
        try:
            return self.order_by('?')[0]
        except IndexError:
            raise self.model.DoesNotExist

