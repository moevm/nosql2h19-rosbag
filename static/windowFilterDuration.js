var WindowFilterDuration = {
    id: "windowFilterDuration",
    view: 'window',
    head: 'Параметры фильтрации по длительности',
    modal: true,
    width: 500,
    height: 500,
    resize: true,
    position: 'center',
    close: true,
    move: true,
    body: {
        view: 'form',
        rows: [
            {
                id: "valueOutput",
                view: "text",
                value: '80',
                label: "Длительность:",
                labelWidth: 120,
                width: 400,
                attributes: {
                    type:"number"
                },
                on: {
                    onChange(oldValue, newValue){
                        $$("valueSlider").setValue(this.getValue())
                        this.refresh();
                    },
                }
            },
            {
                id: "dirDurationChooser",
                view: "select",
                label: "Направление:",
                labelWidth: 120,
                options: [{
                    value: "Ровно",
                    id: 0
                }, {
                    value: "Более чем",
                    id: 1
                }, {
                    value: "Менее чем",
                    id: 2
                }]
            },
            {
                id: "valueSlider",
                view: "slider",
                align: "center",
                width: 400,
                value: "80",
                title: "Initial state",
                moveTitle: false,
                on: {
                    onChange: function() {
                        $$("valueOutput").setValue(this.getValue())
                        this.refresh();
                    },
                }
            },
            {
                view: "button",
                label: "Отфильтровать",
                click: function() {
                    selectedDuration = $$("valueOutput").getValue();
                    selectedDirID = $$("dirDurationChooser").getValue()

                    tableManager.updateMainTableByRequest("/getFilterData", {
                        ids: tableManager.getCurrentIdsFromMainTable(),
                        filterItem: "duration",
                        duration: selectedDuration,
                        dir: convertIDtoDir(selectedDirID)
                    });
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