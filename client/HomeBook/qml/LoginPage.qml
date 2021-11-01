import QtQuick 2.0
import QtQuick.Controls 2.12

import "../js/ajax.js" as Ajax

Rectangle {
    id:root
    anchors.centerIn: parent
    color: "gray"
    Column{
        id:column
        anchors.centerIn: parent
        spacing: 5
        width: parent.width*0.7
        TextField{
            id: mUserNameTf
            width: parent.width
        }
        TextField{
            id:mPassWordTf
            width: parent.width
        }

        Rectangle{
            width: parent.width
            height:mPassWordTf.height
            CheckBox{
                text:"记住密码"
            }
            Button{
                text:"忘记密码"
                anchors.right:parent.right
            }
        }

        Rectangle{
            width: parent.width
            height:mPassWordTf.height
            Button{
                id:mSighnInBtn
                text:"注册"
                onClicked: {
                    Qt.createComponent("RegistryPage.qml").createObject(root)
                }
            }
            Button{
                id:mLoginBtn
                anchors.right:parent.right
                text:"登录"
                onClicked: {
                    var unm=mUserNameTf.text
                    var pwd=mPassWordTf.text
                    Ajax.post("/auth/login",
                              {"username":unm, "password":pwd},
                              function(res){
                                  mToast.show("错误:"+res.msg);
                              },
                              function(res){
                                  mToast.show("错误:"+res.msg);
                              });
                }
            }
        }

        Button{
            width: parent.width
            text:"服务器地址"
            onClicked: {
                Qt.createComponent("ServerUrlPage.qml").createObject(root)
            }
        }

    }
}
