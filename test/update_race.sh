curl -X PUT \
  http://localhost:5000/race/$1 \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 1,
    "name": "Mezza Maratona di Lucca (update)",
    "time": "07/05/2023 10:00",
    "city": "Lucca (update)",
    "distance": 21092,
    "website": "http://www.luccamarathon.it/"
}'
