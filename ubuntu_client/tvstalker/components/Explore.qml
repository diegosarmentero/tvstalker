import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem
import "../js/server.js" as Server

Base {
    id: root

    property var monday
    property var tuesday
    property var wednesday
    property var thursday
    property var friday
    property var saturday
    property var sunday

    function load_explore(){
        Server.explore_day("monday", monday_callback);
        Server.explore_day("tuesday", tuesday_callback);
        Server.explore_day("wednesday", wednesday_callback);
        Server.explore_day("thursday", thursday_callback);
        Server.explore_day("friday", friday_callback);
        Server.explore_day("saturday", saturday_callback);
        Server.explore_day("sunday", sunday_callback);
    }

    function monday_callback(info){
        root.monday = info;
    }

    function tuesday_callback(info){
        root.tuesday = info;
    }

    function wednesday_callback(info){
        root.wednesday = info;
    }

    function thursday_callback(info){
        root.thursday = info;
    }

    function friday_callback(info){
        root.friday = info;
    }

    function saturday_callback(info){
        root.saturday = info;
    }

    function sunday_callback(info){
        root.sunday = info;
    }

    ShowDetails {
        id: details
        visible: false
        following: false
    }

    body: Column {
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            margins: units.gu(2)
        }
        spacing: units.gu(1)

        Label {
            text: i18n.tr("Monday")
            color: UbuntuColors.orange
            fontSize: "x-large"
            font.bold: true
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        }

        ListView {
            id: tilesMonday
            spacing: units.gu(1)
            orientation: ListView.Horizontal
            height: 1.48 * root.width / 4
            anchors {
                left: parent.left
                right: parent.right
                margins: units.gu(1)
            }
            model: root.monday

            delegate: Tile {
                width: root.width / 4
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData["poster"]
                }

                onClicked: {
                    details.showid = modelData["showid"];
                    details.visible = true;
                }
            }
        }

        ListItem.ThinDivider {}

        Label {
            text: i18n.tr("Tuesday")
            color: UbuntuColors.orange
            fontSize: "x-large"
            font.bold: true
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        }

        ListView {
            id: tilesTuesday
            spacing: units.gu(1)
            orientation: ListView.Horizontal
            height: 1.48 * root.width / 4
            anchors {
                left: parent.left
                right: parent.right
                margins: units.gu(1)
            }
            model: root.tuesday

            delegate: Tile {
                width: root.width / 4
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData["poster"]
                }

                onClicked: {
                    details.showid = modelData["showid"];
                    details.visible = true;
                }
            }
        }

        ListItem.ThinDivider {}

        Label {
            text: i18n.tr("Wednesday")
            color: UbuntuColors.orange
            fontSize: "x-large"
            font.bold: true
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        }

        ListView {
            id: tilesWednesday
            spacing: units.gu(1)
            orientation: ListView.Horizontal
            height: 1.48 * root.width / 4
            anchors {
                left: parent.left
                right: parent.right
                margins: units.gu(1)
            }
            model: root.wednesday

            delegate: Tile {
                width: root.width / 4
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData["poster"]
                }

                onClicked: {
                    details.showid = modelData["showid"];
                    details.visible = true;
                }
            }
        }

        ListItem.ThinDivider {}

        Label {
            text: i18n.tr("Thursday")
            color: UbuntuColors.orange
            fontSize: "x-large"
            font.bold: true
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        }

        ListView {
            id: tilesThursday
            spacing: units.gu(1)
            orientation: ListView.Horizontal
            height: 1.48 * root.width / 4
            anchors {
                left: parent.left
                right: parent.right
                margins: units.gu(1)
            }
            model: root.thursday

            delegate: Tile {
                width: root.width / 4
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData["poster"]
                }

                onClicked: {
                    details.showid = modelData["showid"];
                    details.visible = true;
                }
            }
        }

        ListItem.ThinDivider {}

        Label {
            text: i18n.tr("Friday")
            color: UbuntuColors.orange
            fontSize: "x-large"
            font.bold: true
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        }

        ListView {
            id: tilesFriday
            spacing: units.gu(1)
            orientation: ListView.Horizontal
            height: 1.48 * root.width / 4
            anchors {
                left: parent.left
                right: parent.right
                margins: units.gu(1)
            }
            model: root.friday

            delegate: Tile {
                width: root.width / 4
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData["poster"]
                }

                onClicked: {
                    details.showid = modelData["showid"];
                    details.visible = true;
                }
            }
        }

        ListItem.ThinDivider {}

        Label {
            text: i18n.tr("Saturday")
            color: UbuntuColors.orange
            fontSize: "x-large"
            font.bold: true
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        }

        ListView {
            id: tilesSaturday
            spacing: units.gu(1)
            orientation: ListView.Horizontal
            height: 1.48 * root.width / 4
            anchors {
                left: parent.left
                right: parent.right
                margins: units.gu(1)
            }
            model: root.saturday

            delegate: Tile {
                width: root.width / 4
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData["poster"]
                }

                onClicked: {
                    details.showid = modelData["showid"];
                    details.visible = true;
                }
            }
        }

        ListItem.ThinDivider {}

        Label {
            text: i18n.tr("Sunday")
            color: UbuntuColors.orange
            fontSize: "x-large"
            font.bold: true
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        }

        ListView {
            id: tilesSunday
            spacing: units.gu(1)
            orientation: ListView.Horizontal
            height: 1.48 * root.width / 4
            anchors {
                left: parent.left
                right: parent.right
                margins: units.gu(1)
            }
            model: root.sunday

            delegate: Tile {
                width: root.width / 4
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData["poster"]
                }

                onClicked: {
                    details.showid = modelData["showid"];
                    details.visible = true;
                }
            }
        }

        ListItem.ThinDivider {}

    }
}
