 meanReading = from(bucket: "exofense/")|> range(start: 1970-08-28T22:00:00Z) |> filter(fn: (r) => r._measurement == "temp_reading") |> mean()

stdDeviation = from(bucket: "exofense/") 
    |> range(start: 1970-08-28T22:00:00Z) 
    |> filter(fn: (r) => r._measurement == "temp_reading") 
    |> stddev()

from(bucket: "exofense/") 
    |> range(start: 1970-08-28T22:00:00Z) 
    |> filter(fn: (r) => r._measurement == "temp_reading") 
    |> aggregateWindow(every: , fn: mean)
    |> yield(name: "mean")