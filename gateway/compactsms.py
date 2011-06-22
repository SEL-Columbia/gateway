
from datetime import datetime
import random, sys, urllib, urlparse
from collections import deque

def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Convert positive integer to a base36 string. Source: Wikipedia"""
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')

    # Special case for zero
    if number == 0:
        return '0'

    base36 = ''

    sign = ''
    if number < 0:
        sign = '-'
        number = - number

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36

def base36decode(number):
    return int(number, 36)

class Globals:
    maxlen_sms = 160
    max_tu = 86400 # number of seconds in a day
    max_wh = 99999 # tenths; [0 - 10kWh]
    max_cr = 9999999 # hundredths; [0 - 100K]
    factor_wh = 10.0
    factor_cr = 100.0

def paren_enclose(s):
    return '(' + s.strip() + ')'

def deflatelogs(logs):
    """Returns a list of messages containing compressed logs"""

    compressedmessages = []
    transformedmessages = deque()

    # get the meterid and timestamp from the first log
    firstlog = logs[0]
    parsedfirstlog = urlparse.parse_qs(firstlog)
    job = 'l' # primary log
    timestamp = base36encode(int(
            datetime.strptime(parsedfirstlog["ts"][0], "%Y%m%d%H%M%S"
                              ).strftime("%y%m%d%H")))

    # transform the logs
    for log in logs:
        parsedlog = urlparse.parse_qs(log)
        if parsedlog["ct"][0] == "MAINS":
            transformedmessages.append(
                (base36encode(int(float(parsedlog["wh"][0]) * Globals.factor_wh)), 1))
        else:
            transformedmessages.append(
                ("%s,%s,%s,%s" % (base36encode(int(parsedlog["cid"][0][-2:])), 
                                  base36encode(int(parsedlog["tu"][0])), 
                                  base36encode(int(float(parsedlog["wh"][0]) * Globals.factor_wh)), 
                                  base36encode(int(float(parsedlog["cr"][0]) * Globals.factor_cr))), 
                 int(parsedlog["status"][0])))

    header = "Transformed Messages:"
    print header
    print "=" * len(header)
    for i, message in enumerate(transformedmessages):
        print i+1, message
    print

    # compress into messages
    sectiondelim = '#'
    prefix = "%s%s" % (job, timestamp)
    consection = []
    coffsection = []

    while transformedmessages:
        nextlog = transformedmessages[0][0]
        nextstatus = transformedmessages[0][1]

        tmpmessage = ""
        if nextstatus == 1:
            tmpconsection = consection[:]
            tmpconsection.append(nextlog)
            tmpmessage = sectiondelim.join([
                    prefix, 
                    ';'.join(tmpconsection), 
                    ';'.join(coffsection)])
        else:
            tmpcoffsection = coffsection[:]
            tmpcoffsection.append(nextlog)
            tmpmessage = sectiondelim.join([
                    prefix, 
                    ';'.join(consection), 
                    ';'.join(tmpcoffsection)])

        if len(tmpmessage) + 2 > Globals.maxlen_sms: # +2 for the ()
            message = sectiondelim.join([
                    prefix, 
                    ';'.join(consection), 
                    ';'.join(coffsection)])
            compressedmessages.append(paren_enclose(message))
            consection[:]= []
            coffsection[:]= []
        else:
            if nextstatus == 1:
                consection.append(nextlog)
            else:
                coffsection.append(nextlog)

            transformedmessages.popleft()

            if not transformedmessages:
                compressedmessages.append(paren_enclose(sectiondelim.join([
                                prefix, 
                                ';'.join(consection), 
                                ';'.join(coffsection)])))
                
    return compressedmessages

def inflatelogs(logs):
    """Returns a list of messages containing uncompressed logs"""

    sectiondelim = '#'
    uncompressedmessages = []
    transformedmessages = deque()

    for log in logs:
        if '(' not in log or ')' not in log: # discard incomplete message
            continue

        # remove leading and trailing ()
        log = log[1:-1]
        # split the sections: prefix, con, coff
        prefix, consection, coffsection = log.split(sectiondelim)

        # get the meterid and timestamp from the prefix
        timestamp = datetime.strptime(
            str(base36decode(prefix[1:])), "%y%m%d%H").strftime("%Y%m%d%H")

        for circuits in [c for c in consection.split(';') if c]:
            status = 1
            messageparts = circuits.split(',')
            if len(messageparts) == 2:  #mains
                ct = "MAINS"
                wh = base36decode(messageparts[0]) / Globals.factor_wh
                tu = base36decode(messageparts[1])
                cid = "192.168.1.2%02d" % (0,)  #192.168.1.200
                kv = (("job", "pp"),
                      ("status", status),
                      ("ts", timestamp),
                      ("cid", cid),
                      ("tu", tu),
                      ("wh", wh),
                      ("cr", 0),
                      ("ct", ct))
                uncompressedmessages.append(urllib.urlencode(kv))
            elif len(messageparts) == 1:  # mains
                ct = "MAINS"
                wh = base36decode(messageparts[0]) / Globals.factor_wh
                cid = "192.168.1.2%02d" % (0,) # 192.168.1.200
                kv = (("job", "pp"),
                      ("status", status),
                      ("ts", timestamp),
                      ("cid", cid),
                      ("tu", 86400),
                      ("wh", wh),
                      ("cr", 0),
                      ("ct", ct))
                uncompressedmessages.append(urllib.urlencode(kv))
                
            else: # consumer circuits
                ct = "CIRCUIT"
                cid = "192.168.1.2%02d" % (base36decode(messageparts[0]),)
                tu = base36decode(messageparts[1])
                wh = base36decode(messageparts[2]) / Globals.factor_wh
                cr = base36decode(messageparts[3]) / Globals.factor_cr
                kv = (("job", "pp"),
                      ("status", status),
                      ("ts", timestamp),
                      ("cid", cid),
                      ("tu", tu),
                      ("wh", wh),
                      ("cr", cr),
                      ("ct", ct))
                uncompressedmessages.append(urllib.urlencode(kv))

        for circuits in [c for c in coffsection.split(';') if c]:
            status = 0
            messageparts = circuits.split(',')

            ct = "CIRCUIT"
            cid = "192.168.1.2%02d" % (base36decode(messageparts[0]),)
            tu = base36decode(messageparts[1])
            wh = base36decode(messageparts[2]) / Globals.factor_wh
            cr = base36decode(messageparts[3]) / Globals.factor_cr
            kv = (("job", "pp"),
                  ("status", status),
                  ("ts", timestamp),
                  ("cid", cid),
                  ("tu", tu),
                  ("wh", wh),
                  ("cr", cr),
                  ("ct", ct))
            uncompressedmessages.append(urllib.urlencode(kv))

    return uncompressedmessages

def mkoriginallog(status, ts, cid, tu, wh, cr, ct):
    kv = (("job", "pp"),
          ("status", status),
          ("ts", ts),
          ("cid", cid),
          ("tu", tu),
          ("wh", wh),
          ("cr", cr),
          ("ct", ct))
    return urllib.urlencode(kv)

if __name__ == "__main__":

    num_circuits = int(sys.argv[1])
    ts = datetime.now().strftime("%Y%m%d%H%M%S")

    originallogs = deque()
    mains = mkoriginallog(1, 
                          ts,
                          "192.168.1.200", 
                          random.choice(xrange(Globals.max_tu)),
                          random.choice(xrange(Globals.max_wh)) / Globals.factor_wh,
                          0,
                          "MAINS")
    originallogs.append(mains)

    for cid in xrange(1, num_circuits + 1):
        circuit = mkoriginallog(random.choice((0, 1)), 
                                ts,
                                "192.168.1.2%02d" % (cid,),
                                random.choice(xrange(Globals.max_tu)),
                                random.choice(xrange(Globals.max_wh)) / Globals.factor_wh,
                                random.choice(xrange(-10000, Globals.max_cr)) / Globals.factor_cr,
                                "CIRCUIT")
        originallogs.append(circuit)

    header = "Original Uncompressed Logs:"
    print header
    print "=" * len(header)
    for i, log in enumerate(originallogs):
        print i+1, log
    print

    deflatedlogs = deflatelogs(originallogs)    
    header = "Compressed Logs:"
    print header
    print "=" * len(header)
    for i, log in enumerate(deflatedlogs):
        print i+1, log
    print

    inflatedlogs = inflatelogs(deflatedlogs)    
    header = "Uncompressed Logs:"
    print header
    print "=" * len(header)
    for i, log in enumerate(inflatedlogs):
        print i+1, log
    print    

    print "Total number of SMS sent for %d circuit logs = %d" % (
        num_circuits + 1, len(deflatedlogs))
