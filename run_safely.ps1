# Safe profile collection script with proper delays

$industry = "Data Engineer"
$count = 150  # Safe number to avoid rate limits
$api_key = "AIzaSyA5tjOlmPZxbKXz9uDzvNqPO_Sco7Oq9-k"
$cx = "d4849e3a9180a4ea6"
$delay = 5  # 5 seconds delay

Write-Host "Starting safe profile collection..."
Write-Host "Industry: $industry"
Write-Host "Count: $count"
Write-Host "Delay: $delay seconds"
Write-Host ""

python main.py --industry $industry --count $count --api_key $api_key --cx $cx --delay $delay

Write-Host ""
Write-Host "Done! Check the CSV file for results."

