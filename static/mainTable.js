var MainTable = {
    "view": "datatable",
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
            return "<div class='webix_el_button'><button class='webixtype_base'>Показать топики</button></div>";
        }
    }, {
        id: "duration",
        "header": "Продолжительность",
        "sort": "string",
        "fillspace": true,
        "hidden": false
    }],
    "id": "mainTable",
    "select": true,
    "scrollX": false,
    "fixedRowHeight": false,
    "multiselect": false,
    "footer": false,
    "checkboxRefresh": false,
    "width": null,
    onClick: {
        webixtype_base: function(ev, id, html) {
            // webix.alert("Clicked row "+id);
            $$("tableForTopics").show();
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

    url: function() {
        $$("mainTable").clearAll()
        return webix.promise(function(res) {
            setTimeout(function() {
                res(webix.ajax("/getFaceData", function(result) {
                    result = JSON.parse(result)
                    console.log(result);
                    let i = 0
                    for (var key in result) {
                        console.log(key)
                        $$("mainTable").parse([{
                            id: i,
                            filename: result[key]["filename"],
                            creation: result[key]["date_creation"],
                            topics: result[key]["topics_list"],
                            duration: result[key]["duration"]
                        }])
                        i++
                    }

                }));
            }, 1000)
        });
    }
}