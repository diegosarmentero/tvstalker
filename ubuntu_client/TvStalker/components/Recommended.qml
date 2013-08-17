import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1

Base {
    id: root

    property string _description: ""

    Component {
        id: popoverDescription

        Popover {
            id: popover
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

                Label {
                    id: label_description
                    anchors {
                        left: parent.left
                        right: parent.right
                        margins: units.gu(2)
                    }
                    text: root._description
                    color: UbuntuColors.coolGrey
                    fontSize: "large"
                    opacity: .9
                    style: Text.Raised
                    styleColor: "grey"
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                }
            }
        }
    }

    body: Column {
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            margins: units.gu(2)
        }
        spacing: units.gu(1)

        ListView {
            id: tiles
            spacing: units.gu(1)
            orientation: ListView.Horizontal
            height: 1.48 * root.width / 4
            anchors {
                left: parent.left
                right: parent.right
                margins: units.gu(1)
            }
            model: [
                "../img/unnamed.jpg",
                "../img/unnamed2.jpg",
                "../img/unnamed3.jpg",
                "../img/unnamed4.jpg",
                "../img/unnamed5.jpg",
                "../img/unnamed6.jpg",
                "../img/unnamed7.jpg",
                "../img/unnamed8.jpg",
            ]

            delegate: Tile {
                id: item
                width: root.width / 4
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData
                }

                onClicked: {
                    tile.imageSource.source = imagePath
                    text_area_description.text = " ajsdhasjk dshsa dasd sahdksja dksah sahsad sajhdas jksa sajdas sahdkj asdhsa dashdjksa djsahjkd sadhasjk dsahdjsak djashd ashdaskj djas dkjsad  ajsdhasjk dshsa dasd sahdksja dksah sahsad sajhdas jksa sajdas sahdkj asdhsa dashdjksa djsahjkd sadhasjk dsahdjsak djashd ashdaskj djas dkjsad  ajsdhasjk dshsa dasd sahdksja dksah sahsad sajhdas jksa sajdas sahdkj asdhsa dashdjksa djsahjkd sadhasjk dsahdjsak djashd ashdaskj djas dkjsad"
                }
            }
        }

        UbuntuShape {
            color: "#24262c"
            anchors.left: parent.left
            anchors.right: parent.right
            height: 1.48 * (root.width / 3) + units.gu(4)

            Row {
                id: row
                anchors.fill: parent
                anchors.margins: units.gu(2)
                anchors.leftMargin: units.gu(4)
                anchors.rightMargin: units.gu(4)
                spacing: units.gu(2)
                Tile {
                    id: tile
                    width: root.width / 3
                    height: 1.48 * width
                    tileInfoArea: 0
                    imageSource: Image {
                        source: ""
                    }
                }

                Column {
                    id: col
                    spacing: units.gu(1)
                    height: tile.height
                    width: row.width - tile.width - row.spacing

                    Label {
                        id: labelExpand
                        text: i18n.tr("Tap text to expand")
                    }

                    UbuntuShape {
                        id: friendsArea
                        color: "white"
                        height: col.height - row_buttons.height - (col.spacing * 2) - labelExpand.height
                        width: col.width

                        TextArea {
                            id: text_area_description
                            anchors.fill: parent
                            anchors.margins: units.gu(1)
                            readOnly: true

                            font.pixelSize: units.gu(2)
                            text: ""

                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    root._description = text_area_description.text;
                                    PopupUtils.open(popoverDescription, text_area_description)
                                }
                            }
                        }
                    }

                    Row {
                        id: row_buttons
                        spacing: units.gu(2)
                        anchors.right: parent.right

                        Button {
                            text: i18n.tr("Follow")

                            onClicked: {
                                //TODOOOOOOOO
                            }
                        }
                    }
                }
            }
        }
    }
}
