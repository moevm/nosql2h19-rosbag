var TopicsMenu = {
    "id": "topicsMenu",
    "view": "menu",
    "width": 163,
    "hidden": true,
    layout: "y",
    subMenuPos: "right",
    data: [{
        id: "returnToFiles",
        value: "Назад..."
    }, {
        id: "filter",
        value: "Отфильтровать по...",
        submenu: [{
            id: "filterByDate",
            value: "Дате"
        }, {
            id: "filterByTopics",
            value: "Топикам"
        }, {
            id: "filterBySize",
            value: "Размеру"
        }]
    },{
        id: "stats",
        value: "Статистика"
    }],
    on: {
        onMenuItemClick: function(id) {
            if (id == "returnToFiles") {
                tableManager.showMainTable()
            }

            if (id == "filterByDate") {
                $$("windowFilterDate").show()
            }
            if (id == "filterBySize"){
                $$("windowFilterDuration").show()
            }

            if (id == "stats") {
                // $$("mainTable").hide()
                // $$("mainTable_2").show()
                // webix.ajax("/getStats", function(result) {
                //     result = JSON.parse(result)
                //     let text = ""
                //     for (var id in result) {
                //         text = text + result[id]["sum"] + "\n"
                //     }
                //     webix.alert({
                //         title: "Сумма значений топика quaternionTopic сообщений X",
                //         width: 400,
                //         text: text
                //     });
                // })
            }
        },
    }
}