from simplogger import simplog
from copy import deepcopy
import json
from random import randint
import logging

class config():

    __slots__ = ('name','params','dflt','use_logs','logger','set_loglvl',\
                 'get_loglvl','dflt_loglvl','badval_loglvl','track_rqrmnts',\
                 'rqrmnts','track_usage','usage')

    configs = {}

    def __new__(cls, *args, **kargs):

        if len(args) == 0:
            x = randint(0,9999999)
            while x in cls.configs:
                x = randint(0,9999999)
            cfgkey = x.__str__()
        elif len(args) == 1:
            cfgkey = args[0]
        else:
            raise ValueError('Should be passed no value or a str')

        # If cfgkey already exists, return it
        if cfgkey in cls.configs:
            cfg = cls.configs.get(cfgkey)
            if len(args) > 1 or len(kargs) > 0:
                if cfg.use_logs:
                    cfg.logger.warn('Tried calling cfg with already existing '+\
                                    'name and provided parameters')
            return cfg
        else:
            newcfg = super(config, cls).__new__(cls)
            cls.configs[cfgkey] = newcfg
            return newcfg

    def __init__(self, *args, **kargs):
        if len(args) == 1:
            self.name = args[0]

        # Storing the values
        self.params = {}

        # Default value storage
        self.dflt = {}

        # Log parameters
        self.use_logs = kargs.pop('use_logs', True)
        # Set up logs
        if self.use_logs:
            self.logger = self.__setup_logging(**kargs)
        # Set up log lvls for different actions
        dflt_log_val = kargs.pop('loglvl',logging.DEBUG)
        self.set_loglvl = kargs.pop('set_loglvl',dflt_log_val)
        self.get_loglvl = kargs.pop('get_loglvl',dflt_log_val)
        self.dflt_loglvl = kargs.pop('dflt_loglvl',dflt_log_val)
        self.badval_loglvl = kargs.pop('badval_loglvl',dflt_log_val)

        # Requirement tracking
        self.track_rqrmnts = kargs.get('track_rqrmnts', False)
        if self.track_rqrmnts:
            self.rqrmnts = {}

        # Track usage
        self.track_usage = kargs.get('track_usage', False)
        if self.track_usage:
            self.usage = {}

    ''' Getting the values '''
    # Handles getting parameters from user input and default
    def __get(self, *args):
        if len(args) < 1:
            raise ValueError('Need to provide argument')
        key = args[0]
        try:
            if self.get_loglvl > 0:
                item = self.params.get(args[0])
                self.logger.log(self.get_loglvl, f'{key} accessed from config'+\
                                    f', returning {item} of type {type(item)}')
                return item
            else:
                return self.params.get(args[0])
        except:
            if self.get_loglvl > 0:
                self.logger.log(self.get_loglvl, f'{key} not in config')

            # If dflt log level is above 0, try to get the item and log
            if self.dflt_loglvl > 0:
                try:
                    item = self.dflt.get(args[0])
                    self.logger.log(self.dflt_loglvl, f'{key} returned {item}'+\
                        f' of type {type(item)} from default')
                    return item
                except:
                    if len(args) == 2:
                        self.logger.log(self.dflt_loglvl, \
                            f'{key} not in user input or dflt values, but '+\
                            f'{item} ({type(item)}) was provided')
                        return args[1]
                    else:
                        self.logger.exception(f'{key} was not inputted by user, '+\
                             'was not in dflt, and no dflt was given when called')

            else: # Otherwise try to remove
                if len(args) == 2:
                    return self.dflt.setdefault(args[0], args[1])
                else:
                    self.logger.exception(f'{key} was not inputted by user, '+\
                         'was not in dflt, and no dflt was given when called')

    # Returns an item, applies validation
    def get(self, *args, **kargs):
        # Get the item
        key, item = args[0], self.__get(*args)
        # Track the requirements / usage if enabled
        if self.track_rqrmnts:
            self.rqrmnts[key] = self.rqrmnts.get(key,[]).append(kargs)
        if self.track_usage:
            self.usage[key] = self.usage.get(key,0)+1
        # Validates values
        self.validate(item, raise_err=True, **kargs)
        # Returns item
        return item

    # Returns item, uses brackets
    def __getitem__(self, key):
        # Track the requirements / usage if enabled
        if self.track_usage:
            self.usage[key] = self.usage.get(key,0)+1
        return self.__get(key)

    ''' Setting user input '''
    # Sets an item in user input
    def __setitem__(self, key, item):
        self.logger.log(self.set_loglvl, f'{item} saved for {key}')
        self.params.__setitem__(key, item)

    # Sets an item in user input
    def set(self, key, item):
        self.__setitem__(key, item)

    ''' Validate the values '''
    # Validates an item given special flags from kargs
    def validate(self, item, **kargs):

        def badvalerr(msg):
            if kargs.get('raise_err', False):
                self.logger.exception(msg)
            self.logger.log(self.badval_loglvl,msg)
            return False

        if 'always_allow' in kargs:
            if item in kargs.get('always_allow'):
                return True

        # Sees if item is <
        if 'min' in kargs:
            try:
                if item <= kargs.get('min'):
                    min = kargs.get('min')
                    return badvalerr(f'{item} is < min ({min})')
            except:
                return badvalerr(f'{item} cannot be numerically compared')
        # Sees if item is <=
        if 'mineq' in kargs:
            try:
                if item < kargs.get('mineq'):
                    mineq = kargs.get('mineq')
                    return badvalerr(f'{item} is < mineq ({mineq})')
            except:
                return badvalerr(f'{item} cannot be numerically compared')
        # Sees if item is >
        if 'max' in kargs:
            try:
                if item >= kargs.get('max'):
                    max = kargs.get('max')
                    return badvalerr(f'{item} is >= max ({max})')
            except:
                return badvalerr(f'{item} cannot be numerically compared')
        # Sees if item is >=
        if 'maxeq' in kargs:
            try:
                if item > kargs.get('maxeq'):
                    maxeq = kargs.get('maxeq')
                    return badvalerr(f'{item} is > maxeq ({maxeq})')
            except:
                return badvalerr(f'{item} cannot be numerically compared')
        # Sees if item is iterable
        if 'isIter' in kargs:
            if kargs.get('isIter'):
                if not self.__isIter(item):
                    return badvalerr(f'{item} is not iterable')
            else:
                if self.__isIter(item):
                    return badvalerr(f'{item} is iterable')
        # Sees if item is hashable
        if 'isHashable' in kargs:
            if kargs.get('isHashable'):
                if not self.__isHashable(item):
                    return badvalerr(f'{item} is not hasable')
            else:
                if self.__isHashable(item):
                    return badvalerr(f'{item} is hashable')
        # Sees if item is callable
        if 'callable' in kargs:
            if kargs.get('callable'):
                if not callable(item):
                    return badvalerr(f'{item} provided is not callable')
            else:
                if callable(item):
                    return badvalerr(f'{item} provided is callable')

        # Verifies if item is in list of provided options
        if 'options' in kargs:
            options = kargs.get('options')
            if not self.__isIter(options):
                return badvalerr(f'{type(options)} given for options, however '+\
                                    'needs an iterable item')
            if item not in options:
                return badvalerr(f'{item} not in list of given options.')
        # Verifies object type
        if 'dtype' in kargs:
            if not isinstance(item, kargs.get('dtype')):
                return badvalerr(f'{item} is {type(item)}')

        return True

    ''' Import / Export '''
    # Exports as dict
    def toDict(self):
        dct = {}
        dct.update(self.dflt)
        dct.update(self.params)
        return dct
    # Loads the dict
    def loadDict(self, dct, update=False):
        if update:
            self.params.update(dct)
        else:
            self.params = deepcopy(dct)
    def to_tuple(self):
        return tuple([(key,item) for key,item in self.items()])
    def to_set(self):
        return set([(key,item) for key,item in self.items()])
    def to_frozen_set(self):
        return frozenset([(key,item) for key,item in self.items()])


    def __str__(self):
        return self.toDict().__str__()
    def __repr__(self):
        return self.toDict().__str__()

    def load_jsonfile(self, filename):
        with open(filename, 'r') as F:
            self.load_dict(json.load(F))
    def save_jsonfile(self, filename):
        with open(filename, 'w') as F:
            json.dump(F, self.toDict())

    ''' Other '''
    def __iter__(self):
        return self.toDict().__iter__()
    def __len__(self):
        return len(self.toDict())
    def items(self):
        return self.toDict().items()
    def keys(self):
        return self.toDict().keys()
    def __hash__(self):
        return self.to_frozen_set().__hash__()
    def __eq__(self,other):
        if isinstance(other, config):
            return self.to_frozen_set().__eq__(other.to_frozen_set())
        elif isinstance(other, dict):
            return self.to_frozen_set().__eq__(\
                frozenset([(key,item) for key,item in other.items()]))
        return self.to_frozen_set().__eq__(other)

    ''' Setup '''
    # Setup log
    def __setup_logging(self, **kargs):
        log = simplog(__name__)

        if kargs.get('console_log', True):
            log.addHandler(htype='stream', \
                h_lvl=kargs.get('console_loglvl',simplog.DEBUG), \
                formatter=kargs.get('console_log_formatter',4))

        if kargs.get('file_log', False):
            log.addHandler(htype='file', \
                           filename=kargs.get('log_filename','config.logs'),\
                           formatter=kargs.get('file_log_formatter',4))

        if 'custom_handler' in kargs:
            for hndlr in kargs.get('custom_handler'):
                log.addHandler(hndlr)

        return log

    ''' Utililty fxns '''
    # Returns whether an item is iterable
    @staticmethod
    def __isIter(item):
        try:
            iter(item)
            return True
        except:
            return False

    # Returns whether an item is hashable
    @staticmethod
    def __isHashable(item):
        try:
            hash(item)
            return True
        except:
            return False
