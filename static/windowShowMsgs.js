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
                        value: "Сумма",
                        click: showSummaryOfMsgsArray
                    },
                    {
                        id: "btnAvg",
                        view: "button",
                        value: "Среднее",
                        click: showAverageOfMsgsArray
                    },
                    {
                        id: "btnGraph",
                        view: "button",
                        value: "График",
                        click: showGraphOfMsgsArray
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
    on: {
        onHide: () => {
            $$("windowShowMsgs")["config"]["curBagId"] = null
            $$("windowShowMsgs")["config"]["curTopicName"] = null
            $$("windowShowMsgs")["config"]["curMsgsName"] = null
        }
    }
}

function showSummaryOfMsgsArray(){
    webix.ajax("/getSummOfMsgs", {
        id: $$("windowShowMsgs")["config"]["curBagId"],
        topic_name: $$("windowShowMsgs")["config"]["curTopicName"],
        msg_name: $$("windowShowMsgs")["config"]["curMsgsName"],
    }, function(result) {
        result = JSON.parse(result)
        if (result['isValid'])
            webix.alert(`Итоговая сумма: ${result['summary']}`)
        else
            webix.alert(`Некорректный тип`)
    });
}

function showAverageOfMsgsArray(){
    webix.alert("Average")
}

function showGraphOfMsgsArray(){
    webix.alert("Graph")
}