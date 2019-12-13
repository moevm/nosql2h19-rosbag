class contentManager {
    constructor(idMainTable, idTopicsTable, idMsgsTable, idMainMenu, idTopicsMenu, idMsgsMenu){
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
        console.log("error;", `${this.idMainTable}`)
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
                // console.log(topicsNumber)
                // console.log(key)
                for (var i = 0; i < topicsNumber; i++){
                    console.log(result[key]["topic_name"][i])
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
        console.log("Request data:", requestData)
        
        webix.ajax(requestString, requestData, function(result) {
            result = JSON.parse(result)
            console.log(result)
            
            for (var key in result) { // должен быть один   
                let msgs = result[key]["msgs_list"]["msgs_list"]
                console.log(msgs)
                msgs.forEach(element => {
                    console.log(element)
                    $$(tableID).add({
                        // id: key,
                        msgs_name: element['msg_name'],
                        msgs_type: element['msg_type'],
                        // msgs_list: result[key]["msgs_num"][i],
                    })   
                });

                // for (var i = 0; i < topicsNumber; i++){
                //     console.log(result[key]["topic_name"][i])
                //     $$(tableID).add({
                //         id: i,
                //         topic_name: result[key]["topic_name"][i],
                //         msgs_type: result[key]["msgs_type"][i],
                //         msgs_num: result[key]["msgs_num"][i],
                //     })
                // }
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
    
}