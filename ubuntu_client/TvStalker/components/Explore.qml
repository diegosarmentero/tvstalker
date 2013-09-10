import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem

Base {
    id: root

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

        ListItem.ThinDivider {}

    }
}
