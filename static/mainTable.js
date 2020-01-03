var MainTable = {
    "id": "mainTable",
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
        id: "filename",
        "header": "Название",
        "fillspace": true,
        "sort": "string",
        "hidden": false
    }, {
        id: "creation",
        "header": "Дата создания",
        "sort": "string",
        "fillspace": true,
        "hidden": false
    }, {
        id: "topics_list",
        "header": "Топики",
        "sort": "string",
        "fillspace": true,
        "hidden": false,
        template: function(obj) {
            return "<button class='callTopicsBtn'>Показать топики</button>";
        }
    }, {
        id: "duration",
        "header": "Продолжительность",
        "sort": "string",
        "fillspace": true,
        "hidden": false
    }],
    onClick: {
        callTopicsBtn: function(event, cell, target) {
            tableManager.showTopicsTable();
            tableManager.updateTopicsTableByRequest("/getTopicsInfoById", {
                id: cell["row"]
            });
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

    url: () => {
        return webix.promise(function(resolve) {
            setTimeout(function() {
                tableManager.updateMainTableByRequest("/getFaceData")
            }, 1000)
        });
    }
}