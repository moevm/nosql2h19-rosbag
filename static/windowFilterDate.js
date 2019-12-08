var WindowFilterDate = {
    id: "windowFilterDate",
    view: 'window',
    head: 'Параметры фильтрации по дате',
    modal: true,
    width: 400,
    height: 500,
    resize: true,
    position: 'center',
    close: true,
    body: {
        view: 'form',
        rows: [{
                view: "datepicker",
                id: "dateChooser",
                stringResult: true,
                timepicker: false,
                label: "Основная дата:",
                labelWidth: 170
            },
            {
                id: "dirChooser",
                view: "select",
                label: "Направление поиска:",
                labelWidth: 170,
                options: [{
                    value: "Ровно",
                    id: 0
                }, {
                    value: "Позже",
                    id: 1
                }, {
                    value: "Раньше",
                    id: 2
                }]
            },
            {
                view: "button",
                label: "Отфильтровать",
                click: function() {
                    selectedDate = $$("dateChooser").getValue();
                    selectedDirID = $$("dirChooser").getValue();
                    console.log(selectedDate, selectedDirID)

                    if (selectedDate == null){
                        webix.alert("Вы не выбрали дату!")
                        return
                    }
                    updateMainTableByRequest("mainTable", "/getFilterData", {
                        filterItem: "date",
                        date: selectedDate,
                        dir: convertIDtoDir(selectedDirID)
                    });
                    this.getParentView().getParentView().hide()
                }
            }
        ]
    },
    move: true,
    on: {
        // onHide: function() {
        //     updateMainTableByRequest("mainTable", "/getFilterData", {
        //         filterItem: "data",
        //         dir: "less"
        //     });
        // }
    }
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