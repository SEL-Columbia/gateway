import uuid
import urllib2
import urllib


def make_request(msg, phone="+22365489009"):
    data = urllib.urlencode({'message': msg,
                             'number': phone,
                             'uuid': str(uuid.uuid4()) })
    return urllib2.Request(
        data=data, url="http://localhost:6543G/interface/send/6")


def test_consumer_messages():
    account = 'beu754'
    token = '95021282753'

    def test_balance_english():
        response = urllib2.urlopen(make_request("bal." + account))
        print("----------------------------")
        print("testing english balance")
        print(response.read())
        print("-----------------------------")

    def test_balance_num():
        response = urllib2.urlopen(make_request("2." + account))
        print("----------------------------")
        print("testing balance with numeric command")
        print(response.read())
        print("-----------------------------")

    def test_balance_failure():
        response = urllib2.urlopen(make_request("bal.1234"))
        print("----------------------------")
        print("testing english balance fail conition")
        print(response.read())
        print("-----------------------------")

    def test_balance_french():
        response = urllib2.urlopen(make_request("solde." + account))
        print("----------------------------")
        print("testing french balance")
        print(response.read())
        print("----------------------------")

    def test_balance_french_failure():
        response = urllib2.urlopen(make_request("solde.12345"))
        print("----------------------------")
        print("testing french balance fail conition")
        print(response.read())
        print("----------------------------")

    def test_change_primary_phone():
        response = urllib2.urlopen(make_request("prim." + account + ".18182124554"))
        print("----------------------------")
        print("set primary number english")
        print(response.read())
        print("----------------------------")

    def test_primary_phone_french():
        response = urllib2.urlopen(make_request("tel." + account + ".18185846103"))
        print("----------------------------")
        print("set primary number fr")
        print(response.read())
        print("----------------------------")

    def test_add_credit_english():
        response = urllib2.urlopen(
            make_request("add." + account + "." + str(token)))
        print("----------------------------")
        print("add credit in en")
        print(response.read())
        print("----------------------------")

    def test_add_credit_french():
        response = urllib2.urlopen(
            make_request("recharge." + account  + "." + str(token)))
        print("----------------------------")
        print("add credit in fr")
        print(response.read())
        print("----------------------------")

    def test_on_message():
        response = urllib2.urlopen(make_request("on." + account))
        print("----------------------------")
        print("turn the circuit on fr/en ")
        print(response.read())
        print("----------------------------")

    def test_off_message():
        response = urllib2.urlopen(make_request("off." + account))
        print("----------------------------")
        print("turn the circuit off fr/en ")
        print(response.read())
        print("----------------------------")

    def test_usage_english():
        response = urllib2.urlopen(make_request("use." + account))
        print("----------------------------")
        print("testing use en")
        print(response.read())
        print("----------------------------")

    def test_usage_french():
        response = urllib2.urlopen(make_request("conso." + account))
        print("----------------------------")
        print("testing use fr")
        print(response.read())
        print("----------------------------")

    def test_fail_message():
        response = urllib2.urlopen(make_request("this should fail" + account))
        print("----------------------------")
        print("test failure with a response")
        print(response.read())
        print("----------------------------")

    # test_balance_num()
    # test_balance_english()
    # test_balance_failure()
    # test_balance_french()
    # test_balance_french_failure()
    # test_change_primary_phone()
    # test_primary_phone_french()
    test_add_credit_english()
    # test_add_credit_french()
    # test_usage_english()
    # test_usage_french()
    # test_fail_message()


def test_meter_messages():

    cid = "192.168.1.201"
    meter_name = "demo001"

    def test_pp():
        """ test primary log
        """
        response = urllib2.urlopen(
            make_request("(job=pp&cid=" + cid  + "&mid=" + meter_name + "&wh=10.00&tu=12.12&ts=20110107192318&cr=20.10&status=1)", phone="+22365271087"))
        print("----------------------------")
        print("testing primary log")
        print(response.read())
        print("----------------------------")

    def test_job_delete():
        """ Test job delete message
        """
        response = urllib2.urlopen(
            make_request("(job=delete&status=1&tu=2256&ts=20110107192318&wh=9.7&cr=475.95&jobid=2205&ct=CIRCUIT)", phone="13474594669"))
        print("----------------------------")
        print("Testing job delete message")
        print(response.read())
        print("----------------------------")

    def test_alert_meter_down():
        response = urllib2.urlopen(
            make_request("(job=alert&mid=" +
                     meter_name + "&cid=" + cid + "&alert=md)", phone="18185846103"))
        print("----------------------------")
        print("testing alert meter down")
        print(response.read())
        print("----------------------------")

    def test_alert_sdc():
        """ Test meter sd card not found
        """
        response = urllib2.urlopen(
            make_request("(job=alert&mid=" +
                     meter_name + "&cid=" + cid + "&alert=sdc)", phone="18185846103"))
        print("----------------------------")
        print("testing alert test meter sd card not found")
        print(response.read())
        print("----------------------------")

    def test_alert_low_credit():
        """ Test circuit low credit
        """
        response = urllib2.urlopen(
            make_request("(job=alert&mid=" +
                     meter_name + "&cid=" + cid
                     + "&alert=lcw&cr=10.00)"))
        print("----------------------------")
        print("testing alert low credit")
        print(response.read())
        print("----------------------------")

    def test_alert_no_credit():
        """ Test circuit no credit
        """
        msg = '(job=alert&mid=' + meter_name + '&cid=' + cid + '&alert=nocw&cr=00.00)'
        response = urllib2.urlopen(
            make_request(msg))
        print("----------------------------")
        print("testing alert no credit")
        print(response.read())
        print("----------------------------")

    def test_alert_emax():
        msg = '(job=alert&mid=' + meter_name + '&cid=' + cid + '&alert=emax&cr=00.00)'
        response = urllib2.urlopen(
            make_request(msg))
        print("----------------------------")
        print("testing emac alert")
        print(response.read())
        print("----------------------------")

    def test_circuit_compontent_failure():
        """ Test circuit compontent failure
        """
        response = urllib2.urlopen(
            make_request("(job=alert&mid="
                         + meter_name + "&cid=" + cid + "&alert=ce)", phone="18185846103"))
        print("----------------------------")
        print("testing alert ce")
        print(response.read())
        print("----------------------------")

    #test_pp()
    test_job_delete()
    #test_alert_meter_down()
    #test_alert_sdc()
    #test_alert_low_credit()
    #test_alert_no_credit()
    #test_alert_emax()
    #test_circuit_compontent_failure()

test_consumer_messages()
#test_meter_messages()
