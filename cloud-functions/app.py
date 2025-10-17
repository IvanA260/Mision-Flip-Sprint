from main import process_telemetry
import functions_framework

# Este archivo es necesario para Gen2
functions_framework.http("process_telemetry", process_telemetry)