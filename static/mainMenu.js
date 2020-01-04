var MainMenu = {
    "id": "mainMenu",
    "view": "menu",
    "width": 163,
    "hidden": true,
    layout: "y",
    subMenuPos: "right",
    data: [{
        id: "chooseUpload",
        value: "Загрузить файлы..."
    }, {
        id: "chooseDownload",
        value: "Выгрузить файлы..."
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
            
            if (id == "chooseDownload"){
                webix.ajax("/getFilesNumber", {
                    success: function(result) {
                        result = JSON.parse(result)
                        $$("labelDownloadWindow").setValue(`Количество файлов для загрузки: ${result['result']}.`)
                        $$("windowDownload").show()
                    },
                    error: function(text, data, XmlHttpRequest){
                        webix.alert("Что-то пошло не так!")
                    }
                })
            }

            if (id == "filterByDate") {
                let currentIds = tableManager.getCurrentIdsFromMainTable()
                
                webix.ajax("/getMaxMinDatesByIds", {
                    "ids": currentIds
                }, {
                    success: function(result) {
                        result = JSON.parse(result)
                        let minDate = new Date(result['min'])
                        minDate.setDate(minDate.getDate() - 1)
                        let maxDate = new Date(result['max'])
                        maxDate.setDate(maxDate.getDate() + 1)

                        $$("dateChooser").getPopup().getBody().define("minDate", minDate);
                        $$("dateChooser").getPopup().getBody().define("maxDate", maxDate);

                        $$("windowFilterDate").show()
                    },
                    error: function(text, data, XmlHttpRequest){
                        webix.alert("Что-то пошло не так!")
                    }
                })
            }

            if (id == "filterByTopics"){
                let currentIds = tableManager.getCurrentIdsFromMainTable()

                webix.ajax("/getTopicNamesForIds", {
                    "ids": currentIds
                }, {
                    success: function(result) {
                        let topicNames = JSON.parse(result)
                        $$("listOfTopics").clearAll()
                        topicNames.forEach(topicName => {
                            $$("listOfTopics").add({title: topicName})
                        });

                        $$("windowFilterTopics").show()
                    },
                    error: function(text, data, XmlHttpRequest){
                        webix.alert("Что-то пошло не так!")
                    }
                })
            }


            if (id == "filterByDuration"){
                let currentIds = tableManager.getCurrentIdsFromMainTable()
                webix.ajax("/getMaxMinDurationsByIds", {
                    "ids": currentIds
                }, {
                    success: function(result) {
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
                    },
                    error: function(text, data, XmlHttpRequest){
                        webix.alert("Что-то пошло не так!")
                    }
                })
            }

            if (id == "stats") {
                
            }

            if (id == "mainClear"){
                // todo check this
                let my_promise = new Promise(function(resolve) {
                    setTimeout(function() {
                        resolve(tableManager.updateMainTableByRequest("/getBagInfo"))
                    }, 1000)
                });
                my_promise.then(tableManager.deactivateClearMainMenuItem())
            }
        },
    }
}