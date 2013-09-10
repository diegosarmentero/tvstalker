import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem
import "../js/generic_functions.js" as GenericFunctions

Base {
    id: root

    property int tileInfoArea: units.gu(10)
    property var selectedFilter: ["All Shows", ""]

    Component {
        id: showDetails
        ShowDetails {
            id: details

            contentHeight: root.height
            contentWidth: root.width
        }
    }

    Component {
        id: popoverComponent

        Popover {
            id: popover
            Rectangle {
                anchors.fill: parent
                color: "#24262c"
            }

            Column {
                id: containerLayout
                anchors {
                    left: parent.left
                    top: parent.top
                    right: parent.right
                }
                ListItem.Standard {
                    id: listAll
                    text: "All Shows"
                    control: Switch {
                        checked: root.selectedFilter[0] == listAll.text ? true : false
                        onClicked: {
                            root.selectedFilter = [listAll.text, ""];
                            popover.hide();
                        }
                    }
                }
                ListItem.Standard {
                    id: listToday
                    text: "Today Airdate"
                    control: Switch {
                        checked: root.selectedFilter[0] == listToday.text ? true : false
                        onClicked: {
                            root.selectedFilter = [listToday.text, ""];
                            popover.hide();
                        }
                    }
                }
                ListItem.Standard {
                    id: listYesterday
                    text: "Yesterday"
                    control: Switch {
                        checked: root.selectedFilter[0] == listYesterday.text ? true : false
                        onClicked: {
                            root.selectedFilter = [listYesterday.text, ""];
                            popover.hide();
                        }
                    }
                }
                ListItem.Standard {
                    id: listDate
                    text: "By Date/Month"
                    selected: root.selectedFilter[0] == listDate.text ? true : false
                    control: TextField {
                        id: textDate
                        width: units.gu(12)
                        inputMask: "99/99"
                        placeholderText: "DD/MM"
                        text: root.selectedFilter[0] == listDate.text ? root.selectedFilter[1] : ""
                    }
                    progression: true
                    onClicked: {
                        root.selectedFilter = [listDate.text, textDate.text];
                        popover.hide();
                    }
                }
            }
        }
    }

    header: UbuntuShape {
        id: search_area
        color: "#24262c"

        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            margins: units.gu(2)
        }


        Behavior on opacity { NumberAnimation { duration: UbuntuAnimation.SlowDuration } }

        Row {
            id: row_search
            spacing: units.gu(2)
            anchors.fill: parent
            anchors.leftMargin: units.gu(2)
            anchors.rightMargin: units.gu(2)
            anchors.topMargin: units.gu(2)
            IconButton {
                id: filterButton
                height: text_search.height
                icon: "../img/calendar.png"
                middleText: GenericFunctions.get_current_day()
                onClicked: PopupUtils.open(popoverComponent, filterButton)
            }

            TextField {
                id: text_search
                width: row_search.width - (row_search.spacing * 2) - btnSearch.width - filterButton.width
                hasClearButton: true
                placeholderText: i18n.tr("Type the name of a Tv Show")
            }

            Button {
                id: btnSearch
                text: i18n.tr("Search")
                height: text_search.height
                iconSource: "../img/search.png"

                onClicked: text_search.focus = false;

            }
        }
    }

    body: Grid {
        id: grid
        columns: main.width / units.gu(30)
        spacing: units.gu(2)
        anchors {
            left: parent.left
            top: parent.top
            right:parent.right
            margins: units.gu(4)
        }

        Repeater {
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
            Tile {
                width: grid.width / grid.columns - grid.spacing
                height: 1.48 * width + root.tileInfoArea
                tileInfoArea: root.tileInfoArea
                showName: "Angel"
                showSeason: 5
                showEpisode: 17
                showDate: "02/10/2013"
                imageSource: Image {
                    asynchronous: true
                    source: modelData
                }

                onClicked: {
                    PopupUtils.open(showDetails);
                }
            }
        }
    }
}
