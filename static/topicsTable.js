var TopicsTable = {
    "view": "datatable",
    "id": "topicsTable",
    "select": true,
    "scrollX": false,
    "fixedRowHeight": false,
    "multiselect": false,
    "footer": false,
    "checkboxRefresh": false,
    "width": null,
    "hidden": true,

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
            let data = cell["row"].split("|_|")
            let id = data[0]
            let topic_name = data[1]
            tableManager.updateMsgsTableByRequest("/getMsgsInfoByIdAndTopicName", {
                id: id,
                topic_name: topic_name
            });
            tableManager.showMsgsTable()
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