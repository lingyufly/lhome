import QtQuick 2.0
import QtQuick.Controls 2.12
import QtQuick.Dialogs 1.3

import "../js/ajax.js" as Ajax

Item {
    id:root
    anchors.centerIn: parent
    Column{
        id:column
        anchors.centerIn: parent
        spacing: 5
        width: parent.width*0.7

        TextField{
            id: mUserNameTf
            width: parent.width
            placeholderText: "请输入用户名"
            text: {
                return cSetting.getString("login/username");
            }
        }
        TextField{
            id:mPassWordTf
            width: parent.width
            echoMode: TextField.Password
            placeholderText: "请输入密码"

            text: {
                if (cSetting.getBool("login/autologin")){
                    return cSetting.getString("login/password");
                }
            }
        }

        Item{
            width: parent.width
            height:mPassWordTf.height
            CheckBox{
                id: mAutoLoginCbx
                text:"自动登录"
                onCheckedChanged: {
                    cSetting.setValue("login/autologin", checked)
                }

                checked: {
                    return cSetting.getBool("login/autologin")
                }
            }
            Button{
                text:"忘记密码"
                anchors.right:parent.right
                onClicked: {
                }
            }
        }

        Item {
            width: parent.width
            height:mPassWordTf.height
            Button{
                id:mSighnInBtn
                text:"注册"
                onClicked: {
                    m_RegistryPage.open()
                }
            }
            Button{
                id:mLoginBtn
                anchors.right:parent.right
                text:"登录"
                onClicked: {
                    var unm=mUserNameTf.text
                    var pwd=mPassWordTf.text
                    cSetting.setValue("login/username", unm);
                    if (mAutoLoginCbx.checked){
                        cSetting.setValue("login/password", pwd);
                    }
                    else{
                        cSetting.setValue("login/password", "");
                    }

                    login();
                }
            }
        }

        Button{
            width: parent.width
            text:"服务器地址"
            onClicked: {
                m_ServerUrlPage.open()
            }
        }

        // 服务器地址设置窗口
        ServerUrlPage {
             id: m_ServerUrlPage
             modal: true
         }

        // 用户注册窗口
        RegistryPage{
            id:m_RegistryPage
            modal: true
        }


    }

    function login(){
        var unm=mUserNameTf.text
        var pwd=mPassWordTf.text
        Ajax.post("/auth/login",
            {"username":unm, "password":pwd},
            function(res){
              if (res.code===0){
                  mToast.show("登录成功");
                  mLoginPage.visible=false;
                  mMainPage.visible=true;
                  cAjax.setToken(res.data.token);
              }
              else{
                  mToast.show("错误:"+res.msg);
              }
            });
    }

    Component.onCompleted: {
        // 自动登录
        if (cSetting.getBool("login/autologin")){
            login();
        }
    }
}
