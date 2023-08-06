"""
    pygments_clingo.clingo
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Logic Programs as supported by clingo.

    The lexer should cover most of the ASPCore language and thus also be usable
    with systems like dlv.

    :copyright: Copyright 2021-2022 by Roland Kaminski
    :license: MIT, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, bygroups, using
from pygments.lexers import PythonLexer, LuaLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation

__all__ = ['ClingoLexer']


def _script_lexer(name, lexer):
    return (rf'(?s)(\s*)(\()({name})(\))(\s*)(.*)(#end)(\s*)(\.)',
            bygroups(Text, # space
                     Punctuation, # (
                     Text, # python
                     Punctuation, # )
                     Text, # space
                     using(lexer),
                     Keyword, # end
                     Text, # space
                     Punctuation), # .)
            '#pop')


class ClingoLexer(RegexLexer):
    """
    Lexer for Clingo files.
    """
    name = 'Clingo'
    aliases = ['clingo']
    filenames = ['*.lp', '*.asp', '*.clingo', '*.gringo']
    mimetypes = ['text/plain']

    flags = re.UNICODE | re.MULTILINE

    tokens = {
        'root': [
            (r'%\*', Comment.Multiline, 'nested-comment'),
            (r'%.*', Comment.Single),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'\d+', Number.Integer),
            (r'"(\\n|\\"|\\\\|[^\\])*"', String.Double),
            (r':-', Punctuation),
            (r'[\[\](){}]', Punctuation),
            (r'((?<!:):-|(?<!:):~|\.(?!\.)|,(?!;)|;(?!;)|:(?!:))', Punctuation),
            (r'\&[_]*[a-z][a-zA-Z_]*', Keyword),
            (r'[/<=>+\-*\\?&@|:;~k.!]+', Operator),
            (r'(#count|#sum|#min|#max|#show|#const|#edge|#minimize|#maximize|'
             r'#defined|#heuristic|#project|#program|'
             r'#external|#theory|not)\b', Keyword),
            (r'#script', Keyword, 'script'),
            (r'(#inf|#sup|#true|#false)\b', Keyword.Constant),
            (r'[_]*[A-Z][a-zA-Z_]*', Name.Variable),
            (r'_', Name.Variable),
            (r'[_]*[a-z][a-zA-Z_]*', Text),
            (r'\s', Text),
        ],
        'script': [
           _script_lexer('python', PythonLexer),
           _script_lexer('lua', LuaLexer),
        ],
        'nested-comment': [
            (r'\*%', Comment.Multiline, '#pop'),
            (r'%\*', Comment.Multiline, '#push'),
            (r'[^*%]+', Comment.Multiline),
            (r'[*%]', Comment.Multiline),
        ],
    }

    def analyse_text(text):
        return ':-' in text
