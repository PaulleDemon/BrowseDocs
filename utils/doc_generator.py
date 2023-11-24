import json
import markdown
from . import repos
from .common import get_file_name

from .quill_delta import convert_html_to_delta

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
        try:
            project = Project.objects.get(id=project_id)

        except Project.DoesNotExist:
            error.append("Project does not exists")
            return error
        
        doc = Documentation.objects.create(project=project, version=config.get("version"))

    print("Config", config)

    for x in config.get("sidebar") or []:

        path = x.get("path")

        if not path:
            # error.append("sidebar path missing")
            return "sidebar path missing"

        name = x.get("name") or get_file_name(path)
        url = x.get("url") or path

        file_content = repos.get_file(user, owner, repo, path)

        if isinstance(file_content, dict):
            return file_content.get("error")

        html_content =  markdown.markdown(file_content, extensions=['markdown.extensions.toc'])
        print("content: ", convert_html_to_delta(html_content))

        content = json.dumps({'delta': json.dumps(convert_html_to_delta(html_content)), 'html': html_content})

        DocPage.objects.update_or_create(documentation=doc, page_url=url, 
                                            defaults={'page_url': url, 'name': name, 'body': content})


    return True