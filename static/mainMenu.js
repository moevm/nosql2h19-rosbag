var MainMenu = {
    "id": "mainMenu",
    "view": "menu",
    "width": 163,
    "hidden": true,
    layout: "y",
    subMenuPos: "right",
    data: [{
        id: "chooseUpload",
        value: "Добавить..."
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
    }], // TODO добавить кнопку сбросить
    on: {
        onMenuItemClick: function(id) {
            if (id == "chooseUpload") {
                $$("windowUpload").show()
            }

            if (id == "filterByDate") {
                let currentIds = tableManager.getCurrentIdsFromMainTable()
                console.log(currentIds)
                
                webix.ajax("/getMaxMinDatesByIds", {
                    "ids": currentIds
                }, function(result) {
                    result = JSON.parse(result)
                    console.log(result)
                    
                })
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