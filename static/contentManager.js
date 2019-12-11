class contentManager {
    constructor(idMainTable, idTopicsTable, idMainMenu, idTopicsMenu){
        this.idMainTable = idMainTable
        this.idTopicsTable = idTopicsTable
        this.idMainMenu = idMainMenu
        this.idTopicsMenu = idTopicsMenu
        this.activeTable = idMainTable
        this.activeMenu = idMainMenu
    }

    showMainTable(){
        $$(`${this.activeTable}`).hide()
        $$(`${this.activeMenu}`).hide()
        $$(`${this.idMainTable}`).show()
        $$(`${this.idMainMenu}`).show()
        this.activeTable = this.idMainTable
        this.activeMenu = this.idMainMenu
    }

    showTopicsTable(){
        $$(`${this.activeTable}`).hide()
        $$(`${this.activeMenu}`).hide()
        $$(`${this.idTopicsTable}`).show()
        $$(`${this.idTopicsMenu}`).show()
        this.activeTable = this.idTopicsTable
        this.activeMenu = this.idTopicsMenu
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
    

    getCurrentIdsFromMainTable(){
        let ids = []
        $$(`${this.idMainTable}`).eachRow((row) => {
            ids.push(row)
        })
        return ids
    }
    
}