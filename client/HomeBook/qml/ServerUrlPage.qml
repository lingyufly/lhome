import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 2.12

Dialog{
    id:root
    height: 300
    width: 300
    x:parent.width/2-width/2
    y:parent.height/2-height/2

    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: Column{

        anchors.margins: 5
        spacing: 6
        Text{
            text: "请填写服务器地址:"
            width:parent.width
        }

        TextField{
            id:mServerUrlTf
            width:parent.width
            text:cSetting.getString("server/url")
        }

        Text{
            text:"请填写请求超时时长"
        }
        TextField{
            id:mTimeoutTf
            width:parent.width
            text:cSetting.getString("server/timeout")
        }
    }

    onAccepted: {
        cSetting.setValue("server/url", mServerUrlTf.text);
        cSetting.setValue("server/timeout", mTimeoutTf.text);
        cAjax.setServerUrl(mServerUrlTf.text);
        cAjax.setTimeout(Number(mTimeoutTf.text));
    }

    onRejected: {
    }

}
