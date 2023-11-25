import json
import markdown
from urllib.parse import urlparse


from . import repos
from .common import get_file_name

from .repos import read_config_file
from .markdown_extension import CodeDivExtension
from .quill_delta import convert_html_to_delta

from docsapp.models import Project, Documentation, DocPage, LANG


def sidebar_generator():
    pass


def generate_docs(user, project_id):

    error = []

    try:
        project = Project.objects.get(id=project_id)
        owner, repo = str(urlparse(project.source).path).split('/')[1:]
        path = project.doc_path

    except Project.DoesNotExist:
        error.append("Project does not exists")
        return error

    config = read_config_file(user, owner, repo)

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
        
        doc = Documentation.objects.create(project=project, version=config.get("version"))

    print("Config", config)

    for x in config.get("sidebar") or []:

        path = path or x.get("path")

        if not path:
            # error.append("sidebar path missing")
            return "sidebar path missing"

        name = x.get("name") or get_file_name(path)
        url = x.get("url") or path

        print("path: ", path)
        file_content = repos.get_file(user, owner, repo, path)

        if isinstance(file_content, dict):
            return file_content.get("error")

        print("file content: ", file_content)

        html_content =  markdown.markdown(file_content, extensions=[
                                                                    CodeDivExtension(),
                                                                    'markdown.extensions.toc',
                                                                    'markdown.extensions.tables', 
                                                                    'markdown.extensions.meta'])
        print("content: ", convert_html_to_delta(html_content), html_content)

        content = json.dumps({'delta': json.dumps(convert_html_to_delta(html_content)), 'html': html_content})

        DocPage.objects.update_or_create(documentation=doc, page_url=url, 
                                            defaults={'page_url': url, 'name': name, 'body': content})


    return True