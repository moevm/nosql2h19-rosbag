var Menu = {
    "view": "menu",
    "width": 163,
    layout: "y",
    subMenuPos: "right",
    data: [{
        id: "chooseUpload",
        value: "Добавить..."
    }, {
        id: "2",
        value: "Фильтр 7.11 more",
        submenu: [{
            id: "1_1",
            value: "Дата"
        }, {
            id: "1_2",
            value: "Теги"
        }, {
            id: "1_3",
            value: "Размер"
        }, {
            id: "1_4",
            value: "Дата"
        }, ]
    }, {
        id: "3",
        value: "Фильтр 7.11 less",
        // submenu: ["About", "Help"]
    }, {
        id: "4",
        value: "Статистика"
    }],
    on: {
        onMenuItemClick: function(id) {
            if (id == "2") {
                webix.alert("Данные отфильтрованы по датам более поздним чем 7 ноября");
                $$("mainTable").clearAll()
                webix.ajax("/getFilterData", {
                    filterItem: "data",
                    dir: "more"
                }, function(result) {
                    result = JSON.parse(result)
                    let i = 0
                    for (var key in result) {
                        // check if the property/key is defined in the object itself, not in parent
                        console.log(result[key]["topics_list"])
                        $$("mainTable").parse([{
                            id: i,
                            filename: result[key]["filename"],
                            creation: result[key]["date_creation"],
                            topics: result[key]["topics_list"],
                            duration: result[key]["duration"]
                        }])
                        i++
                    }

                })
            }
            if (id == "3") {
                webix.alert("Данные отфильтрованы по датам более ранним чем 7 ноября");
                $$("mainTable").clearAll()
                webix.ajax("/getFilterData", {
                    filterItem: "data",
                    dir: "less"
                }, function(result) {
                    result = JSON.parse(result)
                    let i = 0
                    for (var key in result) {
                        // check if the property/key is defined in the object itself, not in parent
                        console.log(result[key]["topics_list"])
                        $$("mainTable").parse([{
                            id: i,
                            filename: result[key]["filename"],
                            creation: result[key]["date_creation"],
                            topics: result[key]["topics_list"],
                            duration: result[key]["duration"]
                        }])
                        i++
                    }

                })
            }

            if (id == "chooseUpload") {
                // webix.alert("Данные добавлены");
                // $$("mainTable").clearAll()
                $$("windowUpload").show()
                // webix.ajax("/addData", function(result) {
                //     result = JSON.parse(result)
                //     let i = 0
                //     for (var key in result) {
                //         // check if the property/key is defined in the object itself, not in parent
                //         console.log(result[key]["topics_list"])
                //         $$("mainTable").parse([{
                //             id: i,
                //             filename: result[key]["filename"],
                //             creation: result[key]["date_creation"],
                //             topics: result[key]["topics_list"],
                //             duration: result[key]["duration"]
                //         }])
                //         i++
                //     }

                // })
            }
            if (id == "4") {
                // $$("mainTable").clearAll()
                webix.ajax("/getStats", function(result) {
                    result = JSON.parse(result)
                    let text = ""
                    for (var id in result) {
                        text = text + result[id]["sum"] + "\n"
                    }
                    webix.alert({
                        title: "Сумма значений топика quaternionTopic сообщений X",
                        width: 400,
                        text: text
                    });

                })
            }
        },
    }
}