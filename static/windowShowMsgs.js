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

    curBagId: "null",
    curTopicName: "null",
    curMsgsName: "null",
    
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
    }, {
        success: function(result) {
            result = JSON.parse(result)
            if (result['isValid'])
                webix.alert(`Итоговая сумма: ${result['summary']}`)
            else
                webix.alert(`Некорректный тип для суммы`)
        },
        error: function(text, data, XmlHttpRequest){
            webix.alert("Что-то пошло не так!")
        }
    })
}

function showAverageOfMsgsArray(){
    webix.ajax("/getAvgOfMsgs", {
        id: $$("windowShowMsgs")["config"]["curBagId"],
        topic_name: $$("windowShowMsgs")["config"]["curTopicName"],
        msg_name: $$("windowShowMsgs")["config"]["curMsgsName"],
    }, {
        success: function(result) {
            result = JSON.parse(result)
            if (result['isValid'])
                webix.alert(`Итоговое среднее: ${result['average']}`)
            else
                webix.alert(`Некорректный тип для среднего`)
        },
        error: function(text, data, XmlHttpRequest){
            webix.alert("Что-то пошло не так!")
        }
    })
}

function showGraphOfMsgsArray(){
    // Осторожно! Костыль!
    webix.ajax("/getGraph", {
        id: $$("windowShowMsgs")["config"]["curBagId"],
        topic_name: $$("windowShowMsgs")["config"]["curTopicName"],
        msg_name: $$("windowShowMsgs")["config"]["curMsgsName"],
    }, {
        success: function(text, data, xhr) {
            // Возможно можно запихать data в img srs через base64..
            if (xhr.getResponseHeader('isNumeric') == "True"){
                let src = "/getGraph" + `?id=${$$("windowShowMsgs")["config"]["curBagId"]}`
                                    + `&topic_name=${$$("windowShowMsgs")["config"]["curTopicName"]}`
                                    + `&msg_name=${$$("windowShowMsgs")["config"]["curMsgsName"]}`
                webix.alert({text:`<img src=${src} alt="Graph" width="600" height="400"`, width:"630px", height:"480px"})
            }
            else
                webix.alert(`Некорректный тип для графика`)
        },
        error: function(text, data, XmlHttpRequest){
            webix.alert("Что-то пошло не так!")
        }
    });
    
}