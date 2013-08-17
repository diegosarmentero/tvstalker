import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem

Base {
    id: root

    property int _indexSelected: -1
    property string _nickname: ""
    property bool _flashFriendsArea: false
    property string _message: ""
    property bool _modeAddingFriends: false

    function _flash_friends_area() {
        root._flashFriendsArea = false;
        root._flashFriendsArea = true;
    }

    Component {
        id: profilePopover
        Profile {
            id: prof
        }
    }

    Component {
        id: popoverFriends

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
                    id: label_message
                    anchors {
                        left: parent.left
                        right: parent.right
                        margins: units.gu(2)
                    }
                    text: root._message
                    font.bold: true
                    color: UbuntuColors.orange
                    fontSize: "large"
                    opacity: .9
                    style: Text.Raised
                    styleColor: "black"
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                }

                Button {
                    id: button_add_all
                    text: i18n.tr("Add all")
                    anchors.right: parent.right
                    anchors.rightMargin: units.gu(2)
                    visible: root._modeAddingFriends

                    onClicked: {
                        root._flash_friends_area();
                        //for all the items
                        recommendModel.append({"nick": "Gatox", "avatar": "../img/avatar.png"});
                        popover.hide();
                    }
                }

                ListView {
                    height: root._modeAddingFriends ? root.height - label_message.height - (parent.spacing * 3) - button_add_all.height : root.height - label_message.height - (parent.spacing * 2)
                    anchors {
                        left: parent.left
                        right: parent.right
                    }

                    clip: true

                    model: friendsModel
                    delegate: ListItem.Subtitled {
                        id: listAll
                        progression: true
                        removable: root._modeAddingFriends
                        icon: Qt.resolvedUrl(avatar)
                        Label {
                            id: label_nick
                            anchors.fill: parent
                            verticalAlignment: Text.AlignVCenter
                            text: nick
                            color: "black"
                            elide: Text.ElideRight
                        }

                        onClicked: {
                            PopupUtils.open(profilePopover, root)
                        }

                        onItemRemoved: {
                            for(var i = 0; i < recommendModel.count; i++) {
                                if(recommendModel.get(i).nick == label_nick.text){
                                    return;
                                }
                            }

                            root._flash_friends_area();
                            recommendModel.append({"nick": label_nick.text, "avatar": icon});
                        }
                    }
                }
            }
        }
    }

    Component {
         id: dialog
         Dialog {
             id: dialogue
             title: i18n.tr("Remove Friend")
             text: i18n.tr("Do you want to remove %1 from this Recommendation?").arg(root._nickname)
             Button {
                 text: i18n.tr("Cancel")
                 color: "grey"
                 onClicked: PopupUtils.close(dialogue)
             }
             Button {
                 text: i18n.tr("Remove")
                 color: UbuntuColors.orange
                 onClicked: {
                    recommendModel.remove(root._indexSelected);
                    PopupUtils.close(dialogue)
                 }
             }
         }
    }

    Component {
         id: addFriendDialog
         Dialog {
             id: dialogue
             title: i18n.tr("Add Friend")
             text: i18n.tr("Type the nick of a Friend")

             TextField {
                 id: textNick
                 placeholderText: i18n.tr("Nickname")
             }

             Row {
                 spacing: units.gu(2)
                 Button {
                     text: i18n.tr("Cancel")
                     color: "grey"
                     onClicked: PopupUtils.close(dialogue)
                 }
                 Button {
                     text: i18n.tr("Add")
                     color: UbuntuColors.orange
                     onClicked: {
                        friendsModel.append({"nick": textNick.text, "avatar": "../img/avatar.png"});
                        PopupUtils.close(dialogue)
                     }
                 }
             }
         }
    }

    ListModel {
        id: suggestionModel

        ListElement {
            image: "../img/unnamed.jpg"
            showName: "Angel"
            recommendedBy: "gatox, twitter, friend1, friend2"
        }
        ListElement {
            image: "../img/unnamed.jpg"
            showName: "Angel2"
            recommendedBy: "gatox, twitter, friend1, friend2"
        }
        ListElement {
            image: "../img/unnamed.jpg"
            showName: "Angel3"
            recommendedBy: "gatox, twitter, friend1, friend2"
        }
    }

    ListModel {
        id: friendsModel

        ListElement {
            nick: ""
            avatar: ""
        }
    }

    ListModel {
        id: recommendModel

        ListElement {
            nick: ""
            avatar: ""
        }
    }

    Component.onCompleted: {
        friendsModel.clear();
        recommendModel.clear();
    }

    tools: ToolbarItems {
        ToolbarButton {
            action: Action {
                text: "Add"
                iconSource: "../img/friend_add.png"
                onTriggered: {
                    PopupUtils.open(addFriendDialog);
                }
            }
        }
        ToolbarButton {
            action: Action {
                text: "View"
                iconSource: "../img/friend.png"
                onTriggered: {
                    root._message = i18n.tr("Tap on a Friend to see Profile")
                    root._modeAddingFriends = false;
                    PopupUtils.open(popoverFriends, root)
                }
            }
        }
    }

    header: Column {
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            margins: units.gu(2)
        }
        spacing: units.gu(1)

        Label {
            text: "Recommend a Tv Show!"
            fontSize: "large"
            anchors.left: parent.left
            anchors.right: parent.right
            font.bold: true
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        }

        UbuntuShape {
            color: "#24262c"
            anchors.left: parent.left
            anchors.right: parent.right
            height: 1.48 * (root.width / 4) + units.gu(4)

            Row {
                id: row
                anchors.fill: parent
                anchors.margins: units.gu(2)
                anchors.leftMargin: units.gu(4)
                anchors.rightMargin: units.gu(4)
                spacing: units.gu(2)
                Tile {
                    id: tile
                    width: root.width / 4
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

                    UbuntuShape {
                        id: friendsArea
                        color: "#33363b"
                        height: col.height - row_buttons.height - col.spacing
                        width: col.width

                        SequentialAnimation {
                            running: root._flashFriendsArea
                            ColorAnimation { target: friendsArea; property: "color"; from: "#33363b"; to: "lightblue"; duration: 200 }
                            ColorAnimation { target: friendsArea; property: "color"; from: "lightblue"; to: "#33363b"; duration: 200 }
                        }

                        GridView {
                            id: grid
                            anchors.fill: parent
                            anchors.margins: units.gu(1)
                            clip: true

                            model: recommendModel
                            delegate: Column {
                                function get_nick() {
                                    return nickname.text;
                                }

                                Image { source: avatar; anchors.horizontalCenter: parent.horizontalCenter }
                                Text { id: nickname; text: nick; color: "white"; anchors.horizontalCenter: parent.horizontalCenter }
                            }

                            MouseArea {
                                anchors.fill: parent

                                onClicked: {
                                    var index = grid.indexAt(mouseX, mouseY);
                                    grid.currentIndex = index;
                                    if(grid.currentItem) {
                                    var nick = grid.currentItem.get_nick();
                                        root._indexSelected = index;
                                        root._nickname = nick;
                                        PopupUtils.open(dialog);
                                    }
                                }
                            }
                        }
                    }

                    Row {
                        id: row_buttons
                        spacing: units.gu(2)
                        anchors.right: parent.right

                        Button {
                            text: i18n.tr("Add Friends")

                            onClicked: {
                                root._message = i18n.tr("Swype contact to add to recommendation")
                                root._modeAddingFriends = true;
                                PopupUtils.open(popoverFriends, root)
                            }
                        }

                        Button {
                            text: i18n.tr("Send")

                            onClicked: {
                                //TODOOOOOOOO
                                recommendModel.clear();
                                tile.imageSource.source = "";
                            }
                        }
                    }
                }
            }
        }

        ListView {
            id: tiles
            spacing: units.gu(1)
            orientation: ListView.Horizontal
            height: 1.48 * root.width / 6
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
                width: root.width / 6
                height: 1.48 * width
                imageSource: Image {
                    asynchronous: true
                    source: modelData
                }

                onClicked: {
                    tile.imageSource.source = imagePath
                }
            }
        }

        ListItem.ThinDivider {}
    }

    body: Column {
        spacing: units.gu(2)
        anchors {
            left: parent.left
            right:parent.right
            margins: units.gu(2)
        }

        Label {
            text: "Tv Shows recommended for you"
            fontSize: "large"
            anchors.left: parent.left
            anchors.right: parent.right
            font.bold: true
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        }

        Row {
            spacing: units.gu(2)
            anchors.right: parent.right

            Label {
                text: i18n.tr("Swype items to mark as read")
                anchors.bottom: parent.bottom
            }

            Button {
                text: i18n.tr("Mark all as read")

                onClicked: {
                    suggestionModel.clear();
                }
            }
        }

        Repeater {
            model: suggestionModel

            ListItem.Subtitled {
                progression: true
                icon: Qt.resolvedUrl(image)
                removable: true

                onClicked: {
                    console.log("diego")
                }


                onItemRemoved: {
                    suggestionModel.remove(index);
                }

                UbuntuShape {
                    anchors.fill: parent
                    color: "#ededed"

                    Label {
                        id: labelShowName
                        anchors {
                            left: parent.left
                            right: parent.right
                            top: parent.top
                            margins: units.dp(2)
                        }

                        text: i18n.tr("<b>%1</b> (Recommended by:)").arg(showName)
                        color: "black"
                        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    }
                    Label {
                        anchors {
                            left: parent.left
                            right: parent.right
                            top: labelShowName.bottom
                            margins: units.dp(2)
                        }
                        text: recommendedBy
                        color: "gray"
                        elide: Text.ElideRight
                    }
                }
            }
        }
    }

}
