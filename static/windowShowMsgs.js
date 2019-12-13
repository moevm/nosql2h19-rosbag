var WindowShowMsgs = {
    id: "windowShowMsgs",
    view: 'window',
    head: 'Список сообщений',
    modal: true,
    width: 400,
    height: 500,
    resize: true,
    position: 'center',
    close: true,
    move: true,
    body: {
        view: 'form',
        rows: [{
                id: "listOfMsgs",
                view: "list",
                template: "#msg#",
                select: false,
                scroll: true,
            },
        ]
    },
}