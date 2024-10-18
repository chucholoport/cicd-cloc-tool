from utils import *

def set_parser():
    '''
    Set parser for application
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--cloc-report', dest='input', action='store', default=inputs.file)
    parser.add_argument('-o', '--out',         dest='out',   action='store', default=out.file)
    args = parser.parse_args()

    check_file(args.input, ext=inputs.extension, exists=True)
    check_file(args.out, ext=out.extension)
    
    return args