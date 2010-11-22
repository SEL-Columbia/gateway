import transaction
import threading
import datetime
import time
from Queue import Queue
from gateway.models import DBSession, Message,\
    Circuit, Token, SystemLog, Account, AddCredit, TurnOn, TurnOff

delimiter = "."
sendMessageQueue = Queue() 

def get_circuit(message): 
    """ 
    Tries to match message to a circuit 
    """ 
    session = DBSession() 
    pin = message["text"].split(delimiter)[1]
    try:         
        return session.query(Circuit).filter_by(pin=pin).first()
    except Exception,e: 
        session.add(SystemLog("Unable to find circuit\
error@%s message@%s " % (e,message["uuid"])))
        transaction.commit() 
        return False

def get_token(message): 
    """
    Tries to match message to token.
    """
    session = DBSession() 
    token = message["text"].split(delimiter)[2] 
    try:
        return session.query(Token).\
            filter_by(state="new").filter_by(token=token).first() 
    except Exception,e: 
        session.add(SystemLog("Unable to find token\
error@%s message@%s" %(e,message["uuid"]))) 
        return False 

def get_balance(message,lang="en"):     
    """
    Allows users to check blance
    """
    circuit = get_circuit(message)
    if circuit:
        if lang == "en": 
            response = "The remaining electricity \
    credit on %s is %s as of %s" % (circuit.pin,
                                     circuit.credit,
                                     datetime.datetime.now().ctime())
        elif lang =="fr": 
            response = "%s unites. Il restait %s unites sur\
    la ligne %s le %s." % (circuit.credit,
                            circuit.credit,
                            circuit.pin,
                            datetime.datetime.now().ctime())
        Message.send_message(to=message["from"],text=response) 
    else: 
        pass # failt to match any circuit 

def set_primary_contact(message,lang="en"): 
    """
    Allows users to set their primary contact number
    """
    session = DBSession() 
    circuit = get_circuit(message) 
    if circuit:
        account = session.\
            query(Account).get(circuit.account.id) 
        new_number = message["text"].split(delimiter)[2] 
        old_number = account.phone
        if lang == "en": 
            Message.send_message(
                message["from"],
                "The previous primary contact number %s\
 has been replaced with the number %s." % (old_number,
                                           new_number))
            if new_number != message["from"]:
                Message.send_message(
                    new_number, 
                    "The previous primary contact number %s\
 has been replaced with the number %s." % (old_number,
                                           new_number))                    
        elif lang == "fr": 
            Message.send_message(
                message["from"],
"Votre numero de contact est desormais %s. Le numero %s ne\
 sera plus utilise." % (new_number,
                        old_number))
            if new_number != message["from"]:
                Message.send_message(
                    new_number, 
                    "Votre numero de contact est desormais %s. Le numero %s ne\
 sera plus utilise." % (new_number,
                        old_number))
        account.phone = new_number
        session.merge(account) 
        transaction.commit() 
    else: 
        pass # fail to match any circuit 

def add_credit(message,lang="en"): 
    """
    Allows consumer to add credit to their account.
    Sends an outgoing message to the consumer. 
    """
    session = DBSession()
    circuit = get_circuit(message)
    token = get_token(message)
    if circuit and token:
        session.add(AddCredit(circuit=circuit,credit=token.value))
        if lang == "en": 
            Message.send_message(
                message["from"],"Credit has been\
 added to account %s. Status: %s" % (circuit.pin,circuit.status))
        elif lang == "fr": 
            Message.send_message(message["from"],"Merci ! Le solde\
 de la ligne %s est desormais. La ligne est %s." % (circuit.pin,circuit.status))
        token.state = "used"
        transaction.commit()
    else: 
        pass 

def turn_circuit_on(message,lang="en"): 
    session = DBSession()
    circuit = get_circuit(message)
    if circuit:
        if circuit.account.lang == "en" : 
            Message.send_message(message["from"],"Account %s is %s.\
Remaining credit: %s" % (circuit.pin,circuit.status,circuit.credit))
        elif circuit.account.lang == "fr" : 
            Message.send_message(message["from"],"%s La ligne %s est %s.\
 Solde restant: %s." % (circuit.status,circuit.pin,circuit.status,circuit.credit))
        job = TurnOn(circuit)
        session.add(job)
    else: 
        pass # 

def turn_circuit_off(message,lang="en"): 
    session = DBSession() 
    circuit = get_circuit(message)
    if circuit:
        if circuit.account.lang == "en": 
            pass 
        elif circuit.account.lang == "fr": 
            pass 
        session.add(TurnOff(circuit))
        transaction.commit()
    else: 
        pass # 

def set_primary_lang(message): 
    pass 

def use_history(message,lang="en"): 
    if lang == "en": 
        pass 
    elif lang == "fr":
        pass 

def parse_message(message): 
    if message:
        text = message["text"].lower()  
        # allow consumers to check their balance        
        if text.startswith("job"): # collect all jobs
            pass 
        if text.startswith("bal"):
            get_balance(message)
        elif text.startswith("solde"): 
            get_balance(message,"fr")                
        # allow consumers to set their primary contact 
        elif text.startswith("prim"): 
            set_primary_contact(message)
        elif text.startswith("tel"): 
            set_primary_contact(message,"fr")             
        # allow consumers to add credit to their circuits
        elif text.startswith("add"): 
            add_credit(message) 
        elif text.startswith("recharge"): 
            add_credit(message,"fr") 
        # allow consumers to turn circuits on 
        elif text.startswith("on"): 
            turn_circuit_on(message)
        # allow consumers to turn circuit off
        elif text.startswith("off"): 
            turn_circuit_off(message)
        # allows consumers to get their use history
        elif text.startswith("use"): 
            use_history(message)
        elif text.startswith("conso"): 
            use_history(message,"fr")
        # allow users to set their primary contact language 
        elif text.startswith("english"): 
            set_primary_lang(message) 
        else: 
            # fall through if it does not
            Message.send_message(message["from"],
                                 "Unable to processs your message") 
    time.sleep(3) 

process_messages = threading.Thread(target=parse_message)
