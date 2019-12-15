var MsgsMenu = {
    "id": "msgsMenu",
    "view": "menu",
    "width": 163,
    "hidden": true,
    layout: "y",
    subMenuPos: "right",
    data: [{
        id: "returnToTopics",
        value: "Назад в топики..."
    }],
    on: {
        onMenuItemClick: function(id) {
            if (id == "returnToTopics") {
                tableManager.showTopicsTable()
            }
        },
    }
}