function addData(){
    console.log("Added data!")
    $.post("/addData", {}, (data) => {
        // data = JSON.parse(data)
        console.log("Response from server checking:", data)
        alert(`Response from server: ${JSON.stringify(data)}`)
    });
}