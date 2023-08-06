import os
import logging
import eons as e
import threading
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
import jsonpickle

######## START CONTENT ########
# For validating args
class ArgumentNotProvided(Exception): pass

# For initialization
class InitializationError(Exception): pass

# All Device errors
class DevicesError(Exception): pass

# Exception used for miscellaneous Device errors.
class OtherBuildError(DevicesError): pass

# All Routine errors
class RoutineError(Exception): pass

# Exception used for miscellaneous Routine errors.
class OtherRoutineError(RoutineError): pass


class HWBase(e.UserFunctor):
    def __init__(this, name=e.INVALID_NAME(), state=None):
        super(e.UserFunctor).__init__(name)

        # See State.py
        this.state = state

        # If you would like to loop Run() in a separate thread, set this to true, otherwise, set to false
        this.RunInThread = True

        # For required args, simply list what is needed. They will be provided as member variables or *this will not be run.
        this.requiredKWArgs = []

        # For optional args, supply the arg name as well as a default value.
        this.optionalKWArgs = {}

    # Set the state of this.
    def UseState(this, state):
        this.state = state

    # Do stuff!
    # Override this or die.
    def Run(this):
        pass

    # Hook for any pre-run configuration.
    # RETURN whether or not to continue running.
    def Initialize(this):
        return True

    # Hook for any post-run configuration.
    # RETURN whether or not Cleanup was successful.
    def Cleanup(this):
        return True

    # Will try to get a value for the given varName from:
    #    first: this
    #    second: the state
    #    third: the environment
    # RETURNS the value of the given variable or None.
    def FetchVar(this, varName, prepend=""):
        logging.debug(f"{prepend}{this.name} looking to fetch {varName}...")

        if (hasattr(this, varName)):
            logging.debug(f"...{this.name} got {varName} from myself!")
            return getattr(this, varName)

        if (this.state.Has(varName)):
            stateVar = this.state.Get(varName)
            if (stateVar is not None):
                logging.debug(f"...{this.name} got {varName} from state")
                return stateVar

        envVar = os.getenv(varName)
        if (envVar is not None):
            logging.debug(f"...{this.name} got {varName} from environment")
            return envVar

        return None


    # Override of eons.UserFunctor method. See that class for details.
    def ValidateArgs(this):
        for rkw in this.requiredKWArgs:
            if (hasattr(this, rkw)):
                continue

            fetched = this.FetchVar(rkw)
            if (fetched is not None):
                setattr(this, rkw, fetched)
                continue

            # Nope. Failed.
            errStr = f"{rkw} required but not found."
            logging.error(errStr)
            raise ArgumentNotProvided(errStr)

        for okw, default in this.optionalKWArgs.items():
            if (hasattr(this, okw)):
                continue

            fetched = this.FetchVar(okw)
            if (fetched is not None):
                setattr(this, okw, fetched)
                continue

            logging.debug(f"Failed to fetch {okw}. Using default value: {default}")
            setattr(this, okw, default)

    # Override of eons.Functor method. See that class for details
    def UserFunction(this, ehw):

        this.UseState(ehw.state)
        this.ValidateArgs()

        if (not this.Initialize()):
            errStr = f"Failed to initialize {this.name}"
            raise InitializationError(errStr)

        if (not this.Cleanup()):
            logging.error(f"Failed to clean up {this.name}")

    # Run whatever.
    # DANGEROUS!!!!!
    # TODO: check return value and raise exceptions?
    # per https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess
    def RunCommand(this, command):
        p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
        while True:
            line = p.stdout.readline()
            if (not line):
                break
            print(line.decode('utf8')[:-1])  # [:-1] to strip excessive new lines.



class Device(HWBase):
    def __init__(this, name=e.INVALID_NAME()):
        super(HWBase).__init__(name)

        # See HWBase for docs
        this.RunInThread = True
        this.requiredKWArgs = []
        this.optionalKWArgs = {}

    # Do stuff!
    # Override this or die.
    def Run(this):
        pass

    # Hook for any pre-run configuration.
    # RETURN whether or not to continue running.
    def Initialize(this):
        return True

    # Hook for any post-run configuration.
    # RETURN whether or not Cleanup was successful.
    def Cleanup(this):
        return True



#State is essentially just a set of global variables which will be accessible through an EHW instance.
class State:
    def __init__(this):
        pass

    def Has(this, name):
        return hasattr(this,name)

    def Set(this, name, value):
        setattr(this, name, value)

    def Get(this, name):
        return getattr(name)

class EHW(e.Executor):

    def __init__(this):
        super().__init__(name="eons hardware", descriptionStr="Modular framework for controlling hardware devices.")

        this.RegisterDirectory("ehw")

        this.state = State()

    #Override of eons.Executor method. See that class for details
    def RegisterAllClasses(this):
        super().RegisterAllClasses()

    #Override of eons.Executor method. See that class for details
    def AddArgs(this):
        super().AddArgs()
        this.argparser.add_argument('-c', '--config', type = str, metavar = 'config.json', help = 'configuration file.', default = None, dest = 'config')
        this.argparser.add_argument('-d','--device', type = str, action='append', nargs='*', metavar = 'status_led', help = 'enables use of the specified device and assumes the device is properly connected.', dest = 'devices')
        this.argparser.add_argument('-r','--routines', type = str, action='append', nargs='*', metavar = 'blink_led', help = 'will execute the given routine.', dest = 'routines')


    #Override of eons.Executor method. See that class for details
    def ParseArgs(this):
        super().ParseArgs()

        # These are only sets while being populated. They will become lists at the end of this method.
        this.devices = set()
        this.routines = set()

        if (os.path.isfile(this.args.config)):
            config = jsonpickle.decode(open(this.args.config, 'r').read())
            for key in config:
                if (key == "devices"):
                    [this.devices.add(d) for d in config[key]]
                elif (key == "routines"):
                    [this.routines.add(r) for r in config[key]]
                else:
                    this.state.Set(key, config[key])

        if (this.args.devices is not None):
            [[this.devices.add(str(d)) for d in l] for l in this.args.devices]
        this.devices = list(this.devices)

        if (this.args.routines is not None):
            [[this.routines.add(str(r)) for r in l] for l in this.args.routines]
        this.routines = list(this.routines)

        for arg, val in this.extraArgs.items():
            this.state.Set(arg, val)

    #Override of eons.Executor method. See that class for details
    def UserFunction(this, **kwargs):
        super().UserFunction(**kwargs)
        for d in this.devices:
            this.StartHW(d, "dev")
        for r in this.routines:
            this.StartHW(r, "routine")

    #Run some HWBase.
    def StartHW(this, hwName, type):
        hw = this.GetRegistered(hwName, type)
        logging.debug(f"Starting {hw}")
        hw(ehw=this)


class Routine(HWBase):
    def __init__(this, name=e.INVALID_NAME()):
        super(HWBase).__init__(name)

        # See HWBase for docs
        this.RunInThread = True
        this.requiredKWArgs = []
        this.optionalKWArgs = {}

    # Do stuff!
    # Override this or die.
    def Run(this):
        pass

    # Hook for any pre-run configuration.
    # RETURN whether or not to continue running.
    def Initialize(this):
        return True

    # Hook for any post-run configuration.
    # RETURN whether or not Cleanup was successful.
    def Cleanup(this):
        return True

