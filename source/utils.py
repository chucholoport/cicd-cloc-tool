from vars import *

def set_ext(name:str, ext:str):
    '''
    Set an extension to string file name if not yet included
    '''
    return '.'.join(locals().values()) if not name.endswith(f'.{ext}') else name

def set_logfile(name:str, reset:bool=True):
    '''
    Create logfile for application
    '''
    name = set_ext(name,'log')
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.FileHandler(filename=name, mode='w'))
    logging.basicConfig(filename=name, format='%(levelname)s: %(message)s', encoding='utf-8', level=application.log_level)

def set_code(struct:tuple):
    '''
    Set code string for log
    '''
    return f'{struct[1]}. code: {str(struct[0])}'

def print_log(msg, lvl:int=logging.INFO):
    '''
    Print log message with respective level
    '''
    if lvl == logging.INFO:   
        lvl = levelname.info
        logging.info(f'{msg}')
    elif lvl == logging.DEBUG:   
        lvl = levelname.debug
        logging.debug(f'{msg}')
    elif lvl == logging.WARNING: 
        lvl = levelname.warning
        logging.warning(f'{msg}')
    elif lvl == logging.ERROR:
        lvl = levelname.error
        msg = set_code(msg)
        logging.error(f'{msg}')
    else:
        lvl = levelname.info
    print(": ".join(filter(None,[lvl, msg])))
    if lvl == levelname.error: sys.exit()
    
def application_details():
    '''
    Print application details
    '''
    name    = f'* {application.name} *'
    line    = ''.join(['*' for x in range(len(name))])
    logging.info(line)
    logging.info(name)
    logging.info(line)
    logging.info(f'version: {application.version}')
    logging.info(f'author: {application.author}\n')
    
def check_file(name:str, ext:str, exists:bool=False):
    if not name:
        print_log(error.missing_argument, logging.ERROR)
    if not str(name).endswith(ext):
        print_log(error.invalid_extension, logging.ERROR)
    if exists:
        if not os.path.exists(name):
            print_log(error.argument_not_found, logging.ERROR)
        if not os.path.isfile(name):
            print_log(error.invalid_argument, logging.ERROR)

def write_out(name:str, content:str):
    '''
    Write output file
    '''
    try:
        print_log(f'writting {name}')
        if not os.path.exists(os.path.dirname(name)):
            os.mkdir(os.path.dirname(name))
        with open(name, mode='w') as out:
            out.write(content)
        print_log(f'done.\n')
    except:
        print_log(f'unable to write {name}\n', lvl=logging.WARNING)
        
def fig_to_base64(fig):
    '''
    Convert python figure to base64 (for embedded image in html)
    '''
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())