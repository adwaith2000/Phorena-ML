from influxdb import InfluxDBClient

client = InfluxDBClient(
    host = '10.152.183.211',
    port = 8086,
    username = 'exofense',
    password = 'password'
)
client.switch_database('exofense')

mean = client.query('SELECT MEAN(value) FROM cpu_reading').raw['series'][0]['values'][0][1]
stddev = client.query('SELECT STDDEV(value) FROM cpu_reading').raw['series'][0]['values'][0][1]

print("Rows with anomaly")
for row in client.query("SELECT * FROM cpu_reading").raw['series'][0]['values']:
    value = row[4]
    print((value-mean)/stddev)
    if((value-mean)/stddev > 0.5 or (value-mean)/stddev < -0.5):
        print(row)