
SSGateway database tables
========================= 

TODO migrate these table their plural forms.

This is a guide to the SharedSolar's database tables.

Core tables
-----------

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
