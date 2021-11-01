import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 2.12

Rectangle{
    id:root
    height: 300
    width: 300
    x:parent.width/2-width/2
    y:parent.height/2-height/2


    Column{
        anchors.fill: parent
        spacing: 6
        anchors.margins: 5
        Text{
            text: "请填写服务器地址"
            width:parent.width
        }

        TextField{
            id:mServerUrlTf
            width:parent.width
            text:cSetting.value("server/url").toString()
        }

        Row{
            width: parent.width
            height: mServerUrlTf.height
            spacing: 6
            Button{
                id:mAccpetBtn
                text:"确定"
                onClicked: {
                    cSetting.setValue("server/url", mServerUrlTf.text);
                    cAjax.setServerUrl(mServerUrlTf.text);
                    root.destroy();
                }
            }
            Button{
                id:mRejectBtn
                anchors.right: parent.right
                text:"取消"
                onClicked: {
                    root.destroy();
                }
            }
        }
    }

}
