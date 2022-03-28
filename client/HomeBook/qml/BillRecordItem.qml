import QtQuick 2.0
import QtQuick.Controls 2.3
Item {
    id:root
    width: parent.width
    height: 50
    property var rcd: null
    Rectangle{
        anchors.fill: parent

        Rectangle{
            id:iconrect
            anchors.left: parent.left
            anchors.leftMargin: 4
            anchors.verticalCenter: parent.verticalCenter
            height: 35
            width: 35
            radius: 100
            clip: true
            color: "yellow"
            Image {
                anchors.fill: parent
                anchors.centerIn: parent.Center
                source: "qrc:/assets/type/traffic.png"
            }
        }

        Rectangle{
            anchors.top:parent.top
            anchors.topMargin: 3
            anchors.left: iconrect.right
            anchors.leftMargin: 3

            Column{
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.topMargin: 10
                anchors.leftMargin: 10
                spacing:5
                Row{
                    spacing: 5

                    Text {
                        id: categoryText
                        font.pointSize: 12
                        font.weight: Font.Bold
                        text: "出行"
                    }
                    Text {
                        id: typeText
                        font.pointSize: 10
                        text: "公交"
                    }
                    Text {
                        id: dateText
                        text: "03/11"
                    }
                }

                Row{
                    spacing: 5
                    Text {
                        id: userText
                        font.pointSize: 10
                        text: "凌宇"
                    }
                    Text {
                        id: commentText
                        font.pointSize: 10
                        text: ""
                    }
                }
            }
        }
    }

    Text{
        id:countText
        anchors.right: parent.right
        anchors.rightMargin: 4
        verticalAlignment: Text.AlignVCenter
        height: parent.height
        //width:  parent.height
        text: "1.01"
        font.pointSize: 15
        font.weight: Font.Bold
    }
}
