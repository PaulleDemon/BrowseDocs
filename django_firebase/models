import inspect
from typing import Any

from django.conf import settings

from google.cloud.firestore_v1 import Client
from google.cloud.firestore_v1.query import Query
from google.cloud.firestore_v1.base_query import FieldFilter

db_client: Client  = settings.FIRESTORE_CLIENT

class NoDocumentClassException(Exception):
    pass


class NoCollectionClassException(Exception):
    pass


# class Field


class AbstractCollection:

    _collection = None

    def __new__(self) -> None:
       AbstractCollection._collection =  db_client.collection(self.__name__)


    def __call__(self, *args: Any, **kwds: Any) -> Any:
        AbstractCollection.check_inner_classes()
    
    @classmethod
    def check_inner_classes(cls):
        document_class = any([cls_attribute for cls_attribute in cls.__dict__.values()
                                    if inspect.isclass(cls_attribute)
                                    and issubclass(cls_attribute, AbstractDocument)])

        if (not document_class):
            raise NoDocumentClassException

class AbstractDocument:

    _collection = None

    _document = None


    def __init__(self, outer_class: AbstractCollection) -> None:
        
        self.strict_check = True # if this is enabled the model will raise an exception if invalid field is added

        if not isinstance(outer_class._collection, AbstractCollection):
            raise NoCollectionClassException

        AbstractDocument._collection = outer_class._collection

        AbstractDocument._document =  AbstractDocument._collection.document(self.__name__)


    def save(data: dict):
        pass


    def update(data):
        pass

    def delete_collection(self, coll_ref, batch_size):

        """
            To delete an entire collection or subcollection in Cloud Firestore
        """

        docs = coll_ref.list_documents(page_size=batch_size)
        deleted = 0

        for doc in docs:
            # print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
            doc.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return self.delete_collection(coll_ref, batch_size)