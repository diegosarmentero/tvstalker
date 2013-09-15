import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1
import "../js/server.js" as Server

Base {
    id: root

    property string _description: ""
    property string showid: ""
    property string show_title: ""
    property string type: "rated"
    property int page: 0
    property bool showButton: true
    property var model

    function load_recommend() {
        Server.recommend(main.userTOKEN, root.type, root.page, load_callback);
        root.showButton = true;
    }

    function previous_page(){
        if(page > 0){
            page--;
        }

        Server.recommend(main.userTOKEN, root.type, root.page, load_callback);
    }

    function next_page() {
        page++;

        Server.recommend(main.userTOKEN, root.type, root.page, load_callback);
    }

    function load_callback(info) {
        if(info.length > 0){
            root.model = info;
        }else{
            page--;
        }
    }

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
            model: root.model

            delegate: Tile {
                id: item
                width: root.width / 4
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData["poster"]
                }

                onClicked: {
                    tile.imageSource.source = modelData["poster"]
                    text_area_description.text = modelData["overview"]
                    root.show_title = modelData["title"]
                    root.showid = modelData["showid"]
                }
            }
        }

        Row {
            spacing: units.gu(1)

            Button {
                text: "Most Rated"
                onClicked: {
                    root.type = "rated";
                    root.page = 0;
                    root.load_recommend();
                }
            }

            Button {
                text: "Most Viewed"
                onClicked: {
                    root.type = "viewed";
                    root.page = 0;
                    root.load_recommend();
                }
            }

            Button {
                text: "< Previous"
                onClicked: {
                    root.previous_page();
                }
            }

            Button {
                text: "Next >"
                onClicked: {
                    root.next_page();
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
                        id: labelTitle
                        fontSize: "large"
                        color: "white"
                        text: show_title
                    }

                    Label {
                        id: labelExpand
                        text: i18n.tr("Tap text to expand")
                    }

                    UbuntuShape {
                        id: friendsArea
                        color: "white"
                        height: col.height - row_buttons.height - (col.spacing * 2) - labelExpand.height - labelTitle.height
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
                            id: btn
                            text: i18n.tr("Follow")
                            visible: root.showButton

                            onClicked: {
                                Server.add_show(main.userTOKEN, root.showid, root.reload);
                                root.showButton = false;
                            }
                        }
                    }
                }
            }
        }
    }

    function reload(info){
        main.reload_shows();
    }
}
