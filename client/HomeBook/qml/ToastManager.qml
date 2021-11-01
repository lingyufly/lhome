import QtQuick 2.0


ListView {

    /**
      * @brief 显示Toast
      *
      * @param {string} 要显示的内容字符串
      * @param {real} 显示的时间（毫秒）, 默认 3000
      */
    function show(text, duration) {
        model.insert(0, {text: text, duration: duration});
    }

    id: root

    z: Infinity
    spacing: 5
    anchors.fill: parent
    anchors.bottomMargin: 40
    verticalLayoutDirection: ListView.BottomToTop

    interactive: false

    displaced: Transition {
        NumberAnimation {
            properties: "y"
            easing.type: Easing.InOutQuad
        }
    }

    delegate: Toast {
        Component.onCompleted: {
            if (typeof duration === "undefined") {
                show(text);
            }
            else {
                show(text, duration);
            }
        }
    }

    model: ListModel {id: model}
}
