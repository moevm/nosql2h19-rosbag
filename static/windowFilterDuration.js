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
                value: '0',
                label: "Длительность",
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
                        // this.define("title", "Final value " + this.getValue());
                        this.refresh();
                    },
                }
            },
            {
                view: "button",
                label: "Отфильтровать",
                click: function() {
                    console.log("Filter by duration!")
                    // selectedDate = $$("dateChooser").getValue();
                    // selectedDirID = $$("dirChooser").getValue();
                    // console.log(selectedDate, selectedDirID)

                    // if (selectedDate == null){
                    //     webix.alert("Вы не выбрали дату!")
                    //     return
                    // }
                    // updateMainTableByRequest("mainTable", "/getFilterData", {
                    //     filterItem: "date",
                    //     date: selectedDate,
                    //     dir: convertIDtoDir(selectedDirID)
                    // });
                    this.getParentView().getParentView().hide()
                }
            }
        ]
    },
}