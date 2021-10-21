import QtQuick 2.0

Item {
    Text {
        id: text1
        x: 92
        y: 120
        text: qsTr("Text")
        font.pixelSize: 12
    }

    TextInput {
        id: textInput
        x: 92
        y: 177
        width: 80
        height: 20
        text: qsTr("Text Input")
        font.pixelSize: 12
    }

}
