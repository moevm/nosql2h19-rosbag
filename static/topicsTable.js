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
        id: "topicname",
        "header": "Название топика",
        "fillspace": true,
        "sort": "string",
        "hidden": false
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
            return "<div class='webix_el_button'><button class='webixtype_base'>Показать сообщения</button></div>";
        }
    }],
    on: {
        onBeforeLoad: function() {
            this.showOverlay("Loading...");
        },
        onAfterLoad: function() {
            this.hideOverlay();
        }
    },
}