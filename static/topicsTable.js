var TopicsTable = {
    "id": "topicsTable",
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

    "columns": [{
        id: "topic_name",
        "header": "Название топика",
        "fillspace": true,
        "sort": "string",
        "hidden": false,
    }, {
        id: "msgs_type",
        "header": "Типы сообщений",
        "sort": "string",
        "fillspace": true,
        "hidden": false
    }, {
        id: "msgs_num",
        "header": "Количество сообщений",
        "sort": "string",
        "fillspace": true,
        "hidden": false,
    }, {
        id: "msgs_list",
        "header": "Список сообщений",
        "sort": "string",
        "fillspace": true,
        "hidden": false,
        template: function(obj) {
            return "<button class='callMsgsBtn'>Показать сообщения!</button>";
        },
    }],
    onClick: {
        callMsgsBtn: function(event, cell, target) {
            let id = $$("topicsTable")["config"]["curBagId"]
            let topic_name = cell["row"]
            tableManager.updateMsgsTableByRequest("/getMsgsInfoByIdAndTopicName", {
                id: id,
                topic_name: topic_name
            });
            tableManager.showMsgsTable()
        }
    },
}