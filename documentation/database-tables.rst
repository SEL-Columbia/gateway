
SSGateway database tables
========================= 

This is a guide to the SharedSolar's database tables.

Core tables
-----------

#. Meter
   Meters are 

#. Circuits

#. Accounts

#. Devices

#. Users

#. Tokens

#. Token Batches

Base tables
-----------

These tables are base types. Each of these tables will have several
child tables that "inherent" from their parent class. Inheritance is
done via sqlalchemy, a primary key call id is shared between the
parent and child table. *Note that we do not use the built in system
of table inheritance that Postgresql supports*.

#. Communication interface

#. Message

#. Alerts

#. Jobs


Child tables
------------
