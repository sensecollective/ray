from alabama.connection import transaction
from alabama.models import BaseModel, StringProperty
from alabama import storage
from onhands.model import Model


class AlabamaModel(BaseModel, Model):

    # FIXME
    uuid = StringProperty()

    @transaction
    def __put(self, *args, **kwargs):
        return storage.put(self, *args, **kwargs)

    @transaction
    def __delete(self, *args, **kwargs):
        return storage.delete(self, uuid=self.uuid, *args, **kwargs)

    def put(self, *args, **kwargs):
        can_save = super(AlabamaModel, self).put()
        if can_save:
            return self.__put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        can_delete = super(AlabamaModel, self).delete()
        if can_delete:
            deleted = self.__delete(*args, **kwargs)
            if deleted:
                return self

    @transaction
    def get(self, model_id, *args, **kwargs):
        return storage.get(self.__class__, uuid=model_id, *args, **kwargs)

    @transaction
    def find(self, *args, **kwargs):
        return storage.find(self.__class__, *args, **kwargs)