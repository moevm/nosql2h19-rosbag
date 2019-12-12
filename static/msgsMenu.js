var MsgsMenu = {
    "id": "msgsMenu",
    "view": "menu",
    "width": 163,
    "hidden": true,
    layout: "y",
    subMenuPos: "right",
    data: [{
        id: "returnToTopics",
        value: "Назад..."
    }, {
        id: "filter",
        value: "Сообщения!",
        submenu: [{
            id: "filterByTopicNames",
            value: "Топикам"
        }, {
            id: "filterByMsgsType",
            value: "Типу сообщений"
        }, {
            id: "filterByMsgsNum",
            value: "Количеству сообщений"
        }]
    }, {
        id: "topicsClear",
        value: "Убрать фильтры"

    }],
    on: {
        onMenuItemClick: function(id) {
            if (id == "returnToTopics") {
                tableManager.showTopicsTable()
            }

            if (id == "filterByTopicNames") {
                // $$("windowFilterDate").show()
                // tableManager.activateClearTopicsMenuItem()
            }
            if (id == "filterByMsgsType"){

                // tableManager.activateClearTopicsMenuItem()
            }
            if (id == "filterByMsgsNum"){

                // tableManager.activateClearTopicsMenuItem()
            }


            if (id == "topicsClear"){
                // load face topic data
                // tableManager.deactivateClearTopicsMenuItem()
            }

        },
    }
}