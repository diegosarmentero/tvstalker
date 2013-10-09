import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem
import "../js/server.js" as Server

Rectangle {
    id: root
    anchors.fill: parent
    color: "black"
    opacity: 0.9

    property bool loadingOpened: false
    property string showid: ""
    property string poster: ""
    property var model
    property bool following: true

    onShowidChanged: {
        if(root.showid.length > 0) {
            root.loadingOpened = true;
            Server.get_show_details(main.userTOKEN, root.showid, callback)
        }
    }

    function callback(info) {
        labelTitle.text = info["title"];
        labelDescription.text = info["overview"];
        root.poster = info["poster"];
        root.model = info["seasons"]
        root.loadingOpened = false;
    }

    MouseArea {
        anchors.fill: parent
    }

    ActivityIndicator {
        running: root.loadingOpened
        visible: root.loadingOpened
        anchors.centerIn: parent
    }

    Flickable {
        id: flick
        anchors.fill: parent
        anchors.margins: units.gu(4)
        anchors.topMargin: units.gu(12)
        clip: true
        visible: !root.loadingOpened
        contentHeight: column.height + units.gu(20)
        Column {
            id: column
            spacing: units.gu(2)

            Label {
                id: labelTitle
                font.bold: true
                fontSize: "x-large"
                width: flick.width
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }

            Label {
                id: labelDescription
                width: flick.width
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            }

            Row {
                id: row
                spacing: units.gu(2)
                Button {
                    text: i18n.tr("Close")
                    color: "grey"
                    onClicked: {
                        root.visible = false;
                        root.showid = "";
                    }
                }
                Button {
                    text: root.following ? i18n.tr("Unfollow") : i18n.tr("Follow")
                    color: UbuntuColors.orange
                    onClicked: {
                        Server.add_show(main.userTOKEN, root.showid, main.reload_shows);
                        root.visible = false;
                    }
                }
            }

            Rectangle {
                color: "transparent"
                width: flick.width
                height: tile.height
                Tile {
                    id: tile
                    width: flick.width / 2
                    height: 1.48 * width
                    anchors.centerIn: parent
                    imageSource: Image {
                        asynchronous: true
                        source: root.poster
                    }
                }
            }
            Column {
                id: colInfo
                anchors {
                    left: parent.left
                    right: parent.right
                }
                Repeater {
                    model: root.model
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
                                visible: modelData["is_season"]

                                text: i18n.tr("<b>Season %1</b>").arg(modelData["season"])
                                fontSize: "large"
                                horizontalAlignment: Text.AlignLeft
                                color: "white"
                                elide: Text.ElideRight
                                style: Text.Raised
                                styleColor: "grey"
                            }
                            Row {
                                spacing: units.gu(2)
                                visible: !modelData["is_season"]
                                CheckBox {
                                    checked: modelData["viewed"] ? modelData["viewed"] : false
                                    onCheckedChanged: {
                                        var episode = lblEpisodeNro.text
                                        var season = lblEpisodeNro.season
                                        Server.mark_as_viewed(main.userTOKEN, root.showid, checked, season, episode);
                                    }
                                }
                                Label {
                                    id: lblEpisodeNro
                                    property string season: modelData["season"]
                                    text: modelData["nro"] ? modelData["nro"] : ""
                                    color: UbuntuColors.orange
                                    style: Text.Raised
                                    styleColor: "grey"
                                    elide: Text.ElideRight
                                }
                                Label {
                                    text: modelData["name"] ? modelData["name"] : ""
                                    color: UbuntuColors.orange
                                    style: Text.Raised
                                    styleColor: "grey"
                                    elide: Text.ElideRight
                                }
                                Label {
                                    text: modelData["airdate"] ? modelData["airdate"] : ""
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
}
