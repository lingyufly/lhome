import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.5

import "../js/ajax.js" as Ajax

Window {
    width: 400
    height: 700
    visible: true
    title: qsTr("家庭账本")

    ToastManager{
        id:mToast
    }

    LoginPage{
        anchors.fill: parent
    }


}
