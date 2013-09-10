import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem

Dialog {
    id: dialogue
    title: i18n.tr("Angel")

    property int contentWidth: 0
    property int contentHeight: 0

    ListModel {
        id: suggestionModel

        ListElement {
            image: "../img/unnamed.jpg"
            showName: "Season 1"
            episode: ""
        }
        ListElement {
            image: "../img/unnamed.jpg"
            showName: "aAsdsasssssssssssssssssssssssssssss"
            episode: "e01: 10/02/2012"
        }
        ListElement {
            image: "../img/unnamed.jpg"
            showName: "Qqwwer"
            episode: "e02: 17/02/2012"
        }
        ListElement {
            image: "../img/unnamed3.jpg"
            showName: "Season 2"
        }
        ListElement {
            image: "../img/unnamed.jpg"
            showName: "Ggfhgh"
            episode: "e01: 10/02/2013"
        }
        ListElement {
            image: "../img/unnamed.jpg"
            showName: "Hjhhhhj"
            episode: "e02: 17/02/2013"
        }
    }

    Flickable {
        id: flick
        height: dialogue.contentHeight
        width: dialogue.contentWidth
        clip: true
        contentHeight: column.height + units.gu(20)
        Column {
            id: column
            spacing: units.gu(2)

            Label {
                text: i18n.tr("The vampire Angel, cursed with a soul, moves to Los Angeles and aids people with supernatural-related problems while questing for his own redemption. ")
                width: flick.width
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }

            Row {
                id: row
                spacing: units.gu(2)
                Button {
                    text: i18n.tr("Close")
                    color: "grey"
                    onClicked: PopupUtils.close(dialogue)
                }
                Button {
                    text: i18n.tr("Unfollow")
                    color: UbuntuColors.orange
                    onClicked: {
                       PopupUtils.close(dialogue)
                    }
                }
            }

            Tile {
                id: tile
                width: flick.width
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: "../img/unnamed.jpg"
                }
            }
            Column {
                id: colInfo
                anchors {
                    left: parent.left
                    right: parent.right
                }
                Repeater {
                    model: suggestionModel
                    delegate: ListItem.Subtitled {
                        id: listAll
                        Rectangle {
                            anchors.fill: parent
                            color: "transparent"

                            Label {
                                id: labelShowName
                                anchors {
                                    left: parent.left
                                    right: parent.right
                                    top: parent.top
                                    margins: units.dp(2)
                                }

                                text: i18n.tr("<b>%1</b>").arg(showName)
                                fontSize: episode ? "medium" : "large"
                                horizontalAlignment: episode ? Text.AlignLeft : Text.AlignHCenter
                                color: "white"
                                elide: Text.ElideRight
                                style: Text.Raised
                                styleColor: "grey"
                            }
                            Label {
                                anchors {
                                    left: parent.left
                                    right: parent.right
                                    top: labelShowName.bottom
                                    margins: units.dp(2)
                                }
                                text: episode ? episode : ""
                                color: UbuntuColors.orange
                                style: Text.Raised
                                styleColor: "grey"
                                elide: Text.ElideRight
                            }
                        }
                    }
                }
            }
        }
    }
}
