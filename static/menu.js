var Menu = {
    "view": "menu",
    "width": 163,
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
    }, {
        id: "3",
        value: "Фильтр 7.11 less",
    }, {
        id: "4",
        value: "Статистика"
    }],
    on: {
        onMenuItemClick: function(id) {
            if (id == "chooseUpload") {
                $$("windowUpload").show()
            }

            if (id == "filterByDate") {
                $$("windowFilterDate").show()
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