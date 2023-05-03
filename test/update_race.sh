curl -X PUT \
  http://localhost:5000/race/$1 \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 1,
    "name": "Mezza Maratona di Lucca",
    "time": "07/05/2023 09.00",
    "city": "Lucca",
    "distance": 21097,
    "website": "http://www.luccamarathon.it/"
}'
