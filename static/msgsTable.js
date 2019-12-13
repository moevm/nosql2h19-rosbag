var MsgsTable = {
    "id": "msgsTable",
    "view": "datatable",
    "select": true,
    "scrollX": false,
    "fixedRowHeight": false,
    "multiselect": false,
    "footer": false,
    "checkboxRefresh": false,
    "width": null,
    "hidden": true,

    "columns": [{
        id: "msgs_name",
        "header": "Название",
        "fillspace": true,
        "sort": "string",
        "hidden": false,
    }, {
        id: "msgs_type",
        "header": "Тип",
        "sort": "string",
        "fillspace": true,
        "hidden": false
    }, {
        id: "msgs_list",
        "header": "Показать сообщения",
        "sort": "string",
        "fillspace": true,
        "hidden": false,
        template: function(obj) {
            return "<button class='showWindowWithListOfMsgs'>Вывести сообщения</button>";
        }
    }],
    onClick: {
        showWindowWithListOfMsgs: function(event, cell, target) {
            let data = cell["row"].split("|_|")
            let id = data[0]
            let topic_name = data[1]
            let cur_msg_name = data[2]

            webix.ajax("/getMsgsInfoByIdAndTopicName", {
                id: id,
                topic_name: topic_name,
            }, function(result) {
                result = JSON.parse(result)
                for (var key in result) { // должен быть один   
                    let msgs = result[key]["msgs_list"]["msgs_list"]
                    msgs = msgs.find((element) => {
                        if (element['msg_name'] == cur_msg_name)
                            return true
                    })
                    msgs = msgs['msgs'] 
    
                    $$("listOfMsgs").clearAll()
                    msgs.forEach(element => {
                        $$("listOfMsgs").add({msg: element})         
                    });
                }
            })
            $$("windowShowMsgs").show()
        }
    },
    on: {
        onBeforeLoad: function() {
            this.showOverlay("Loading...");
        },
        onAfterLoad: function() {
            this.hideOverlay();
        }
    },
}