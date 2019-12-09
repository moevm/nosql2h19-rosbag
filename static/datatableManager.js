class datatableManager {
    constructor(idMainTable, idTopicsTable){
        this.idMainTable = idMainTable
        this.idTopicsTable = idTopicsTable
        this.activeTable = idMainTable
    }

    showMainTable(){
        $$(`${this.activeTable}`).hide()
        $$(`${this.idMainTable}`).show()
        this.activeTable = this.idMainTable
    }

    showTopicsTable(){
        $$(`${this.activeTable}`).hide()
        $$(`${this.idTopicsTable}`).show()
        this.activeTable = this.idTopicsTable
    }
    
}