curl -v -H "Content-Type: application/json" \
-X POST -d "{\"device_id\": \"abc123\", \"tokens\" : [ {\"token_id\" : 56386878804 , \"account_id\" : \"b\"}] }" \
http://localhost:6543/manage/update_tokens
