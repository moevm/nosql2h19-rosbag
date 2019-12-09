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
                    id: i,
                    filename: result[key]["filename"],
                    creation: result[key]["date_creation"],
                    topics: result[key]["topics_list"],
                    duration: result[key]["duration"]
                }])
                i++
            }
        });
    }
    
}