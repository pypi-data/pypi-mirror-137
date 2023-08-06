
from mistletoe.html_renderer import HTMLRenderer
# from mistletoe.block_token import BlockCode
# from subprocess import Popen, PIPE
# import select
import base64
from shutil import move
import rich
import re
import os
import logging
from .Executor import RootExecutor
from .Executor import GnuPlotExecutor
from .Executor import RnuPlotExecutor
# from . import log
from rich.logging import RichHandler
from .YamlBlock import YamlFence, CodeFence
import yaml

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

"""
HTML renderer for mistletoe with ROOT code execution and asset injection.
"""

pygments_extra_css = """
pre {
    line-height: 1.1em!important;
    text-size: 1.1em!important;
    font-family: 'Fira Code'
}
"""

codetemplate = '<pre class="languag-{lang}"><code class="language-{lang}">{inner}</code></pre>'
divtemplate = '<div class="output" >' + codetemplate + '</div>'
# imgtemplate = '<img src="{src}" class="{ext}  {ucls}"/>'

autocanvast = ''
autodrawt = 'if (gPad) { gPad->Print("auto.svg"); }\n'



class RootHtmlRenderer(HTMLRenderer, RootExecutor):
    def __init__(self, *extras):
        RootExecutor.__init__(self, *extras)
        super().__init__(YamlFence, CodeFence)
        log.debug("RootHtmlRenderer")
        self.blockid = 0
        self.embed = False
        self.asset_prefix = ""
        self.asset_dir = ""
        self.clean = False
        self.no_exec = False

        # document meta
        self.title = ""
        self.author = ""
        self.description = ""
        self.keywords = ""
        self.theme = "light"
        self.prismjs_theme = "okaidia"
        self.yaml = {}

        # Control metadata
        self.autodraw = False

        # additional executors
        self.gnuplot = GnuPlotExecutor()
        self.rnuplot = RnuPlotExecutor()
        self.highlighter = self.yaml.get("highlight", "prismjs").lower()
    
    def set( self, **kwargs ) :
        if "embed" in kwargs :
            self.embed = kwargs.get( "embed" )
        if "asset_dir" in kwargs :
            self.asset_dir = kwargs.get( "asset_dir" )
        if "asset_prefix" in kwargs:
            self.asset_prefix = kwargs.get( "asset_prefix" )
        if "clean"  in kwargs:
            self.clean = kwargs.get( "clean", False )
        if "no_exec"  in kwargs:
            self.no_exec = kwargs.get( "no_exec", False )

    def process_image_output(self, path, **kwargs):
        path = path.strip()
        _, ext = os.path.splitext( path )
        ext = ext.replace( ".", "" )

        if self.asset_dir != "" and not self.embed:
            print( "cp %s %s" % (path, self.asset_dir) )
            try :
                move( path, os.path.join( self.asset_dir, path) )
            except Exception as e:
                log.error( 'Tried move( "%s", "%s" ) ' % (path, self.asset_dir) )
                log.error( e )

        template = '<img src="data:image/{ext};charset=utf-8;base64,{data}" class="{cls} {ucls}"/>'
        # cml line flag, block option, or YAML
        if self.embed or kwargs.get( "embed", False ):
            # SVG does not need to be b64 embeded in an img tag, just load into DOM 
            if "svg" == ext:
                with open(path, "rb") as image_file:
                    return ''.join(image_file.read().decode('utf-8'))

            # b64 encode other image formats
            with open(path, "rb") as image_file:
                b64_encoded = base64.b64encode(image_file.read())
            template = '<img src="data:image/{ext};charset=utf-8;base64,{data}" class="{cls} {ucls}"/>'
            if self.clean:
                log.info( "Removing embedded asset: %s" % path )
                os.remove( path )
            if "svg" == ext:
                ext = "svg+xml"
            return template.format( ext=ext, data=b64_encoded.decode(), cls=ext, ucls=kwargs.get("ucls", "") )
        

        if self.clean:
            try:
                os.remove( path )
            except Exception as e:
                rich.inspect(e)
        # Return a link to standard image formats
        image_exts = [ "png", "jpeg", "jpg", "svg", "gif", "webp", "apng" ]
        if ext in image_exts :
            template = '<img src="{src}" class="{ext}  {ucls}"/>'
            return "\n" + template.format( src=path, ext=ext, ucls=kwargs.get("ucls", "") )
        
        # try to embed as an object (e.g. PDF)
        template = '<object data="{src}" class="{ext}" {attr}> </object>'
        return template.format( src=path, ext=ext, attr="" )
    
    def divWrap(self, inner, cls="", id=""):
        template = '<div {i} class="{c}" >\n{inner}\n</div>'
        # avoid empty id attr
        if id != "":
            id = 'id="' + id + '"'
        return template.format( i=id, c=cls, inner=inner )

    def render_yaml_fence(self, token):
        log.info("YAML Fence")
        try:
            y = yaml.safe_load( token.children[0].content )
            self.process_yaml( y )
            # Do something here
        except yaml.YAMLError as e:
            log.error( e )

        token.language = "yaml"
        if self.yaml.get( "hide", False ) == True or self.yaml.get( "hide", False ) == "1" or self.yaml.get( "hide", False ) == 1 :
            return ""
        return super().render_block_code(token)

    def pycode( self, code, lang, options ):
        log.info( "Pygments with theme: %s" % self.yaml.get( "pygments-theme", "dracula" ) )
        lexer = get_lexer_by_name( lang)
        try:
            ln = False
            if options.get("linenos", False) == "table":
                ln = "table"
            elif options.get("linenos", False) != False:
                ln = "inline"

            formatter = HtmlFormatter( style=self.yaml.get( "pygments-theme", "dracula" ), linenos=ln, wrapcode=True )
            return highlight(code, lexer, formatter)
        except ClassNotFound as e:
            log.warning( "Cannot find pygment style: %s " % self.yaml.get( "pygments-theme", "dracula" ) )
            log.info( "Using default style as fallback" )
            from pygments.styles import STYLE_MAP
            log.info( "Available styles are:" )
            log.info( STYLE_MAP )
        formatter = HtmlFormatter( style="default")
        return highlight(code, lexer, formatter)

    def hpygments( self, token ):
        return self.pycode( token.children[0].content, token.language, token.options)

    def process_yaml( self, yaml ):
        self.yaml = yaml
        self.title = yaml.get( "title", self.title )
        self.author = yaml.get( "author", self.author )
        self.description = yaml.get( "description", self.description )
        self.keywords = yaml.get( "keywords", self.keywords )
        self.autodraw = yaml.get( "auto-draw", self.autodraw )
        self.highlighter = self.yaml.get("highlight", "prismjs").lower()

        if self.autodraw:
            self.embed = True

    def render_inline_code( self, token):
        # rich.inspect( token )
        code = token.children[0].content

        # evaluate code inside BASH style blocks
        m = re.search( "\${(.*?)}", code )
        if m:
            # log.info( "--->CODE: %s" % ( m.groups()[0] ) )
            evalcode = m.groups()[0]
            evalcode += ';printf("\\n");'

            log.info( 'eval: "%s"' % evalcode )
            output, err, imgs = self.run_cmd( evalcode )
            log.info( "stdout: %s" % ( output ) )
            log.info( "stderr: %s" % ( err ) )
            return output

        return super().render_inline_code( token )

    """
    Process gnuPlot code execution
    """
    def process_gnuplot( self, token ):
        log.info( "gnuplot" )
        token.language = "python" # just for output syntax highlighting
        if self.highlighter == "pygments":
            code_block = self.hpygments( token )
        else:
            code_block =  super().render_block_code(token)
        code =token.children[0].content
        imgs = self.gnuplot.find_output( code )
        img_class = ""

        log.info( "Executing gnuplot" )
        self.gnuplot.run( code )

        # inject images
        imgout = '<div id="{id}" class="image-out gnuplot-images" style="text-align: center;">'.format( id="gnuplot-images-%d" % (self.blockid))
        for i in imgs:
            imgout += self.process_image_output( i, ucls=img_class )
        imgout += '</div>'

        return self.divWrap( code_block, "gnuplot-block input-block", "" ) + self.divWrap(
                imgout, 
                "gnuplot-block output-block", 
                "gnuplot-output-block-%d" % (self.blockid) 
            )

    """
    Process RNUPlot code execution
    """
    def process_rnuplot( self, token ):
        log.info( "rnuplot" )
        token.language = "python" # just for output syntax highlighting
        if self.highlighter == "pygments":
            code_block = self.hpygments( token )
        else:
            code_block =  super().render_block_code(token)
        code =token.children[0].content
        imgs = self.rnuplot.find_output( code )
        img_class = ""

        log.info( "Executing rnuplot" )
        self.rnuplot.run( code )

        # inject images
        imgout = '<div id="{id}" class="root-images" style="text-align: center;">'.format( id="root-images-%d" % (self.blockid))
        for i in imgs:
            imgout += self.process_image_output( i, ucls=img_class )
        imgout += '</div>'

        return code_block + self.divWrap(imgout, "gnuplot-block", "gnuplot-output-block-%d" % (self.blockid) )

    """
    Code Fence is a custom Code Block token that accepts optional arguments after the language id
    example:
    ```cpp in:0
    ...
    ```

    the above turns off echoing the input to rendered document
    """
    def render_code_fence( self, token ):
        log.info( "render_code_fence" )
        # rich.inspect( token )
        return self.render_block_code( token )

    def optionAsBool( self, options, n, default = False ):
        
        # option is false by default
        if n not in options :
            return default
        if type( options[n] ) == bool:
            return options[n]
        return  not (options.get( n, "" ).lower() == 'false' or options.get( n, "" ) == '0')

    def process_cpp( self, token ):
        if self.highlighter == "pygments":
            code_block = self.hpygments( token )
        else:
            code_block =  super().render_block_code(token)
        code = token.children[0].content
        
        # log.info( "exec: %r" % self.optionAsBool( token.options, "exec", True ) )
        # log.info ("no-exec: %r" % self.no_exec)
        if self.optionAsBool( token.options, "exec", True ) == False or self.no_exec:
            log.info( "skipping execution of cpp code block" )
            return code_block

        # rich.inspect( token.options )
        # optional class for input code block
        input_class = token.options.get( ".in", "" ) + " root-block input-block"
        code_block = self.divWrap( code_block, input_class)

        if self.autodraw:
            code = autocanvast + code + autodrawt

        # Execute the codez!
        output, err, imgs = self.run_cmd( code )
        raw_output = output
        if len(output):
            output = ("# Block [%d]\n" % self.blockid) + output

        # output controls
        if self.optionAsBool( token.options, "out", True) == False or self.optionAsBool( token.options, "stdout", True) == False:
            output = ""
        elif "out" in token.options or "stdout" in token.options:
            stdout_filename = token.options.get("out", token.options.get( "stdout", "stdout.dat" ))
            log.info( "Writing block %d stdout to file: %s" % ( self.blockid, stdout_filename ) )
            with open( stdout_filename, "w" ) as wf:
                wf.writelines( output.split() )
        if self.optionAsBool( token.options, "err", True) == False or self.optionAsBool( token.options, "stderr", True) == False:
            err = ""
        elif "err" in token.options or "stderr" in token.options:
            stderr_filename = token.options.get("err", token.options.get( "stderr", "stderr.dat" ))
            log.info( "Writing block %d stderr to file: %s" % ( self.blockid, stderr_filename ) )
            with open( stderr_filename, "w" ) as wf:
                wf.writelines( err.split() )
        
        log.error( err )

        # log.info( "silent? %r" % ('silent' in token.options) )
        if 'silent' in token.options or 'quiet' in token.options:
            output = ""
            err = ""

        if self.optionAsBool( token.options,'in', True) == False:
            code_block = ""
        
        img_class = token.options.get( ".image", "" )
        if self.optionAsBool( token.options, 'img', self.optionAsBool( token.options, 'image', True ) ) == False:
            imgs = []

        # inject stdout
        divout = '<div id="{id}" class="root-output output-block">'.format( id="root-output-%d" % (self.blockid) )
        if len( output ):
            if self.highlighter == "pygments":
                divout += self.pycode( output, "bash", {} )
            else:
                divout +=  "\n" + divtemplate.format( lang="bash", inner=self.escape_html(output) )
        divout += '</div>'

        divout += '<div id="{id}" class="root-output output-block-err">'.format( id="root-err-%d" % (self.blockid) )
        if len( err ):
            if self.highlighter == "pygments":
                divout += self.pycode( err, "bash", {} )
            else:
                divout += "\n" + divtemplate.format( lang="bash", inner=self.escape_html(err) )
        divout += '</div>'

        # inject images
        imgout = '<div id="{id}" class="root-images output-images">'.format( id="root-images-%d" % (self.blockid))
        for i in imgs:
            imgout += self.process_image_output( i, ucls=img_class )
        imgout += '</div>'


        # lexer = get_lexer_by_name("c++")
        # formatter = HtmlFormatter( style=self.yaml.get( "pygments-theme", "dracula" ))
        # if code_block != ""  and self.yaml.get("highlight", "prismjs").lower() == "pygments" :
        #     code_block = highlight(code, lexer, formatter)

        self.blockid = self.blockid + 1

        if token.options.get( "raw" ) == True:
            log.info( "RAW OUTPUT: %s" % raw_output )
            return raw_output

        return code_block + self.divWrap( divout + imgout, "root-block", "root-output-block-%d" % (self.blockid - 1) )

    def process_js(self, token):
        if self.highlighter == "pygments":
            code_block = self.hpygments( token )
        else:
            code_block =  super().render_block_code(token)
        code =token.children[0].content
        template = '<script>\n{content}\n</script>'
        if "//qin" in code:
            code_block = "" # dont output the code
        if "//noexec" in code:
            return code_block
        code_block = self.divWrap( code_block, "root-block-green")
        return code_block + template.format(content=code)

    def process_css(self, token):
        if self.highlighter == "pygments":
            code_block = self.hpygments( token )
        else:
            code_block =  super().render_block_code(token)
        code = token.children[0].content
        template = '<style>\n{content}\n</style>'
        if "/* qin */" in code or "/*qin*/" in code:
            code_block = "" # dont output the code
        if "/*noexec*/" in code or "/* noexec */" in code:
            return code_block
        code_block = self.divWrap( code_block, "root-block-green")
        return code_block + template.format(content=code)

    def process_html(self, token):
        if self.highlighter == "pygments":
            code_block = self.hpygments( token )
        else:
            code_block =  super().render_block_code(token)
        code =token.children[0].content
        template = '<div>\n{content}\n</div>'
        if "<!--qin-->" in code or "<!-- qin -->" in code:
            code_block = "" # dont output the code
        if "<!--noexec-->" in code or "<!-- noexec -->" in code:
            return code_block
        code_block = self.divWrap( code_block, "root-block-green")

        return code_block + template.format(content=code)

    def render_block_code(self, token):
        log.info( 'block_code' )
        # rich.inspect( token.options )

        # include a file into a code block
        include = token.options.get( "include", "" )
        if "include" in token.options and os.path.exists( include ):
            log.info( "including file: %s" % include )
            with open( include ) as f:
                c = f.read()
                token.children[0].content = c
        elif "include" in token.options and not os.path.exists( include ):
            log.warning( "Cannot include %s, file DNE" % include )

        if "gnuplot" == token.language or token.options.get( "exec", "" ) == "gnuplot":
            return self.process_gnuplot( token )
        
        if "rnuplot" == token.language or token.options.get( "exec", "" ) == "rnuplot":
            return self.process_rnuplot( token )

        if "cpp" == self.escape_html(token.language) or token.options.get( "exec", "" ) == "cpp":
            return self.process_cpp( token )
        
        if "js" == token.language:
            return self.process_js(token)

        if "css" == token.language:
            return self.process_css(token)

        if "html" == token.language:
            return self.process_html(token)

        if self.highlighter == "pygments":
            code_block = self.hpygments( token )
        else:
            code_block =  super().render_block_code(token)
        return code_block
    
    def loadCSS( self ):
        mycss = ""
        mydir = os.path.dirname(os.path.abspath(__file__))
        # log.info( mydir)
        prismjs_theme = self.yaml.get("prismjs_theme", self.yaml.get( "prismjs-theme", "okaidia" ))
        if  prismjs_theme in [ "a11y-dark","atom-dark","base16-ateliersulphurpool.light","cb","coldark-cold","coldark-dark","coy-without-shadows","darcula","dracula","duotone-dark","duotone-earth","duotone-forest","duotone-light","duotone-sea","duotone-space","ghcolors","gruvbox-dark","gruvbox-light","holi-theme","hopscotch","lucario","material-dark","material-light","material-oceanic","night-owl","nord","one-dark","one-light","pojoaque","shades-of-purple","solarized-dark-atom","synthwave84","vs","vsc-dark-plus","xonokai","z-touch", "coy","dark","funky","okaidia","solarizedlight","tomorrow","twilight" ]:
            with open( mydir + "/data/css/prismjs/prism-%s.css" % prismjs_theme ) as f:
                ncss = "".join(f.readlines())
                # log.info( ncss )
                mycss += "\n" + ncss
        return mycss

    def render_document(self, token):
        self.footnotes.update(token.footnotes)
        mydir = os.path.dirname(os.path.abspath(__file__))
        inner = '\n'.join([self.render(child) for child in token.children])
        try : 
            with open( os.path.join(mydir, "data/css/core.css")) as f:
                core_css = ''.join(f.readlines())
        except Exception as e:
            log.error(e)
        css = core_css
        if self.yaml.get("highlight", "prismjs").lower() == "prismjs" :
            try:
                css =css + self.loadCSS()
            except Exception as e:
                log.error( e )
        
        if self.yaml.get("highlight", "prismjs").lower() == "pygments":
            try :
                css = css + HtmlFormatter(style=self.yaml.get( "pygments-theme", "dracula" )).get_style_defs('.highlight') + pygments_extra_css
            except ClassNotFound as e:
                log.warning( "Cannot find pygments style %s" % self.yaml.get( "pygments-theme", "dracula" ) )
        html = ""
        try :
            with open( os.path.join(mydir, "data/template.html")) as f:
                html = ''.join(f.readlines())

            output =  html.format( 
                title=self.title, 
                description=self.description,
                author=self.author,
                keywords=self.keywords,
                css=css, 
                body= '\n\n{}\n'.format(inner) if inner else '' 
            )
            return output
        except Exception as e:
            log.error(e)
        return inner
