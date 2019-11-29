var WindowUpload = {
    id: "windowUpload",
    view: 'window',
    head: 'Загрузка новых файлов',
    modal: true,
    width: 600,
    height: 500,
    resize: true,
    position: 'center',
    body: {
        view: 'form',
        rows: [{
                view: "uploader",
                value: "Загрузить",
                name: "files",
                link: "uploadedFilesList",
                upload: "/uploadBags"
            },
            {
                view: "list",
                id: "uploadedFilesList",
                type: "uploader",
                autoheight: true,
                borderless: true
            },
            {
                view: "button",
                label: "Закрыть",
                click: function() {
                    this.getParentView().getParentView().hide()
                }
            }
        ]
    },
    move: true,
    on: {
        onHide: function(){
            $$("uploadedFilesList").clearAll()
        }

    }
};