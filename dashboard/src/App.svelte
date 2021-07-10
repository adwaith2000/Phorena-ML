<script>
	import { onMount } from "svelte";
	import Chart from 'svelte-frappe-charts';

    const apiURL = "http://localhost:5001";

    let data = [];
	let dataResp = [];
	let sensors = [];

	let limit = 30;
	let currSensor = "All clients";

	let chartData = {
		labels: [],
		datasets: []
	};

	onMount(async function() {
        const response = await fetch(apiURL);
		const sensorsInResp = [];
		const isAnomalyShown = false;

        dataResp = (await response.json()).map(data => {
			let date = new Date(data.time);  
			let options = {  
    			weekday: "long", year: "numeric", month: "short",  
    			day: "numeric", hour: "2-digit", minute: "2-digit"  
			}; 
			data.time = date.toLocaleTimeString("en-us", options);

			data.sensor_name = data.sensor_name || 'client-temp';
			if(! sensorsInResp.includes(data.sensor_name)) {
				sensorsInResp.push(data.sensor_name);
			}

			return data;
		}).reverse();

		sensors = [...sensorsInResp];
		data = dataResp.slice(0, limit);
    });

	async function changeData(e) {
		currSensor = e.target.value;
	}

	function changeLimit(e) {
		limit = e.target.value;
	}

	function getData(sensor, limit) {
		if(limit == "All") limit = dataResp.length;
		if(sensor === "All clients") {
			console.log("All clients");	
			return dataResp.slice(0, limit);
		}
		
		return dataResp.filter(data => data.sensor_name === sensor).slice(0, limit); 
	}

	function getChartData(data) {
		return {
			labels: data.map(dataVal => dataVal.time),
			datasets: [{
				values: data.map(dataVal => dataVal.value),
			}]
		};
	}

	$: data = getData(currSensor, limit);
	$: chartData = getChartData(data);
</script>

<main>
	<h1>Dashboard</h1>
	<div class="controls">
	<span>
	Limit: &nbsp; &nbsp;<select on:change="{changeLimit}">
		<option>30</option>
		<option>60</option>
		<option>90</option>
		<option>All</option>
	</select>
	</span>
	<span>
	Select client: &nbsp; &nbsp;<select on:change="{changeData}">
		<option>All clients</option>
		{#each sensors as sensor}
			<option>{sensor}</option>
		{/each}
	</select>
	</span>
	</div>

	<Chart data={chartData} type="line" />

	<table>
		<thead>
			<tr>
				<th>Time</th>
				<th>Reading</th>
				<th>Sensor</th>
				<th>Topic</th>
			</tr>
		</thead>
		{#each data as item}
			<tr class="{item.anomaly? 'anomaly': ''}">
				<td>{item.time}</td>
				<td>{item.value}</td>
				<td>{item.sensor_name}</td>
				<td>{item.topic}</td>
			</tr>
		{/each}
	</table>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	table {
		
    	border-collapse: collapse;
    	margin: 25px 0;
    	font-size: 1em;
		width: 100%;
    	font-family: sans-serif;
    	min-width: 400px;
    	box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);

	}
	
	thead tr {
    	background-color: #009879;
    	color: #ffffff;

	}

	table tbody tr {
    	border-bottom: 1px solid #dddddd;
	}

	table th,
	table td {
	    padding: 12px 15px;
	}

	table tr:nth-of-type(even) {
    	background-color: #f3f3f3;
	}

	table tr:last-of-type {
	    border-bottom: 2px solid #009879;
	}

	tr.anomaly {
		background: red !important;
		color: #fff !important;
	}

	.controls {
		display: flex;
		justify-content: space-around;
		width: 100%;
	}
</style>