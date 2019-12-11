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
            id: "filterByDuration",
            value: "Времени записи"
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
                
                webix.ajax("/getMaxMinDatesByIds", {
                    "ids": currentIds
                }, function(result) {
                    result = JSON.parse(result)
                    let minDate = new Date(result['min'])
                    minDate.setDate(minDate.getDate() - 1)
                    let maxDate = new Date(result['max'])
                    maxDate.setDate(maxDate.getDate() + 1)

                    $$("dateChooser").getPopup().getBody().define("minDate", minDate);
                    $$("dateChooser").getPopup().getBody().define("maxDate", maxDate);

                    $$("windowFilterDate").show()
                })
            }
            if (id == "filterByDuration"){
                let currentIds = tableManager.getCurrentIdsFromMainTable()
                webix.ajax("/getMaxMinDurationsByIds", {
                    "ids": currentIds
                }, function(result) {
                    result = JSON.parse(result)
                    console.log(result)
                    let minDur = Math.round(result['min']) - 1
                    let maxDur = Math.round(result['max']) + 1
                    console.log(minDur, maxDur)

                    $$("valueSlider").define("min", minDur)
                    $$("valueSlider").define("max", maxDur)
                    let avg = Math.floor((maxDur - minDur) / 2)
                    $$("valueSlider").setValue(avg)
                    $$("valueOutput").setValue(avg)
                    
                    $$("windowFilterDuration").show()
                })

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