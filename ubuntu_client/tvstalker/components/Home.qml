import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.Popups 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem
import "../js/generic_functions.js" as GenericFunctions
import "../js/server.js" as Server
import "../js/filter.js" as Filter

Base {
    id: root

    property int tileInfoArea: units.gu(10)
    property var selectedFilter: ["All", "Current", ""]
    property var multipleModel
    property string error: ""

    property string _temp_search: ""

    Component {
         id: dialogError
         Dialog {
             id: dialogue
             title: i18n.tr("Show not Found")

             Column {
                 spacing: units.gu(1)
                 Label {
                     text: root.error
                 }

                 Button {
                     id: btnClose
                     text: i18n.tr("Close")
                     color: "grey"
                     onClicked: PopupUtils.close(dialogue)
                     anchors {
                         left: parent.left
                         right: parent.right
                     }
                 }
             }
         }
    }

    Component {
         id: dialog
         Dialog {
             id: dialogue
             title: i18n.tr("Choose Show")

             Column {
                 spacing: units.gu(1)
                 Button {
                     id: btnClose
                     text: i18n.tr("Close")
                     color: "grey"
                     onClicked: PopupUtils.close(dialogue)
                     anchors {
                         left: parent.left
                         right: parent.right
                     }
                 }

                 Repeater{
                     model: root.multipleModel

                     Button {
                         property string showid: modelData[0]
                         iconSource: modelData[2]
                         text: modelData[1]
                         width: btnClose.width

                         onClicked: {
                             Server.add_show(main.userTOKEN, showid, root.search_callback);
                             PopupUtils.close(dialogue);
                         }
                     }
                 }
             }
         }
    }

    ShowsModel {
        id: showsModel
    }

    Component.onCompleted: {
        showsModel.clear();
    }

    function init_user() {
        timer.running = true;
    }

    Timer {
        id: timer
        interval: 3600000; running: false; repeat: true
        onTriggered: load_shows();
    }

    function load_shows() {
        Server.get_shows(main.userTOKEN, load_callback);
    }

    function load_callback(info) {
        showsModel.clear();
        var model = info["shows"];
        for(var i = 0; i < model.length; i++) {
            showsModel.append({"mshowID": model[i]["showid"],
                              "mshowName": model[i]["title"],
                              "mshowSeason": model[i]["season_nro"],
                              "mshowEpisode": model[i]["episode_nro"],
                              "mshowDate": model[i]["next"] + " " + model[i]["airdate"],
                              "mairdate": model[i]["date"],
                              "mcurrent": model[i]["current"],
                              "mposter": model[i]["poster"],
                              "mdayOfWeek": model[i]["dayOfWeek"],
                              "mvisible": true});
        }
        root.hide_loading();
        main.load_sections();
    }

    function search_show() {
        Server.search_show(main.userTOKEN, root._temp_search, search_callback);
    }

    function search_callback(result) {
        if(result["showid"]){
            showsModel.append({"mshowID": result["showid"],
                              "mshowName": result["title"],
                              "mshowSeason": result["season_nro"],
                              "mshowEpisode": result["episode_nro"],
                              "mshowDate": result["next"] + " " + result["airdate"],
                              "mairdate": result["date"],
                              "mcurrent": result["current"],
                              "mposter": result["poster"],
                              "mdayOfWeek": result["dayOfWeek"],
                              "mvisible": true});
        }else if(result["multiple"]){
            root.multipleModel = result["shows"];
            PopupUtils.open(dialog);
        }else{
            root.error = result['error'];
            PopupUtils.open(dialogError);
        }
    }

    ShowDetails {
        id: details
        visible: false
        following: true
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
                    text: "<font color='white'>All Shows</font>"
                    property string value: "All"
                    control: Switch {
                        checked: root.selectedFilter[0] == listAll.value ? true : false
                        onClicked: {
                            root.selectedFilter = [listAll.value, "", ""];
                            popover.hide();
                            Filter.filter_all();
                        }
                    }
                }
                ListItem.Standard {
                    id: listCurrent
                    text: "<font color='white'>Current</font>"
                    property string value: "Current"
                    control: Switch {
                        checked: root.selectedFilter[0] == listCurrent.value ? true : false
                        onClicked: {
                            root.selectedFilter = [listCurrent.value, "", ""];
                            popover.hide();
                            Filter.filter_current();
                        }
                    }
                }
                ListItem.Standard {
                    id: listToday
                    text: "<font color='white'>Today Airdate</font>"
                    property string value: "Today"
                    control: Switch {
                        checked: root.selectedFilter[0] == listToday.value ? true : false
                        onClicked: {
                            root.selectedFilter = [listToday.value, "", ""];
                            popover.hide();
                            Filter.filter_today();
                        }
                    }
                }
                ListItem.Standard {
                    id: listDate
                    text: "<font color='white'>By Day of Week</font>"
                    property string value: "Date"
                    selected: root.selectedFilter[0] == listDate.value ? true : false
                    control: TextField {
                        id: textDate
                        width: units.gu(12)
                        placeholderText: "Monday"
                        text: root.selectedFilter[0] == listDate.value ? root.selectedFilter[1] : ""
                    }
                    progression: true
                    onClicked: {
                        root.selectedFilter = [listDate.value, textDate.text];
                        popover.hide();
                        Filter.filter_by_date(textDate.text);
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

                Keys.onEnterPressed: {
                    root._temp_search = text_search.text;
                    root.search_show();
                    text_search.focus = false;
                    text_search.text = "";
                    root._temp_search = "";
                }
            }

            Button {
                id: btnSearch
                text: root.width > units.gu(50) ? i18n.tr("Search") : ""
                height: text_search.height
                iconSource: "../img/search.png"

                onClicked: {
                    root._temp_search = text_search.text
                    root.search_show();
                    text_search.focus = false;
                    text_search.text = "";
                    root._temp_search = "";
                }

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
            model: showsModel
            Tile {
                showID: mshowID
                width: grid.width / grid.columns - grid.spacing
                height: 1.48 * width + root.tileInfoArea
                tileInfoArea: root.tileInfoArea
                showName: mshowName
                showSeason: mshowSeason
                showEpisode: mshowEpisode
                showDate: mshowDate
                airdate: mairdate
                current: mcurrent
                imageSource: Image {
                    asynchronous: true
                    source: mposter
                }
                visible: mvisible

                onClicked: {
                    details.showid = showID;
                    details.visible = true;
                }
            }
        }
    }
}
