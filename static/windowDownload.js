var WindowDownload = {
    id: "windowDownload",
    view: 'window',
    head: 'Выгрузка файлов',
    modal: true,
    width: 400,
    height: 500,
    resize: true,
    position: 'center',
    move: true,
    close: true,
    body: {
        view: 'form',
        rows: [{
                id: "labelDownloadWindow", 
                view:"label", 
                label: "if you see it - it`s error", 
                align: "left"
            }, {
                view: "button",
                label: "Загрузить файлы",
                click: function() {
                    webix.ajax().response("blob").get("/load/download", function(text, data){
                        webix.html.download(data, "patch.zip");
                    });
                    this.getParentView().getParentView().hide()
                }
            }
        ]
    }
};