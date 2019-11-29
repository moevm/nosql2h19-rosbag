var TopicsTable = {
    id: "topicsTable",
    view: 'window',
    head: 'Топики файла',
    modal: true,
    width: 1000,
    height: 500,
    resize: true,
    position: 'center',
    body: {
        view: 'form',
        elements: [{
                "view": "datatable",
                "columns": [{
                    id: "topic_name",
                    "header": "Название",
                    "fillspace": true,
                    "sort": "string",
                    "hidden": false
                }, {
                    id: "msgs_type",
                    "header": "Тип сообщения",
                    "sort": "string",
                    "fillspace": true,
                    "hidden": false
                }, {
                    id: "msgs_num",
                    "header": "Топики",
                    "sort": "string",
                    "fillspace": true,
                    "hidden": false,
                }, {
                    id: "msgs_list",
                    "header": "Сообщения",
                    "sort": "string",
                    "fillspace": true,
                    "hidden": false,
                    // template:function(obj){ 
                    //     return "<div class='webix_el_button'><button class='webixtype_base'>Показать топики</button></div>";
                    // }
                }],
                "id": "topics",
                "select": true,
                "scrollX": false,
                "fixedRowHeight": false,
                "multiselect": false,
                "footer": false,
                "checkboxRefresh": false,
                "width": null,
                // onClick:{
                //     webixtype_base: function(ev, id, html){
                //         // webix.alert("Clicked row "+id);
                //         // myWin.show();
                //         // $$('login').focus();
                //     }
                // },
                // on: {
                //     onBeforeLoad: function() {
                //         this.showOverlay("Loading...");
                //     },
                //     onAfterLoad: function() {
                //         this.hideOverlay();
                //     }
                // },

                // url: function() {
                //     return webix.promise(function(res) {
                //         setTimeout(function() {
                //             res(webix.ajax("/getFaceData", function(result) {
                //                 result = JSON.parse(result)
                //                 let i = 0
                //                 for (var key in result) {
                //                     // check if the property/key is defined in the object itself, not in parent
                //                     // console.log(result[key]["topics_list"]) 
                //                     console.log("load daa for table")
                //                     $$("topicsTable").parse([{
                //                         id: i,
                //                         topic_name:   result[key]["filename"],
                //                         msgs_type:   result[key]["date_creation"],
                //                         msgs_num:   result[key]["topics_list"]
                //                     }])
                //                     i++
                //                 }

                //             }));
                //         }, 1000)
                //     });
                // }
            },
            {
                view: 'button',
                value: 'Close',
                click: function(elementId, event) {
                    this.getParentView().getParentView().hide();
                }
            }
        ]
    },
    move: true
};