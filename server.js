const express = require("express")
const fs = require("fs")
const { get } = require("http")
const app = express()
const PORT = 3000
const jsonpath = "./src/data.json"


app.use(express.static('public'))


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

if (fs.existsSync(jsonpath)) {

	fs.readFile(jsonpath, (err, data_string) => {
		if (err) throw err;

		var get_data = JSON.parse(data_string)
		for (let i = 0; i < get_data.list.length-1; i++) {
			DataObj.add(get_data.list[i].temp,
				get_data.list[i].humidtiy,
				get_data.list[i].fullDate,
				get_data.list[i].fullDate2,
				get_data.list[i].fullDate3,
				get_data.list[i].fullDate4,
				get_data.list[i].date_time
			);
		}	
	console.log(DataObj);

	})
}
	

function writeItDown() {
	DataObj.add(23, 32, "2", "20", "2", "5", "3")
	fs.writeFileSync(jsonpath, JSON.stringify(DataObj, null, 2), 'utf-8', (err) => {
		if (err) throw err
		console.log("data succesfully added to file!");
	})
}

writeItDown()


app.get("/getData", function (req,res )  {
	// send whole object ... data.list[i]....
	res.send(JSON.stringify(DataObj.list))
})


app.listen(PORT, () => {
	console.log(`server listening on http://localhost:${PORT}/index.html`)
})



