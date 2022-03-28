import QtQuick 2.0
import QtQuick.Controls 2.3
Item {
    SwipeView{
        anchors.fill: parent
        id:swipeview
        currentIndex: footer.currentIndex
        UserInfoPage{
            id:userInfoPage
        }
        BillPage{
            id:billPage
        }
        FamilyInfoPage {
            id:familyInfoPage
        }
    }

    TabBar{
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        id:footer
        currentIndex: swipeview.currentIndex
        TabButton{
            text:"个人"
        }
        TabButton{
            text:"账本"
        }
        TabButton{
            text:"家庭"
        }
    }
    Component.onCompleted: {
        swipeview.setCurrentIndex(1)
    }

}
