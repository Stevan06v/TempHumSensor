fetch('/getData')
    .then((response) =>{
        return response.json()
    })
    .then((data) => {
        console.log(data);
        document.getElementById('box1').innerHTML = `${data[0].temp}`
        
    })
    .catch((err) =>{
        console.log(err);
    })