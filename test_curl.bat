@echo off
echo Testing Flask API endpoints with curl...
echo.

echo Testing server status:
curl -X GET http://localhost:5000
echo.
echo.

echo Testing activity booking:
curl -X POST http://localhost:5000/api/book-activity ^
  -H "Content-Type: application/json" ^
  -H "Accept: application/json" ^
  -d "{\"name\":\"Test User\",\"phone\":\"+91 9876543210\",\"email\":\"test@example.com\",\"activity\":\"trekking\",\"location\":\"parasnath\",\"participants\":2,\"date\":\"2024-02-15\",\"requirements\":\"Vegetarian food\"}"
echo.
echo.

echo Testing guide booking:
curl -X POST http://localhost:5000/api/book-guide ^
  -H "Content-Type: application/json" ^
  -H "Accept: application/json" ^
  -d "{\"name\":\"Guide Test\",\"phone\":\"+91 9876543210\",\"email\":\"guide@example.com\",\"language\":\"English\",\"places\":[\"Ranchi\",\"Netarhat\"],\"date\":\"2024-02-20\"}"
echo.
echo.

pause