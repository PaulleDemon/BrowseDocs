from django.conf import settings

from google.cloud.firestore_v1 import Client
from google.cloud.firestore_v1.query import Query
from google.cloud.firestore_v1.base_query import FieldFilter

db_client: Client  = settings.FIRESTORE_CLIENT


class AbstractModel:

    def create_or_update(data: dict, pk=None):

        pass


def create_or_update_project(data:dict, pk=None):
    """
        the project info
        {
            name: "",
            repo: "",
            author: "", // repo author
            datetime: "",
        }
    """
    collection =  db_client.collection('projects')
    
    if pk:
       return collection.document(pk).update(data)

    else:
        return collection.document().set(data)


def create_or_update_doc(data: dict, projectid=None, pk=None):

    """
        a sub collection of project
        data structure
            {
                version: 1,
                ln: en,
                document: "the actual document",
                indexes: [],
                user: 1 // commit author
            }
    """
    project = db_client.collection("projects").document(projectid)
    collection =  project.collection('docs')

    if pk:
       collection.document(pk).update(data)

    else:
        collection.document().add(data)


def get_project(projectid):
    return db_client.collection("projects").document(projectid).get()


def unqiue_project_name_exists(project_name):
    """
        checks if the project name already exists
    """
    return len(db_client.collection("projects").where(filter=FieldFilter("unqiue_name", "==", project_name.lower())).limit(1).get()) > 0


def create_or_update_blog(data: dict, pk=None):

    """
        data structure:
            {
                blog: "text",
                title: "",
                user: 1,
                draft: false,
                published: false
            }
    """
    