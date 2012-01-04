
SSGateway database tables
========================= 

TODO migrate these table their plural forms.

This is a guide to the SharedSolar's database tables.

Core tables
-----------
These table repersent 


* Meters

  Table name: `meter`

  .. autoclass:: gateway.models.Meter

* Circuits

  Table name: `circuit`

  .. autoclass:: gateway.models.Circuit

* Accounts

  Table name: `account`
  
  .. autoclass:: gateway.models.Account

* Devices

  Table name: `devices`
  
  .. autoclass:: gateway.models.Device

* Users

  Table name: `user`

  .. autoclass:: gateway.models.Users

* Group

  Table name: `groups`
  
  .. autoclass:: gateway.models.Groups

* Tokens

  Table name: `token`

  .. autoclass:: gateway.models.Token


* Token Batches

  Table name: `tokenbatch`

  .. autoclass:: gateway.models.TokenBatch


Base tables
-----------

These tables are base types. Each of these tables will have several
child tables that "inherent" from their parent class. Inheritance is
done via sqlalchemy, a primary key call id is shared between the
parent and child table. *Note that we do not use the built in system
of table inheritance that Postgresql supports*.

* Communication interface

  .. autoclass:: gateway.models.CommunicationInterface

* Message

  .. autoclass:: gateway.models.Message

* Alerts

  .. autoclass:: gateway.models.Alert

* Jobs

  .. autoclass:: gateway.models.Job

* Logs

  .. autoclass:: gateway.models.Log


Child tables
------------

Child tables inherent columns from their parent classes. This allows
for the Gateway code to query, for example, all of the jobs assoicated
with an meter or circuit.


CommunicationInterface
++++++++++++++++++++++

* TwilioInterface

  .. autoclass:: gateway.models.TwilioInterface

* KannelInterface

  .. autoclass:: gateway.models.KannelInterface

* AirtelInterface

  .. autoclass:: gateway.models.AirtelInterface

* YoInterface
 
  .. autoclass:: gateway.models.YoInterface

* NetbookInterface

  .. autoclass:: gateway.models.NetbookInterface

Messages
+++++++++

* IncomingMessage

  .. autoclass:: gateway.models.IncomingMessage

* OutgoingMessage

  .. autoclass:: gateway.models.OutgoingMessage


* JobMessage

  .. autoclass:: gateway.models.JobMessage

Alerts
++++++

* UnresponsiveCircuit

  .. autoclass:: gateway.models.UnresponsiveCircuit


* PowerMax 

  .. autoclass:: gateway.models.PowerMax

* EnergyMax
  
  .. autoclass:: gateway.models.EnergyMax

* LowCredit

  .. autoclass:: gateway.models.LowCredit

* NoCredit

  .. autoclass:: gateway.models.NoCredit

* UnresponsiveJob

  .. autoclass:: gateway.models.UnresponsiveJob

* PowerOn

  .. autoclass:: gateway.models.PowerOn


Logs
++++

* PCULog 

  .. autoclass:: gateway.models.PCULog

* PrimaryLog 

   .. autoclass:: gateway.models.PrimaryLog


Jobs
++++ 

* AddCredit

  .. autoclass:: gateway.models.AddCredit

* TurnOff

  .. autoclass:: gateway.models.TurnOff

* TurnOn

  .. autoclass:: gateway.models.TurnOn

* Mping

  .. autoclass:: gateway.models.Mping

* Cping

  .. autoclass:: gateway.models.Cping

