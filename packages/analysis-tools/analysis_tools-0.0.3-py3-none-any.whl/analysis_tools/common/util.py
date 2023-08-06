### common.py ###################################
# Commonly used functions, classes are defined in here
###############################################


from analysis_tools.common.env import *

### lambda functions
tprint     = lambda dic: print(tabulate(dic, headers='keys', tablefmt='psql'))  # print 'dic' with fancy 'psql' form
display_md = lambda msg: display(Markdown(msg))
list_all   = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path))]
list_dirs  = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if isdir(join(path, name))]
list_files = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if isfile(join(path, name))]

def rmdir(path):
    if isdir(path):
        shutil.rmtree(path)


### PATH
class PATH:
    @classmethod
    def update(cls, ROOT='.'):
        cls.ROOT   = abspath(ROOT)
        cls.SRC    = join(cls.ROOT, 'src')
        cls.INPUT  = join(cls.ROOT, 'input')
        cls.OUTPUT = join(cls.ROOT, 'output')
        cls.TRAIN  = join(cls.INPUT, 'train')
        cls.TEST   = join(cls.INPUT, 'test')
        cls.CKPT   = join(cls.SRC, 'ckpt')
        cls.RESULT = join(cls.ROOT, 'result')
PATH.update("..")
