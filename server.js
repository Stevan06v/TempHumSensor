const express = require("express")
const fs = require("fs")
const app = express()
const PORT = 3000


app.use(express.static('public'))




app.listen(PORT, ()=>{
	console.log(`server listening on http://localhost:$(PORT)/index.html`)
})



