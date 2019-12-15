var WindowFilterTopics = {
    id: "windowFilterTopics",
    view: 'window',
    head: 'Список топиков для фильтрации',
    modal: true,
    width: 400,
    height: 500,
    resize: true,
    position: 'center',
    close: true,
    move: true,
    body: {
        view: 'form',
        rows: [
            {
                id: "listOfTopics",
                view: "list",
                template: "#title#",
                select: true,
                multiselect: true,
                multiselect: "touch",
                scroll: false
            },
            {
                view: "button",
                label: "Отфильтровать",
                click: function() {
                    let topics = $$("listOfTopics").getSelectedItem()
                    if (topics == undefined){
                        webix.alert("Вы не выбрали ни одного топика!")
                        return;
                    }

                    if (!Array.isArray(topics))
                        topics = [topics]
                    topics = topics.map((id) => {
                        return id['title']
                    })

                    tableManager.updateMainTableByRequest("/getFilterData", {
                        ids: tableManager.getCurrentIdsFromMainTable(),
                        filterItem: "topics",
                        topics: topics
                    });
                    tableManager.activateClearMainMenuItem()
                    this.getParentView().getParentView().hide()
                }
            }
        ]
    },
}