import pytest
import utils

#from wiki_converter.core.log import create_logger
#from wiki_converter.core.function import create_parser, create_converter
from md2ameblo.core.log import create_logger
from md2ameblo.core import Markdown2Ameblo
#from md2ameblo.

class TestMarkdown2Ameblo(object):

    def setup_method(self, method):
        self.log = create_logger(True)
        self.md2ameblo = Markdown2Ameblo(self.log)
#       self.p = create_parser('confluence_ameblo', {}, self.log)
#       self.c = create_converter('ameblo', {}, self.log)

    def teardown_method(self, method):
        pass


    def test_simple(self):
        output = self.md2ameblo.convert("""
# h1
hello world.
""".strip()
)
        assert output == "<h3>h1</h3><p>hello world.</p>"

    def test_code_to_pre(self):
        output = self.md2ameblo.convert("""
### code
```
#!/usr/bin/env python
import markdown2
```
""".strip()
)
        assert output.strip() == """
<h3>code</h3><p><pre>#!/usr/bin/env python
import markdown2</pre></p>
""".strip()
