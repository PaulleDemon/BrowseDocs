from bs4 import BeautifulSoup, NavigableString

# FIXME: this is still work in progress, the quill editor also accepts html as input, so just stick to that

def convert_html_to_delta(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    delta = {"ops": []}
    convert_element(soup, delta["ops"])
    return delta


def has_only_text_children(element):
    return all(isinstance(child, NavigableString) for child in element.children)


def convert_element(element, ops):

    if not isinstance(element, NavigableString):
        for child in element.children:
            if not has_only_text_children(element):
                convert_element(child, ops)

    if element.name in ("p", "h1", "h2", "h3", "h4", "h5", "h6"):
        convert_paragraph(element, ops)
    
    elif element.name == "br":
        # NOTE: if there is a br tage the \n\n should be added to the previous text, but this one is hacky
        ops.append({"insert": "\n"})
    
    elif element.name == "img":
        src = element["src"]
        alt = element.get("alt", "")
        ops.append({"insert": {"image": src}, "attributes": {"alt": alt}})
    
    elif element.name == "a":
        href = element.get("href", "")
        convert_link(element, ops, href)
    
    elif element.name == "span":
        convert_span(element, ops)
    
    elif element.name in ("strong", "b"):
        convert_bold(element, ops)
    
    elif element.name in ("em", "i"):
        convert_italic(element, ops)
    
    elif element.name == "div" and "ql-code-block-container" in element.get("class", []):
        convert_code_block(element, ops)

    elif element.name == "div" and "notice-block" in element.get("class", []):
        convert_notice_block(element, ops)

    elif element.name == "code":
        convert_inline(element, ops)
    
    elif element.name == "blockquote":
        convert_blockquote(element, ops)

    elif isinstance(element, NavigableString):
        # print("String: ", element.string)
        if element.string and element.string != "\n" and element.string != '':
            ops.append({"insert": element.string, "attributes": get_style_attributes(element)})
            ops[-1].update(get_class_and_id_attributes(element))



def convert_paragraph(element, ops):
    text = ""
    for child in element.children:
        # if isinstance(child, NavigableString):
        #     if child.string:
        #         ops.append({"insert": child.string, "attributes": get_style_attributes(child)})
        #         ops[-1].update(get_class_and_id_attributes(child))
        if child.name == "b":
            text += child.text.replace(child.text, "**%s**" % child.text)
        elif child.name == "i":
            text += child.text.replace(child.text, "*%s*" % child.text)
        elif child.name == 'code':
            convert_inline(child, ops)

    if element.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        ops.append({"insert": text})
        ops.append({"attributes": {"header": int(element.name[1])}, "insert": "\n"})
    # else:
    #     ops.append({"insert": f"{text}\n", "attributes": get_attributes(element)})

def convert_code_block(element, ops):
    for code in element.find_all("div", class_="ql-code-block"):
        code_text = "\n".join(text for text in code.children)
        ops.append({"insert": code_text})
        ops.append({"attributes": {"code-block": "plain"}, "insert": "\n"})
    # code_text = element.text
    # ops.append({"insert": f"{code_text}", "attributes": {"code": True}})
    # ops.append({"attributes": {"code-block": "plain"}, "insert": "\n"})


def convert_notice_block(element, ops):
    for child in element.children:
        convert_element(child, ops)
    ops.append({"insert": "\n", "attributes": {"notice": True}})



def convert_inline(element, ops):
    code_text = element.text
    ops.append({"insert": f"{code_text}", "attributes": {"code": True}})

def convert_blockquote(element, ops):
    # for child in element.children:
    #     convert_element(child, ops)
    ops.append({"insert": "\n", "attributes": {"blockquote": True}})


def convert_link(element, ops, href):
    text = element.text
    ops.append({"insert": text, "attributes": {"link": href}})
    ops[-1].update(get_class_and_id_attributes(element))


def convert_span(element, ops):
    for child in element.children:
        convert_element(child, ops)


def convert_bold(element, ops):
    for child in element.children:
        convert_element(child, ops)
    ops[-1]["attributes"]["bold"] = True


def convert_italic(element, ops):
    for child in element.children:
        convert_element(child, ops)
    ops[-1]["attributes"]["italic"] = True


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
# <h1 id="testdocs">TestDocs</h1>
# <p>A repo for testing docs</p>
# <p align="center">
#   <img src="https://github.com/PaulleDemon/Email-automation/blob/master/logos/atmailwin-logo.svg" alt="CupidCues icon" width="200px" height="200px"/>
# </p>

# <p><img alt="another image" src="https://github.com/PaulleDemon/PaulleDemon/raw/main/images/buy-me-coffee.png?raw=true" /></p>
# <p>A free and open-source email automation tool. Schedule, personalize and send!
# <br/>
# <br/>
# Have you ever meticulously crafted a personalized email to a potential employer or business and waited eagerly for a response that never arrived? It's a common scenario, and the disappointment is palpable. Creating highly personalized emails is time-consuming and often doesn't yield the desired results. AtMailWin offers a workaround - the ability to create semi-personalized emails, schedule them send them in bulk to multiple recipients.</p>
# <p>You can use the site at <a href="https://atmailwin.com">https://atmailwin.com</a> </p>
# <h2 id="features">Features</h2>
# <ul>
# <li>Create dynamic email templates.</li>
# <li>Use variables, if statements in your email template.</li>
# <li>Schedule email.</li>
# <li>Schedule Follow-ups (follow-ups increases the chance of receiving response from recipient).</li>
# <li>Specify follow up rule. </li>
# <li>Use existing <a href="https://atmailwin.com/email/templates/?public=True">templates</a>.</li>
# </ul>
# <blockquote>
# <p><strong>Note</strong>: Don't use this service to send marketing emails or spams. It can result in your email's being sent to spam or locked.</p>
# </blockquote>
# <p>Read this <a href="https://atmailwin.com/blog/9/making-the-most-of-atmailwin-for-effective-cold-mailing/">article</a> 
# to make most out of this tool</p>
# <p><div class="notice-block alert alert-warning">This tool makes use if Jinja2 to render the emails, so any valid jinja syntax is acceptable</div>
# <h2 id="example-usage">Example Usage</h2>
# <p>Subject
# <div class="ql-code-block-container" spellcheck="false"><div class="ql-code-block">Feedback on AtMailWin</div>
# </div>
# <p>Body
# <div class="ql-code-block-container" spellcheck="false"><div class="ql-code-block">Hello {{name}},</div>
# <div class="ql-code-block">Hope you are doing well. I am {{from_name}} reaching out to you to</div>
# <div class="ql-code-block">inquire about your experience using this automation platform. It </div>
# <div class="ql-code-block">looks like your experience with us is {% if feedback == "positive" %} </div>
# <div class="ql-code-block">positive {% else %} negative {% endif %}. We would be grateful, if you </div>
# <div class="ql-code-block">could explain a little more about your feed back.</div>
# <div class="ql-code-block"></div>
# <div class="ql-code-block">{{from_signature}}</div>
# </div>
# <details>

# <summary>Output</summary>
# Hello Rob,

# Hope you are doing well. I am Paul reaching out to you to inquire about your experience using this automation platform. It looks like your experience with us is positive . We would be grateful if you could explain a little more about your feedback.

# Best regards, Paul

# </details>

# <h2 id="how-it-works">How it works?</h2>
# <ol>
# <li>Configure a email id by clicking on email configuration link.</li>
# <li>Create a email template. Use Variables within enclosed brackets <code class="inline-code">{{}}</code> to personalize the email.</li>
# <li>Schedule the email, create followups.</li>
# </ol>
# <h2 id="self-hosting">Self hosting</h2>
# <p>If you want to self host it.</p>
# <p>clone the repo
# <div class="ql-code-block-container" spellcheck="false"><div class="ql-code-block">git clone https://github.com/PaulleDemon/Email-automation</div>
# </div>
# <p>Install python 3.8 or above</p>
# <p>Install dependencies
# <div class="ql-code-block-container" spellcheck="false"><div class="ql-code-block">pip install -r requirements.txt</div>
# </div>
# <p>add a .env file inside the email_automation folder with the following 
# <div class="ql-code-block-container" spellcheck="false"><div class="ql-code-block">DEBUG=1</div>
# <div class="ql-code-block">DOMAIN=""</div>
# <div class="ql-code-block">SECRET_KEY=""</div>
# <div class="ql-code-block">PORD_SECRET_KEY=""</div>
# <div class="ql-code-block">REDIS_PROD_HOST=""</div>
# <div class="ql-code-block"></div>
# <div class="ql-code-block">FIELD_ENCRYPTION_KEY=""</div>
# <div class="ql-code-block">PROD_FIELD_ENCRYPTION_KEY=""</div>
# <div class="ql-code-block"></div>
# <div class="ql-code-block">EMAIL_HOST=""</div>
# <div class="ql-code-block">EMAIL_HOST_USER=""</div>
# <div class="ql-code-block">EMAIL_HOST_PASSWORD=""</div>
# <div class="ql-code-block"></div>
# <div class="ql-code-block">POSTGRES_DATABASE=""</div>
# <div class="ql-code-block">POSTGRES_USER=""</div>
# <div class="ql-code-block">PROD_DB_PASSWORD=""</div>
# <div class="ql-code-block">POSTGRES_PASSWORD=""</div>
# <div class="ql-code-block">POSTGRES_HOST=""</div>
# <div class="ql-code-block"></div>
# <div class="ql-code-block">POSTGRES_URL=""</div>
# <div class="ql-code-block"></div>
# <div class="ql-code-block">FIREBASE_CRED_PATH=""</div>
# </div>
# <p><div class="notice-block alert alert-warning">You must fill up the values required</div>
# <p><div class="notice-block alert alert-warning">You can create encryption key using the following <code>python manage.py generate_encryption_key</code></div>
# <p><div class="notice-block alert alert-warning">To generate secret key use <code>from django.core.management.utils import get_random_secret_key</code> then <code>get_random_secret_key()</code> in your python shell</div>
# <p>Run database creation queries using
# <div class="ql-code-block-container" spellcheck="false"><div class="ql-code-block">python manage.py migrate</div>
# </div>
# <p>now run the website using 
# <div class="ql-code-block-container" spellcheck="false"><div class="ql-code-block">python manage.py runserver</div>
# </div>
# '''

# delta = convert_html_to_delta(html_string)
# print(delta)
