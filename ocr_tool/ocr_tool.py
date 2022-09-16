#
# ocr_tool ds ChRIS plugin app
#
# (c) 2022 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp
import pytesseract
import os, re
from langdetect import detect_langs
import pycountry

Gstr_title = r"""
                 _              _
                | |            | |
  ___   ___ _ __| |_ ___   ___ | |
 / _ \ / __| '__| __/ _ \ / _ \| |
| (_) | (__| |  | || (_) | (_) | |
 \___/ \___|_|   \__\___/ \___/|_|
           ______
          |______|
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       ocr_tool

    SYNOPSIS

        docker run --rm fnndsc/pl-ocr_tool ocr_tool                     \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-ocr_tool ocr_tool                        \
                /incoming /outgoing

    DESCRIPTION

        `ocr_tool` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.
"""


class OcrTool(ChrisApp):
    """
    An application that can take images as input and identify and extract written text from them
    """
    PACKAGE                 = __package__
    TITLE                   = 'A ChRIS OCR plugin app'
    CATEGORY                = 'Utility'
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 2000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 8000  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        def get_input_output_path(f):
            outfilename = re.sub('\.\w+$', '.txt', f)
            input_path = os.path.join(options.inputdir, f)
            output_path = os.path.join(options.outputdir, outfilename)
            return input_path, output_path

        def convert_lang_code(input):
            lang = pycountry.languages.get(alpha_2=input)
            return lang.alpha_3

        def auto_detect_langs(contents):
            all_detected_langs = list(convert_lang_code(x.lang) for x in detect_langs(contents))
            if "eng" not in all_detected_langs:
                all_detected_langs.append("eng")
            return all_detected_langs


        print(Gstr_title)
        print('Version: %s' % self.get_version())
        inputdir = options.inputdir
        outputdir = options.outputdir
        print("Converting images in %s to text in %s" % (inputdir, outputdir))

        # TODO, make this an option
        options.auto_detect_langs = True

        for f in os.listdir(inputdir):
            img, txt = get_input_output_path(f)
            contents = pytesseract.image_to_string(img)

            if options.auto_detect_langs:
                all_detected_langs = auto_detect_langs(contents)
                custom_config = r'-l %s --psm 6' % "+".join(all_detected_langs)
                contents = pytesseract.image_to_string(img, config=custom_config)
            with open(txt, "w") as f:
                f.write(contents)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
