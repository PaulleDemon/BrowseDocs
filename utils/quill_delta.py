from bs4 import BeautifulSoup, NavigableString

def convert_html_to_delta(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    delta = {"ops": []}
    for element in soup.descendants:

        if isinstance(element, NavigableString):
            if element.string:
                ops = {"insert": element.string, "attributes": get_style_attributes(element)}
                ops.update(get_class_and_id_attributes(element))
                delta["ops"].append(ops)
        
        elif element.name in ("p", "h1", "h2", "h3", "h4", "h5", "h6"):
            convert_paragraph(element, delta["ops"])
        
        elif element.name == "br":
            delta["ops"].append({"insert": "\n"})
        
        elif element.name == "img":
            src = element["src"]
            alt = element.get("alt", "")
            delta["ops"].append({"insert": {"image": src}, "attributes": {"alt": alt}})
        
        elif element.name == "a":
            href = element.get("href", "")
            convert_link(element, delta["ops"], href)
        
        elif element.name == "span":
            convert_span(element, delta["ops"])
        
        elif element.name in ("strong", "b"):
            convert_bold(element, delta["ops"])
        
        elif element.name in ("em", "i"):
            convert_italic(element, delta["ops"])
    return delta

def convert_paragraph(element, ops):
    text = element.text
    if element.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        ops.append({"insert": text})
        ops.append({"attributes": {"header": int(element.name[1])}, "insert": "\n"})
    else:
        for child in element.children:
            if child.name == "b":
                text = text.replace(child.text, "**%s**" % child.text)
            elif child.name == "i":
                text = text.replace(child.text, "*%s*" % child.text)
        ops.append({"insert": text, "attributes": get_attributes(element)})

def convert_link(element, ops, href):
    text = element.text
    ops.append({"insert": text, "attributes": {"link": href}})
    ops[-1].update(get_class_and_id_attributes(element))

def convert_span(element, ops):
    text = element.text
    ops.append({"insert": text, "attributes": get_style_attributes(element)})
    ops[-1].update(get_class_and_id_attributes(element))

def convert_bold(element, ops):
    text = element.text
    ops.append({"insert": text, "attributes": {"bold": True}})
    ops[-1].update(get_class_and_id_attributes(element))

def convert_italic(element, ops):
    text = element.text
    ops.append({"insert": text, "attributes": {"italic": True}})
    ops[-1].update(get_class_and_id_attributes(element))

def get_attributes(element):
    attributes = get_style_attributes(element)
    attributes.update(get_class_and_id_attributes(element))
    return attributes

def get_style_attributes(element):
    attributes = {}
    if hasattr(element, "attrs"):
        if "class" in element.attrs:
            attributes["class"] = " ".join(element["class"])
        
        if "id" in element.attrs:
            attributes["id"] = element["id"]

        if "style" in element.attrs:
            styles = [s.strip() for s in element["style"].split(";")]
            style_dict = {s.split(":")[0]: s.split(":")[1] for s in styles if ":" in s}
            attributes.update(style_dict)

    return attributes



def get_class_and_id_attributes(element):
    attributes = {}
    if hasattr(element, "attrs"):
        if "class" in element.attrs:
            attributes["class"] = " ".join(element["class"])
        if "id" in element.attrs:
            attributes["id"] = element["id"]
    return attributes

# html_string = '''
# <p class="paragraph" id="p1">This is a paragraph with class and id.</p>
# <p style="background: #121212; color: #eeeeee;" class="paragraph" id="p2">64&nbsp;Possibly a newbie question, so please bear with me.</p>
# <span style="font-size: 18px;" class="styled-text" id="span1">This is a span with a class and id.</span>
# <h1 id="header1">This is a header with an id.</h1>
# <a href="https://google.com">hello world</a>
# <i>world is not ending</i>
# <img src="image.png" alt="Image description" class="image" id="img1">
# '''
# delta = convert_html_to_delta(html_string)
# print(delta)
