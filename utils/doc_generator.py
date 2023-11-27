import json
import markdown
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from lxml.html.clean import clean_html

from django.utils.text import slugify

from . import repos
from .common import get_file_name

from .repos import read_config_file
from .markdown_extension import CodeDivExtension
from .quill_delta import convert_html_to_delta

from docsapp.models import (Project, Documentation, DocPage, AdditionalLink,
                            Sponsor, Social, LANG, SOCIAL, SPONSORS)


def strip_path_slash(text: str):

    """ To save urls without trailing slash"""
    path = text
    if text.endswith("/"):
        path = text[:-1]

    if text.startswith("/"):
        path = path[1:]

    return path

def update_project(project_id, config):

    if not isinstance(config.get('authors') or [], list):
        return

    conf = {
        'name': config.get('project_name') or '',
        'about': config.get('about') or '',
        'version': config.get('version') or '',
        'about': config.get('about') or '',
        'doc_path': config.get('source') or '',
        'project_logo': config.get('project_logo') or '',
        'authors': config.get('authors') or []
        # 'tags': config.get
    }

    project = Project.objects.filter(id=project_id)
    project.update(**conf)

    # if project.exists():

    #     additional_links = config.get('additional_links') or {}

    #     AdditionalLink.objects.filter(project=project).delete()

    #     for link_name, link_url in additional_links.items():
    #         AdditionalLink.objects.create(project=project, url=link_url, name=link_name)


def generate_docs(user, project_id):

    error = []

    try:
        project = Project.objects.get(id=project_id)
        owner, repo = str(urlparse(project.source).path).split('/')[1:]

    except Project.DoesNotExist:
        error.append("Project does not exists")
        return error

    config = read_config_file(user, owner, repo)
    update_project(project_id, config)
    path = project.doc_path

    if path.endswith("/"):
        path = "index.md"

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
        # doc.save()

    else:
        
        doc = Documentation.objects.create(project=project, version=config.get("version"), 
                                            )

    print("Config", config)

    sidebar = []

    for x in config.get("sidebar") or [{'path': path}]:

        path = x.get("path", path)

        if not path:
            # error.append("sidebar path missing")
            return "sidebar path missing"

        if not path.endswith(".md"):
            return f"non markdown file {path}"

        name = x.get("name", get_file_name(path))
        url = x.get("url", slugify(path))
        #FIXME: problem in creating url
        url = strip_path_slash(url)
        print("url: ",  path)

        file_content = repos.get_file(user, owner, repo, path)

        if isinstance(file_content, dict):
            return file_content.get("error")

        if not file_content or len(file_content) < 50:
            return f"The document {path} is too small for document to be created. Add necessary details"

        html_content =  markdown.markdown(file_content, extensions=[
                                                                    CodeDivExtension(),
                                                                    'markdown.extensions.toc',
                                                                    'markdown.extensions.tables', 
                                                                    'markdown.extensions.meta'])

        # content = json.dumps({'delta': json.dumps(convert_html_to_delta(html_content)), 'html': html_content})
        content = json.dumps({'delta': "['ops': []]", 'html': clean_html(html_content)})

        soup = BeautifulSoup(html_content, 'html.parser')

        target = soup.find_all(['h1', 'h2'])

        sidebar.append({
            'name': name,
            'url': url,
            'path': path,
            'headings': [x.text for x in target]
        })

        DocPage.objects.update_or_create(documentation=doc, page_url=url, 
                                            defaults={'page_url': url, 'name': name, 'body': content})

    doc.sidebar = sidebar
    doc.save()

    return True