# 
#   NatML
#   Copyright (c) 2022 Yusuf Olokoba.
#

from argparse import ArgumentParser
from .login import login_cli
from .predictor import create_predictor
from ..version import __version__

# Constants
CATEGORIES = [
    "vision", "vision/classification", "vision/detection", "vision/segmentation", "vision/translation", "vision/text",
    "natural language", "natural language/classification", "natural language/qa", "natural language/completion", "natural language/entity recognition", "natural language/summarization", "natural language/translation",
    "audio", "audio/classification", "audio/speech-to-text", "audio/text-to-speech", "audio/translation",
    "time series"
]
PREDICTOR_TYPES = ["edge", "hub"]
GRAPH_FORMATS = ["onnx", "tensorflow", "pytorch"]
ASPECT_MODES = ["scale", "fill", "fit"]

# Create parser
parser = ArgumentParser(description=f"NatML CLI {__version__}")
subparsers = parser.add_subparsers()

# Create top-level parsers
login_parser = subparsers.add_parser("login")
predictor_parser = subparsers.add_parser("predictors")

# Create sub-parsers
predictor_subparsers = predictor_parser.add_subparsers()

# Login
login_parser.add_argument("--access-key", type=str, required=True, help="NatML access key")
login_parser.set_defaults(func=login_cli)

# Create predictor
create_predictor_parser = predictor_subparsers.add_parser("create")
create_predictor_parser.add_argument("--tag", type=str.lower, required=True, help="Predictor tag")
create_predictor_parser.add_argument("--type", type=str.lower, required=True, choices=PREDICTOR_TYPES, help="Predictor type")
create_predictor_parser.add_argument("--model", type=str, required=True, help="Path to ML model")
create_predictor_parser.add_argument("--format", type=str.lower, required=False, choices=GRAPH_FORMATS, help="Model graph format")
create_predictor_parser.add_argument("--private", action="store_true", help="Make predictor private")
create_predictor_parser.add_argument("--category", type=str.lower, required=True, choices=CATEGORIES, help="Predictor category")
create_predictor_parser.add_argument("--description", type=str, required=False, help="Predictor description")
create_predictor_parser.add_argument("--draft-format", type=str.lower, required=False, choices=GRAPH_FORMATS, help="Preferred graph format for draft predictor")
create_predictor_parser.add_argument("--executor", type=str, required=False, help="Path to executor for Hub predictor")
create_predictor_parser.add_argument("--labels", type=str, required=False, help="Path to line-separated classification labels")
create_predictor_parser.add_argument("--aspect", type=str.lower, required=False, choices=ASPECT_MODES, help="Image aspect mode")
create_predictor_parser.set_defaults(func=create_predictor)

# Define entry point
def main ():
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)

# Run
if __name__ == "__main__":
    main()
