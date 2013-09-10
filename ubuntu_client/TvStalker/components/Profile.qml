import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem

Popover {
    id: popover

    Component {
        id: showDetails
        ShowDetails {
            id: details

            contentHeight: root.height
            contentWidth: root.width
        }
    }

    Rectangle {
        anchors.fill: parent
        color: "#ededed"
    }

    Column {
        anchors {
            left: parent.left
            top: parent.top
            right: parent.right
            topMargin: units.gu(2)
        }
        spacing: units.gu(2)

        Row {
            spacing: units.gu(2)

            Tile {
                id: tile
                width: popover.width / 8
                height: width
                tileInfoArea: 0
                imageSource: Image {
                    source: "../img/avatar.png"
                }
            }

            Label {
                text: "Name"
                color: UbuntuColors.coolGrey
                fontSize: "large"
                opacity: .9
                style: Text.Raised
                styleColor: "grey"
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }
        }

        Label {
            id: labelTvShows
            text: "Tv Shows:"
            color: UbuntuColors.coolGrey
            opacity: .9
            style: Text.Raised
            styleColor: "grey"
        }

        ListView {
            height: main.height - tile.height - (parent.spacing * 2) - labelTvShows.height
            anchors {
                left: parent.left
                right: parent.right
            }

            clip: true

            model: 30
            delegate: ListItem.Subtitled {
                id: listAll
                progression: true
                icon: Qt.resolvedUrl("../img/unnamed4.jpg")
                Label {
                    id: label_nick
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                    text: "Dr House"
                    color: "black"
                    elide: Text.ElideRight
                }

                onClicked: {
                    PopupUtils.open(showDetails);
                }
            }
        }
    }
}
