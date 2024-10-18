from args import *
from formatter import *

def main():
    
    cloc = Formatter(file=args.input, fig=os.path.join(os.path.dirname(args.out), f'{application.name}.png'))
    
    write_out(args.out, content=cloc.report)
        
    return status.success

if __name__ == '__main__':
    # logger initialization
    set_logfile(application.logger)
    application_details()
    # arguments parse
    args = set_parser()
    # application execution
    sys.exit(main())
    