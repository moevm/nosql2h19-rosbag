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

        webix.ajax(requestString, requestData, {
            success: function(result, data, XmlHttpRequest) {
                result = JSON.parse(result)
                console.log(result)
                result.forEach(element => {
                    $$(tableID).parse([{
                        id: element["id"],
                        filename: element["filename"],
                        creation: element["date_creation"],
                        topics: element["topics_list"],
                        duration: element["duration"],
                    }])                    
                })
            },
            error: function(text, data, XmlHttpRequest){
                webix.alert("Что-то пошло не так!")
            },
        });
    }

    updateTopicsTableByRequest(requestString, requestData){
        $$(`${this.idTopicsTable}`).clearAll()
        const tableID = this.idTopicsTable

        webix.ajax(requestString, requestData, {
            success: function(result, data, XmlHttpRequest){
                result = JSON.parse(result)
                $$(tableID)["config"]["curBagId"] = result["id"]
                for (var i = 0; i < result["topic_name"].length; i++){
                    $$(tableID).add({
                        id: result["topic_name"][i],
                        topic_name: result["topic_name"][i],
                        msgs_type: result["msgs_type"][i],
                        msgs_num: result["msgs_num"][i],
                    })
                }
            },
            error: function(text, data, XmlHttpRequest){
                webix.alert("Что-то пошло не так!")
            },
        });
    }

    updateMsgsTableByRequest(requestString, requestData){
        $$(`${this.idMsgsTable}`).clearAll()
        const tableID = this.idMsgsTable
        
        webix.ajax(requestString, requestData, {
            success: function(result, data, XmlHttpRequest) {
                result = JSON.parse(result)
                $$(tableID)["config"]["curBagId"] = requestData["id"]
                $$(tableID)["config"]["curTopicName"] = requestData["topic_name"]
                
                result["msgs_list"].forEach(element => {
                    $$(tableID).add({
                        id: element['msg_name'],
                        msgs_name: element['msg_name'],
                        msgs_type: element['msg_type'],
                    })
                })
            },
            error: function(text, data, XmlHttpRequest){
                webix.alert("Что-то пошло не так!")
            },
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