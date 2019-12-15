var TopicsMenu = {
    id: "topicsMenu",
    view: "menu",
    width: 163,
    hidden: true,
    layout: "y",
    subMenuPos: "right",
    data: [{
        id: "returnToFiles",
        value: "Назад в файлы..."
    },],
    on: {
        onMenuItemClick: function(id) {
            if (id == "returnToFiles"){
                tableManager.showMainTable()
            }
        },
    }
}