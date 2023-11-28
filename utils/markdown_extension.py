import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor

from .common import get_language_name

class CodeDivExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(CodeDivPreprocessor(md), 'codediv', 15)
        md.postprocessors.register(CodeDivPostprocessor(md), 'codedivpost', 0)


class CodeDivPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        in_code_block = False
        code_block_lines = []

        extension = ''
        for line in lines:
            if line.strip().startswith("```"):
                if in_code_block:
                    # Closing code block
                    in_code_block = False
                    code_content = '\n'.join(code_block_lines)
                    new_lines.append(f'<div class="ql-code-block-container {"language-"+get_language_name(extension) if extension else ""}" spellcheck="false">{code_content}</div>\n')
                    code_block_lines = []
                else:
                    extension = line.strip()[3:].strip() or ''

                    # Opening code block
                    in_code_block = True

                    code_block_lines = []

            elif line.startswith("> "):
                quote_content = line[2:].strip()
                new_lines.append(f'<div class="notice-block alert alert-warning">{quote_content}</div>')
            
            elif in_code_block:
                # code_content = '\n'.join(code_block_lines)
                code = f'<div class="ql-code-block">{line}</div>\n'
                # new_lines.append(code)
                code_block_lines.append(code)
            else:
                line = self.convert_inline_code(line)
                new_lines.append(line)

        return new_lines

    def convert_inline_code(self, line):
        # Convert inline code to custom div structure
        while '`' in line:
            line = line.replace('`', '<code class="inline-code">', 1)
            line = line.replace('`', '</code>', 1)
        return line

class CodeDivPostprocessor(Postprocessor):
    def run(self, text):
        # Remove <p> tags from code blocks
        text = text.replace('<p><div class="ql-code-block-container"', '<div class="ql-code-block-container"')
        text = text.replace('</div></p>', '</div>')
        text = text.replace('<p><div class="ql-code-block">', '<div class="ql-code-block">')
        return text


# Example usage
# if __name__ == "__main__":
#     md_text = """
#     # Example Markdown with Code Blocks

#     Some text before the code block.

#     ```python
#     def hello_world():
#         print("Hello, world!")
#     ```

#     Some text after the code block.
#     """

#     md = markdown.Markdown(extensions=[CodeDivExtension()])
#     html = md.convert(md_text)

#     # Remove <code> and <pre> tags from the output
#     html = html.replace('<code>', '').replace('</code>', '').replace('<pre>', '').replace('</pre>', '')

#     print(html)
