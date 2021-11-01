import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 2.12

import "../js/ajax.js" as Ajax

Rectangle {
    id:root
    height: 300
    width: 300
    x:parent.width/2-width/2
    y:parent.height/2-height/2

    Column{
        anchors.margins: 5
        anchors.fill: parent
        spacing: 6
        Text{
            text:"注册用户"
        }

        Text{
            text:"用户名:"
        }

        TextField{
            width:parent.width
            id:mUserNameTf
        }

        Text {
            text: "密码"
        }
        TextField{
            width:parent.width
            id:mPassWordTf
        }

        Row{
            width:parent.width
            height:mPassWordTf.height
            spacing: 6
            Button{
                text: "注册"
                onClicked: {
                    var unm=mUserNameTf.text
                    var pwd=mPassWordTf.text
                    Ajax.post("/user/registeruser",
                              {"username":unm, "password":pwd},
                              function(res){
                                  if (res.code===0){
                                      mToast.show("注册成功!");
                                  }else{
                                      mToast.show("错误:"+res.msg);
                                  }
                              },
                              function(res){
                                  mToast.show("错误:"+res.msg);
                              });
                }
            }
            Button{
                text:"退出"
                anchors.right: parent.right
                onClicked: {
                    root.destroy();
                }
            }
        }
    }

    onVisibleChanged: {
        if (visible){

        }
    }
}
