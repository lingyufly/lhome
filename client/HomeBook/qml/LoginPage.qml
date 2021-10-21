import QtQuick 2.0
import QtQuick.Controls 2.12

import "../js/ajax.js" as Ajax

Rectangle {

    anchors.centerIn: parent
    color: "gray"
    Column{
        id:column
        anchors.centerIn: parent
        spacing: 10
        width: parent.width/2
        TextField{
            id: username
            width: parent.width
        }
        TextField{
            id:password
            width: parent.width
        }

        Rectangle{
            width: parent.width
            height:password.height
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
            height:password.height
            Button{
                id:sighnBtn
                width: parent.width/2
                text:"注册"
                onClicked: {
                    var unm=username.text
                    var pwd=password.text
                    Ajax.post("http://127.0.0.1:8000/user/registeruser",
                              {"username":unm, "password":pwd},
                              function(res){
                                console.log(res)
                              },
                              function(res){
                                console.log(res)
                              });
                }
            }
            Button{
                id:loginBtn
                width: parent.width/2
                anchors.right:parent.right
                text:"登录"
                onClicked: {
                    var unm=username.text
                    var pwd=password.text
                    Ajax.post("http://127.0.0.1:8000/auth/login",
                              {"username":unm, "password":pwd},
                              function(res){
                                console.log(res)
                              },
                              function(res){
                                console.log(res)
                              });
                }
            }
        }

        Button{
            width: parent.width
            text:"服务器地址"
        }
    }
}
