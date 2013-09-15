import QtQuick 2.0
import Ubuntu.Components 0.1

Button {
    id: root

    property alias icon: img.source
    property alias middleText: label.text
    property int pendingNotifications: 0

    width: units.gu(6)

    Image {
        id: img
        anchors.fill: parent
        fillMode: Image.PreserveAspectFit
        smooth: true
        Label {
            id: label
            anchors {
                left: parent.left
                right: parent.right
                bottom: parent.bottom
                bottomMargin: units.dp(3)
                rightMargin: units.dp(1)
            }

            horizontalAlignment: Text.AlignHCenter
            text: ""
            font.bold: true
            color: "#333333"
        }
    }

    UbuntuShape {
        color: UbuntuColors.lightAubergine
        width: label_notifications.width
        height: label_notifications.height
        radius: "medium"
        visible: root.pendingNotifications != 0 ? true : false
        anchors {
            right: parent.right
            bottom: parent.bottom
            margins: units.dp(3)
        }

        Label {
            id: label_notifications
            text: root.pendingNotifications != 0 ? root.pendingNotifications : ""
            font.bold: true
            color: "white"
            opacity: .9
            style: Text.Raised
            styleColor: "black"
        }
    }
}
