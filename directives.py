# Define a new directive `code-block` (aliased as `sourcecode`) that uses the
# `pygments` source highlighter to render code in color.
#
# Incorporates code from the `Pygments`_ documentation for `Using Pygments in
# ReST documents`_ and `Octopress`_.
#
# .. _Pygments: http://pygments.org/
# .. _Using Pygments in ReST documents: http://pygments.org/docs/rstdirective/
# .. _Octopress: http://octopress.org/
import hashlib
import os
import re

from docutils import nodes
from docutils.parsers.rst import directives, Directive
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer


class Pygments(Directive):
    """Source code syntax hightlighting."""
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    string_opts = ['title', 'url', 'caption']
    option_spec = dict([(key, directives.unchanged) for key in string_opts])
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer_name = self.arguments[0]
            lexer = get_lexer_by_name(lexer_name)
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer_name = 'text'
            lexer = TextLexer()
        formatter = HtmlFormatter()

        # Construct cache filename
        cache_file = None
        content_text = u'\n'.join(self.content).encode('utf-8')
        cache_file_name = (u'%s-%s.html' %
                           (lexer_name,
                            hashlib.md5(content_text).hexdigest()))
        cached_path = self._get_cached_path(cache_file_name)

        # Look for cached version, otherwise parse
        if os.path.exists(cached_path):
            cache_file = open(cached_path, 'r')
            parsed = cache_file.read()
        else:
            parsed = highlight(content_text, lexer, formatter)

        # Strip pre tag and everything outside it
        pres = re.compile("<pre>(.+)<\/pre>", re.S)
        stripped = pres.search(parsed).group(1)

        lined = ''
        for idx, line in enumerate(stripped.splitlines(True)):
            lined += '<span class="line">%s</span>' % line

        # Add wrapper with optional caption and link
        code = '<figure class="code">'
        if self.options:
            caption = ''
            title = 'link'
            link = ''

            if 'caption' in self.options:
                caption = ('<span>%s</span>' % self.options['caption'])
            if 'title' in self.options:
                title = self.options['title']
            if 'url' in self.options:
                link = ('<a href="%s">%s</a>' % (self.options['url'], title))

            if caption or link:
                code += '<figcaption>%s %s</figcaption>' % (caption, link)

        code += ('<div class="highlight"><pre><code class="%s">%s</code>'
                 '</pre></div>' % (lexer_name, lined))
        code += '</figure>'

        # Write cache
        if cache_file is None:
            cache_file = open(cached_path, 'w')
            cache_file.write(parsed)
        cache_file.close()

        return [nodes.raw('', code, format='html')]

    def _get_cached_path(self, cache_file_name):
        # TODO(gryf): Here is an assumption, that .pygments-cache directory
        # will lay on top direcotry of jekyll project. Make it *real* tmp, by
        # using tempfile module.
        cached_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   '../../.pygments-cache'))
        if not os.path.exists(cached_path):
            os.makedirs(cached_path)

        return os.path.join(cached_path, cache_file_name)


directives.register_directive('code-block', Pygments)
directives.register_directive('sourcecode', Pygments)
