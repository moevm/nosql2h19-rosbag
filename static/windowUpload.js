var WindowUpload = {
    id: "windowUpload",
    view: 'window',
    head: 'Загрузка новых файлов',
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
                view: "uploader",
                value: "Загрузить",
                name: "files",
                link: "uploadedFilesList",
                upload: "/load/upload",
                on: {
                    onUploadComplete: function(){
                        // TODO update data table after uploading complete
                        // $$("mainTable").refresh()
                    }
                }
            }, {
                view: "list",
                id: "uploadedFilesList",
                type: "uploader",
                autoheight: true,
                borderless: true
            }, {
                view: "button",
                label: "Закрыть",
                click: function() {
                    this.getParentView().getParentView().hide()
                }
            }
        ]
    },
    on: {
        onHide: function(){
            $$("uploadedFilesList").clearAll()
        }
    }
};