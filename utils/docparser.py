import markdown
from docutils.core import publish_parts
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

md = (
    MarkdownIt('commonmark' ,{'breaks':True,'html':True})
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .enable('table')
)

def parse_doc(text, doc_type="md"):

    if doc_type == "rst":
        html_parts = publish_parts(
                                    source=text,
                                    writer_name="html",
                                    # settings_overrides={"initial_header_level": 2}
                                )   

        return html_parts["fragment"]

    else:
        return md.render(text)


rst_content = """
    #Example Markdown to HTML Conversion

This is a paragraph in Markdown format.

- This is a list item.
- This is another list item.
| Symbol | Meaning |
| ------ | ------- |
| :fish: | fishy   |

[Link to Google](https://www.google.com)
"""
print(parse_doc(rst_content))