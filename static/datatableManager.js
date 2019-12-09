class datatableManager {
    constructor(idMainTable, idTopicsTable){
        this.idMainTable = idMainTable
        this.idTopicsTable = idTopicsTable
        this.activeTable = idMainTable
    }

    showMainTable(){
        $$(`${this.activeTable}`).hide()
        $$(`${this.idMainTable}`).show()
        this.activeTable = this.idMainTable
    }

    showTopicsTable(){
        $$(`${this.activeTable}`).hide()
        $$(`${this.idTopicsTable}`).show()
        this.activeTable = this.idTopicsTable
    }

    updateMainTableByRequest(requestString, requestData){
        $$(`${this.idMainTable}`).clearAll()
        const tableID = this.idMainTable

        webix.ajax(requestString, requestData, function(result) {
            result = JSON.parse(result)
            let i = 0
            for (var key in result) {
                console.log(key)
                $$(tableID).parse([{
                    id: key,
                    filename: result[key]["filename"],
                    creation: result[key]["date_creation"],
                    topics: result[key]["topics_list"],
                    duration: result[key]["duration"]
                }])
                i++
            }
        });
    }

    updateTopicsTableByRequest(requestString, requestData){
        $$(`${this.idTopicsTable}`).clearAll()
        const tableID = this.idTopicsTable
        
        webix.ajax(requestString, requestData, function(result) {
            result = JSON.parse(result)
            console.log(result)
            
            for (var key in result) {
                let topicsNumber = result[key]["topic_name"].length
                console.log(topicsNumber)
                console.log(key)
                for (var i = 0; i < topicsNumber; i++){
                    console.log(result[key]["topic_name"][i])
                    $$(tableID).add({
                        id: i,
                        topic_name: result[key]["topic_name"][i],
                        msgs_type: result[key]["msgs_type"][i],
                        msgs_num: result[key]["msgs_num"][i],
                    })
                }
            }
        });
    }
    
}