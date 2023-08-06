

__all__ = ['MAX_DIMENSION', 'DEFAULT_HEIGHT', 'DEFAULT_WIDTH', 'is_notebook', 'is_colab', 'merge_dicts']


# 이 모듈을 helloai에서만 사용하는 것으로, 
# HelloAI의 모든 모듈에 import 될수 있어서, 
# helloai모듈을 import해서 사용해서는 안된다.

MAX_DIMENSION = 1024
DEFAULT_HEIGHT= 640
DEFAULT_WIDTH = 640

# def is_notebook():
#     # https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
#     print('@config:', hasattr(__builtins__,'__IPYTHON__'))
#     return hasattr(__builtins__,'__IPYTHON__')

def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def is_colab():
    try:
        shell = get_ipython().__class__.__module__
        if shell == 'google.colab._shell':
            return True   
        else:
            return False  
    except NameError:
        return False


def merge_dicts(defaut_options, options):
    # defaut_options를 options으로 업데이트 
     ret_opts = defaut_options.copy()
     ret_opts.update(options)
     print('merge_dicts', options)
     return ret_opts



     