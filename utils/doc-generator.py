import markdown

from . import repos
from .common import get_file_name

from docsapp.models import Project, Documentation, DocPage, LANG


def sidebar_generator():
    pass


def generate_docs(user, owner, repo, config, project_id):

    error = []

    url_set = set()
    for item in config.get("sidebar") or []:
        if item.get("url") in url_set:
            error.append("duplicate urls found")

            return error
        
        if item.get("url"):
            url_set.add(item["url"])


    doc = Documentation.objects.filter(project=project_id, version=config.get("version"))

    if doc.exists():
        doc = doc.last()

    else:
        doc = Documentation.objects.filter(project=project_id, version=config.get("version"))

    for x in config.get("sidebar") or []:

        path = x.get("path")

        if not path:
            # error.append("sidebar path missing")
            return "sidebar path missing"

        name = x.get("name") or get_file_name(path)
        url = x.get("url") or path

        file_content = repos.get_file(user, owner, repo, )

        if isinstance(file_content, dict):
            return file_content.get("error")
      
        content = {'delta': '', 'html': markdown.markdown(file_content, extensions=['markdown.extensions.toc'])}

        DocPage.objects.update_or_create(documentation=doc, page_url=url, defaults={'page': url, 'name': name, 'body': content})


    return True