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
                    date = $$("dateChooser").getValue();
                    dir = $$("dirChooser").getValue();
                    console.log(date, dir)
                    this.getParentView().getParentView().hide()
                }
            }
        ]
    },
    move: true,
    on: {
        onHide: function() {
            updateMainTable("mainTable", "/getFilterData", {
                filterItem: "data",
                dir: "less"
            });
        }
    }
}