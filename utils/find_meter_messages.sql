-- SQL query to find incoming messages associated with a meter.
-- 
--SELECT incoming.id, message.number
--                    FROM incoming_message AS incoming, message WHERE message.id = incoming.id;

SELECT meter.name, message.date, incoming_message.text
       FROM meter, message, incoming_message
       WHERE meter.phone = message.number AND meter.name = 'ml07'
       AND message.id = incoming_message.id ORDER BY message.date DESC;
