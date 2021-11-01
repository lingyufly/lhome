import QtQuick 2.0


Rectangle {

    /**
      * Public
      */

    /**
      * @brief 显示Toast
      *
      * @param {string} 要显示的内容字符串
      * @param {real} 显示的时间（毫秒）, 默认 3000
      */
    function show(text, duration) {
        message.text = text;

        // 判断是否超出最大的显示宽度
        width = Math.min(message.contentWidth+20, 0.7*parent.width);

        if (typeof duration !== "undefined") {
            time = Math.max(duration, 2 * fadeTime);
        }
        else {
            time = defaultTime;
        }
        animation.start();
    }

    id: root

    // 完成后是否自动释放
    property bool selfDestroying: false
    readonly property real defaultTime: 3000
    property real time: defaultTime
    readonly property real fadeTime: 300
    property real margin: 10

    anchors {
        horizontalCenter: parent.horizontalCenter
        margins: margin
    }

    height: message.height + margin
    width:0
    radius: margin

    opacity: 0
    color: "#222222"

    Text {
        id: message
        color: "white"
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignHCenter
        anchors {
            bottom: parent.bottom
            left: parent.left
            right: parent.right
            margins: margin / 2
        }
    }

    SequentialAnimation on opacity {
        id: animation
        running: false

        NumberAnimation {
            to: .9
            duration: fadeTime
        }

        PauseAnimation {
            duration: time - 2 * fadeTime
        }

        NumberAnimation {
            to: 0
            duration: fadeTime
        }

        onRunningChanged: {
            if (!running && selfDestroying) {
                root.destroy();
            }
        }
    }
}
