from hashlib import sha256
import random

random.seed(0)

MAX_INT32 = 2 ** 32 - 1
MAX_TIME_TO_DIG_ONE_BLOCK = 36000  # 10-minutes


def getHash(data):
    return sha256(data.encode('utf-8')).hexdigest()


def getNonce():
    return random.randint(0, MAX_INT32)


def generateBlock(prev_hash):
    nonce = getNonce()
    h = getHash(f"{nonce}{prev_hash}")
    return h


def digBlock():
    """ `Tk ~ Exp(a)` """
    return random.randint(0, MAX_TIME_TO_DIG_ONE_BLOCK)


def digNBlocks(n):
    """ `Sn ~ Gamma(n,a)` """
    Ts = [digBlock() for i in range(n)] # time per digged block
    Sn = sum(Ts)                        # sum of times
    return Ts, Sn


def stochasticProcess(time, blocks):
    """ `N(t)` """
    totalTime = 0
    diggedBlocks = 0
    for blockTime in blocks:
        if totalTime + blockTime <= time:
            totalTime += blockTime
            diggedBlocks += 1
        else:
            break
    return diggedBlocks
