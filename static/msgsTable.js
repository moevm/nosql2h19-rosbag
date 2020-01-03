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

    // Промежуточные данные запрашиваемогй части файла.
    "curBagId": null,
    "curTopicName": null,

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
            let id = $$("msgsTable")["config"]["curBagId"]
            let topic_name = $$("msgsTable")["config"]["curTopicName"]
            let cur_msg_name = cell['row']

            webix.ajax("/getMsgsByIdAndTopicNameAndMsgsName", {
                id: id,
                topic_name: topic_name,
                msg_name: cur_msg_name,
            }, function(result) {
                result = JSON.parse(result)
                $$("listOfMsgs").clearAll()
                result["msgs"].forEach(element => {
                    $$("listOfMsgs").add({msg: element})         
                });

                $$("windowShowMsgs")["config"]["curBagId"] = id;
                $$("windowShowMsgs")["config"]["curTopicName"] = topic_name;
                $$("windowShowMsgs")["config"]["curMsgsName"] = cur_msg_name;
            })
            $$("windowShowMsgs").show()
        }
    },
}