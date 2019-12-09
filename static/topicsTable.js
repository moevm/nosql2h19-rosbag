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
        id: "filename",
        "header": "Пидорас",
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
            return "<div class='webix_el_button'><button class='webixtype_base'>Показать топики</button></div>";
        }
    }, {
        id: "duration",
        "header": "Продолжительность",
        "sort": "string",
        "fillspace": true,
        "hidden": false
    }],
    onClick: {
        webixtype_base: function(ev, id, html) {
            // webix.alert("Clicked row "+id);
            $$("topicsTable").show();
            // $$('login').focus();
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

    // url: () => {
    //     return webix.promise(function(resolve) {
    //         setTimeout(function() {
    //             updateMainTableByRequest("mainTable", "/getFaceData")
    //         }, 1000)
    //     });
    // }
}