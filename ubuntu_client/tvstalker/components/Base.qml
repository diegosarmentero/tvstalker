import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1

Page {
    id: root

    property int keyboardSize: Qt.inputMethod.visible ? Qt.inputMethod.keyboardRectangle.height : 0

    property Component header
    property Component body
    property Component footer

    signal flickMoved

    property bool _loadingOpened: false

    Component {
        id: loading
        Dialog {
            id: dialogue
            title: i18n.tr("Loading...")

            property bool stayOpen: root._loadingOpened

            onStayOpenChanged: {
                if(stayOpen == false) {
                    PopupUtils.close(dialogue);
                }
            }

            ActivityIndicator {
                running: dialogue.visible
            }
        }
    }

    function show_loading() {
        root._loadingOpened = true;
        PopupUtils.open(loading);
    }

    function hide_loading() {
        root._loadingOpened = false;
    }

    Flickable {
        id: flick
        anchors.fill: parent
        clip: true
        contentHeight: column.height + root.keyboardSize

        onMovementStarted: root.flickMoved();

        Column {
            id: column
            objectName: "column"
            anchors {
                left: parent.left
                right: parent.right
            }
            height: childrenRect.height + units.gu(8)
            spacing: units.gu(3)

            Loader {
                id: loaderHeader
                anchors.left: parent.left
                anchors.right: parent.right
                sourceComponent: header ? header : undefined
            }

            Loader {
                id: loader
                anchors.left: parent.left
                anchors.right: parent.right
                sourceComponent: body ? body : undefined
            }

            Loader {
                id: loaderFooter
                anchors.left: parent.left
                anchors.right: parent.right
                sourceComponent: footer ? footer : undefined
            }
        }
    }

}
