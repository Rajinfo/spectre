# Define the path to your JaCoCo HTML report
$reportPath = "C:\program\test\java-17-examples\examples\jce-demo\build\reports\jacoco\test\html\index.html"

# Read the HTML file content
$htmlContent = Get-Content -Path $reportPath -Raw

# Use a regular expression to extract the total coverage percentage
if ($htmlContent -match '<tfoot>.*?<td class="ctr2">(\d+%)</td>.*?</tfoot>') {
    $coveragePercent = $matches[1]
    Write-Output "Total Coverage: $coveragePercent"
} else {
    Write-Output "Coverage percentage not found."
}
