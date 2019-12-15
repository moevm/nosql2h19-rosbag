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
    }, {
        id: "stats",
        value: "Статистика",
    }, {
        id: "mainClear",
        value: "Убрать фильтры"

    }],
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

            if (id == "filterByTopics"){
                let currentIds = tableManager.getCurrentIdsFromMainTable()

                webix.ajax("/getTopicsByIds", {
                    "ids": currentIds
                }, function(result) {
                    let topics = JSON.parse(result)['topics']
                    $$("listOfTopics").clearAll()
                    topics.forEach(topic => {
                        $$("listOfTopics").add({title: topic})
                    });
                    // let minDate = new Date(result['min'])
                    // minDate.setDate(minDate.getDate() - 1)
                    // let maxDate = new Date(result['max'])
                    // maxDate.setDate(maxDate.getDate() + 1)

                    // $$("dateChooser").getPopup().getBody().define("minDate", minDate);
                    // $$("dateChooser").getPopup().getBody().define("maxDate", maxDate);

                    $$("windowFilterTopics").show()
                })
            }


            if (id == "filterByDuration"){
                let currentIds = tableManager.getCurrentIdsFromMainTable()
                webix.ajax("/getMaxMinDurationsByIds", {
                    "ids": currentIds
                }, function(result) {
                    result = JSON.parse(result)
                    let minDur = Math.round(result['min']) - 1
                    let maxDur = Math.round(result['max']) + 1

                    $$("valueSlider").define("min", minDur)
                    $$("valueSlider").define("max", maxDur)
                    $$("valueSlider").define("title", `От ${minDur} до ${maxDur}`)
                    let avg = Math.floor((maxDur - minDur) / 2)
                    $$("valueSlider").setValue(avg)
                    $$("valueOutput").setValue(avg)
                    
                    $$("windowFilterDuration").show()
                })

            }

            if (id == "stats") {
                
            }

            if (id == "mainClear"){
                // todo check this
                let my_promise = new Promise(function(resolve) {
                    setTimeout(function() {
                        resolve(tableManager.updateMainTableByRequest("/getFaceData"))
                    }, 1000)
                });
                my_promise.then(tableManager.deactivateClearMainMenuItem())
            }
        },
    }
}