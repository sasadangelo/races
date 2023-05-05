curl -X POST \
  http://localhost:5000/race \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Maratona di Roma",
    "time": "03/04/2023 09:00",
    "city": "Roma",
    "distance": 42192,
    "website": "http://www.maratonadiroma.it/"
}'
