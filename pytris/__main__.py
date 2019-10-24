from .utils import parse_args
args = parse_args()

if args.test:
    from .test_all import *
