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
            return "<button class='webixtype_base'>Показать сообщения</button>";
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