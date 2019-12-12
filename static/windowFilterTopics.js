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
                data:[
                  { id:1, title:"Item 1"},
                  { id:2, title:"Item 2"},
                  { id:3, title:"Item 3"}
                ]
            },
            {
                view: "button",
                label: "Отфильтровать",
                click: function() {
                    // selectedDate = $$("dateChooser").getValue();
                    // selectedDirID = $$("dirDateChooser").getValue();
                    // console.log(selectedDate, selectedDirID)

                    // if (selectedDate == null){
                    //     webix.alert("Вы не выбрали дату!")
                    //     return
                    // }
                    // tableManager.updateMainTableByRequest("/getFilterData", {
                    //     ids: tableManager.getCurrentIdsFromMainTable(),
                    //     filterItem: "date",
                    //     date: selectedDate,
                    //     dir: convertIDtoDir(selectedDirID)
                    // });
                    tableManager.activateClearMainMenuItem()
                    this.getParentView().getParentView().hide()
                }
            }
        ]
    },
}

function convertIDtoDir(id){
    if (id == 0)
        return "exactly"
    if (id == 1)
        return "more"
    if (id == 2)
        return "less"
    console.assert("Error id dir")
}