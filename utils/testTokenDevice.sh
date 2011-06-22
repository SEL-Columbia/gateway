curl -v -H "Content-Type: application/json" \
-X POST -d "{\"device_id\": \"abc123\", \"tokens\": [{\"denomination\": 500, \"count\": 10}, {\"denomination\": 500, \"count\": 24}]}" \
http://localhost:6543/manage/make_tokens
