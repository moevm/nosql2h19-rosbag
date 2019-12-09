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
                    selectedDuration = $$("dateChooser").getValue();
                    console.log(selectedDuration)

                    tableManager.updateMainTableByRequest("/getFilterData", {
                        filterItem: "duration",
                        duration: selectedDuration,
                    });
                    this.getParentView().getParentView().hide()
                }
            }
        ]
    },
}