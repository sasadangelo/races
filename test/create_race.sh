curl -X POST \
  http://localhost:5000/race \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Mezza Maratona di Lucca",
    "time": "07/05/2023 09:00",
    "city": "Lucca",
    "distance": 21097,
    "website": "http://www.luccamarathon.it/"
}'
