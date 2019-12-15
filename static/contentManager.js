class contentManager {
    constructor(idHeader, idMainTable, idTopicsTable, idMsgsTable, idMainMenu, idTopicsMenu, idMsgsMenu){
        this.idMainTable = idMainTable
        this.idTopicsTable = idTopicsTable
        this.idMsgsTable = idMsgsTable

        this.idMainMenu = idMainMenu
        this.idTopicsMenu = idTopicsMenu
        this.idMsgsMenu = idMsgsMenu

        this.activeTable = idMainTable
        this.activeMenu = idMainMenu
    }

    showMainTable(){
        // this._SetLabelInHeader(textOfMainLabel)
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

    showMsgsTable(){
        $$(`${this.activeTable}`).hide()
        $$(`${this.activeMenu}`).hide()
        $$(`${this.idMsgsTable}`).show()
        $$(`${this.idMsgsMenu}`).show()
        this.activeTable = this.idMsgsTable
        this.activeMenu = this.idMsgsMenu
    }

    updateMainTableByRequest(requestString, requestData){
        $$(`${this.idMainTable}`).clearAll()
        const tableID = this.idMainTable

        webix.ajax(requestString, requestData, function(result) {
            result = JSON.parse(result)
            let i = 0
            for (var key in result) {
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
            
            for (var key in result) {
                let topicsNumber = result[key]["topic_name"].length
                for (var i = 0; i < topicsNumber; i++){
                    $$(tableID).add({
                        id: key + "|_|" + result[key]["topic_name"][i],
                        topic_name: result[key]["topic_name"][i],
                        msgs_type: result[key]["msgs_type"][i],
                        msgs_num: result[key]["msgs_num"][i],
                    })
                }
            }
        });
    }

    updateMsgsTableByRequest(requestString, requestData){
        $$(`${this.idMsgsTable}`).clearAll()
        const tableID = this.idMsgsTable
        
        webix.ajax(requestString, requestData, function(result) {
            result = JSON.parse(result)
            console.log(requestData)
            
            for (var key in result) { // должен быть один   
                let msgs = result[key]["msgs_list"]["msgs_list"]

                msgs.forEach(element => {
                    console.log(element)
                    $$(tableID).add({
                        id: requestData["id"] + "|_|" + requestData["topic_name"] + "|_|" + element['msg_name'],
                        msgs_name: element['msg_name'],
                        msgs_type: element['msg_type'],
                    })   
                });
            }
        });
    }

    activateClearMainMenuItem(){
        $$(`${this.idMainMenu}`).enableItem("mainClear")
    }

    deactivateClearMainMenuItem(){
        $$(`${this.idMainMenu}`).disableItem("mainClear")
    }

    activateClearTopicsMenuItem(){
        $$(`${this.idTopicsMenu}`).enableItem("topicsClear")
    }

    deactivateClearTopicsMenuItem(){
        $$(`${this.idTopicsMenu}`).disableItem("topicsClear")
    }
    

    getCurrentIdsFromMainTable(){
        let ids = []
        $$(`${this.idMainTable}`).eachRow((row) => {
            ids.push(row)
        })
        return ids
    }
    // _SetLabelInHeader(text){
    //     let idLabel = "headerLabel"
                
    //     let label = $$(idLabel)["config"]["label"]
    //     console.log("header before", label)
    //     label += text + "/"
    //     $$(idLabel)["config"]["label"]= label
    //     console.log($$(idLabel)["config"]["label"])
    //     $$(idLabel).refresh()
    // }

}