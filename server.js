const express = require("express")
const fs = require("fs")
const { get } = require("http")
const app = express()
const PORT = 3000

const jsonPath = "./src/roomStats.json"
const sensorDataPath = "./data.json"


app.use(express.static('public'))

// check if any data is there --> yes: save into array 
if (fs.existsSync(jsonPath) && hasContent(jsonPath)) {

	fs.readFile(jsonPath, (err, data_string) => {
		if (err) throw err;

		let get_data = JSON.parse(data_string)

		for (let i = 0; i < get_data.list.length; i++) {
			DataObj.add(get_data.list[i].temp,
				get_data.list[i].humidtiy,
				get_data.list[i].fullDate,
				get_data.list[i].fullDate2,
				get_data.list[i].fullDate3,
				get_data.list[i].fullDate4,
				get_data.list[i].date_time
			);
		}

		console.log("Current Data: ");
		console.log(DataObj);
	})
}

function hasContent(path) {
	fs.readFileSync(path, (err, data) => {
		if (data.length != 0) {
			return true;
		} else {
			return false;
		}
	})
}

class Data {
	constructor() {
		this.list = []
	}
	add(temp, hum, fullDate, fullDate2, fullDate3, fullDate4, dateTime) {
		var newData = {
			temp: temp,
			humidtiy: hum,
			fullDate: fullDate,
			fullDate2: fullDate2,
			fullDate3: fullDate3,
			fullDate4: fullDate4,
			date_time: dateTime
		}
		this.list.push(newData)
	}
}

const DataObj = new Data()


// wait one minute for data
var waitForData = 5000

function saveSensorDataIntervall() {
	setInterval(() => {
		//wait for sensor to get data and save it
		getSensorData()
		// write data into roomStats file 
		console.log(`Data got written to ${jsonPath}`);
	}, waitForData);
}

// write sensor data into second json file 
function writeData(data) {
	if (fs.existsSync(jsonPath)) {
		fs.writeFileSync(jsonPath, JSON.stringify(data), err => {
			if (err) throw err;
		})
	}
}

// get data from sensor.json and add them to object list
function getSensorData() {
	// check if file exists 
	if (fs.existsSync(sensorDataPath)) {
		fs.readFile(sensorDataPath, (err, getData) => {
			if (err) throw err;
			var data = JSON.parse(getData)

			for (let i = 0; i < data.list.length; i++) {
				DataObj.add(
					DataObj.add(data.list[i].temp,
						data.list[i].humidtiy,
						data.list[i].fullDate,
						data.list[i].fullDate2,
						data.list[i].fullDate3,
						data.list[i].fullDate4,
						data.list[i].date_time
					)
				)
			}
			writeData(DataObj)
		})
	}
}

saveSensorDataIntervall()

app.get("/getData", function (req, res) {
	// send data to client 
	res.send(JSON.stringify(DataObj))
})



app.listen(PORT, () => {
	console.log(`Server listening on http://localhost:${PORT}/index.html`)
})



