import QtQuick 2.0
import QtQuick.Controls 2.3

Item {
    id:root

    ListModel{
        id:listmodel
    }

    // 顶部部分
    Rectangle{
        id: toper
        height: 150
        width: parent.width
        color: "red"
        z:1000

        Item {
            id: top_1
            width: parent.width
            height: 50
            Button {
                width: 32
                height: 32
                anchors.left: parent.left
                anchors.leftMargin: 20
                flat: true
                Image {
                    anchors.fill: parent
                    source: "qrc:/assets/percent.png"
                }
            }

            Button {
                width: 32
                height: 32
                anchors.right: parent.right
                anchors.rightMargin: 20
                flat: true
                Image {
                    anchors.fill: parent
                    source: "qrc:/assets/rili/rili00.png"
                }
            }
        }

        // 结余
        Item{
            id: top_2
            anchors.top: top_1.bottom
            anchors.left: parent.left
            width: parent.width
            height: 50
            Column{
                width: parent.width
                Label{
                    text: "11522.73"
                    color: "white"
                    width: parent.width
                    font.weight: Font.Bold
                    horizontalAlignment: Text.AlignHCenter
                    font.pointSize: 30
                }
                Label{
                    color: "white"
                    width: parent.width
                    font.weight: Font.Bold
                    horizontalAlignment: Text.AlignHCenter
                    text: "三月结余"
                }
            }
        }

        // 收入和支出
        Item{
            id: top_3
            anchors.top: top_2.bottom
            anchors.left: parent.left
            width: parent.width
            height: 50

            // 收入
            Rectangle{
                anchors.top: parent.top
                anchors.left: parent.left
                width: parent.width/2
                Column{
                    width: parent.width
                    Label{
                        text: "18408.34"
                        color: "white"
                        width: parent.width
                        font.weight: Font.Bold
                        horizontalAlignment: Text.AlignHCenter
                        font.pointSize: 20
                    }
                    Label{
                        color: "white"
                        width: parent.width
                        font.weight: Font.Bold
                        horizontalAlignment: Text.AlignHCenter
                        text: "三月收入"
                    }
                }
            }

            // 支出
            Rectangle{
                anchors.top: parent.top
                anchors.right: parent.right
                width: parent.width/2

                Column{
                    width: parent.width
                    Label{
                        text: "6885.61"
                        color: "white"
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        font.pointSize: 20
                        font.weight: Font.Bold
                    }
                    Label{
                        color: "white"
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        text: "三月支出"
                        font.weight: Font.Bold
                    }
                }
            }
        }
    }

    // 账本部分
    Rectangle{
        id: conter
        anchors.top: toper.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        color: "#f6f6f6"

        ListView{
            id:listview
            anchors.fill:parent
            model:listmodel
            spacing: 1
            delegate: BillRecordItem{
                height: 50
                width: parent.width
                rcd: listmodel.get(index)
            }
        }
    }

    Component.onCompleted: {
        listmodel.append({name:"x1"})
        listmodel.append({name:"x2"})
        listmodel.append({name:"x3"})
        listmodel.append({name:"x4"})
        listmodel.append({name:"x5"})
        listmodel.append({name:"x6"})
    }
}
