var WindowShowMsgs = {
    id: "windowShowMsgs",
    curBagId: "null",
    curTopicName: "null",
    curMsgsName: "null",
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
                view:"toolbar",
                cols:[
                    {
                        id: "btnSumm",
                        view: "button",
                        value: "Сумма"
                    },
                    {
                        id: "btnAvg",
                        view: "button",
                        value: "Среднее"
                    },
                    {
                        id: "btnGraph",
                        view: "button",
                        value: "График"
                    },
                ]
            },
            {
                id: "listOfMsgs",
                view: "list",
                template: "#msg#",
                select: false,
                scroll: true,
            },
        ]
    },
}