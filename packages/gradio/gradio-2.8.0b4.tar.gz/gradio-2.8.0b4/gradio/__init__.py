import pkg_resources

from gradio.routes import get_state, set_state
from gradio.flagging import *
from gradio.interface import *
from gradio.mix import *

current_pkg_version = pkg_resources.require("gradio")[0].version
__version__ = current_pkg_version
