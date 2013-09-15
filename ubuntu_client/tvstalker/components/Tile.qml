import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem

UbuntuShape {
    id: tile
    color: "#24262c"

    property int showID: 0
    property alias imageSource: img.image
    property int tileInfoArea: 0
    property int _tileBorders: units.gu(2)
    property alias date: label_date.text
    property alias showName: label_name.text
    property string showSeason: ""
    property string showEpisode: ""
    property string showDate: ""
    property string airdate: ""
    property bool current: false

    signal clicked(string name, int season, int episode, string date, string imagePath)

    MouseArea {
        anchors.fill: parent

        onClicked: tile.clicked(tile.showName, tile.showSeason, tile.showEpisode, tile.showDate, tile.imageSource.source)
    }

    UbuntuShape {
        id: img
        color: "#33363b"
        width: parent.width - tile._tileBorders
        height: parent.height - tile.tileInfoArea - tile._tileBorders
        anchors {
            left: parent.left
            top: parent.top
            leftMargin: units.gu(1)
            topMargin: units.gu(1)
        }
    }

    Label {
        id: label_name
        text: ""
        visible: text ? true : false
        color: "lightblue"
        fontSize: "medium"
        font.bold: true
        font.underline: true
        opacity: .9
        style: Text.Raised
        styleColor: "black"
        wrapMode: Text.WrapAtWordBoundaryOrAnywhere

        anchors {
            left: parent.left
            right: parent.right
            top: img.bottom
            margins: units.gu(1)
        }
    }

    Label {
        id: label_episode
        text: i18n.tr("Season: ") + showSeason + i18n.tr("  |  Episode: ") + showEpisode
        visible: showSeason && showEpisode ? true : false
        color: "lightblue"
        fontSize: "medium"
        font.bold: true
        opacity: .9
        style: Text.Raised
        styleColor: "black"
        wrapMode: Text.WrapAtWordBoundaryOrAnywhere

        anchors {
            left: parent.left
            right: parent.right
            top: label_name.bottom
            leftMargin: units.gu(1)
        }
    }

    ListItem.ThinDivider {
        id: divider
        anchors {
            left: parent.left
            right: parent.right
            top: label_episode.bottom
            topMargin: units.gu(1)
        }
        visible: tile.showDate ? true : false
    }

    UbuntuShape {
        color: "#1a1b1f"
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
            top: divider.bottom
        }
        visible: tile.showDate ? true : false

        Label {
            id: label_date
            text: showDate
            visible: text ? true : false
            color: "white"
            fontSize: "medium"
            opacity: .9
            style: Text.Raised
            styleColor: "black"
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter

            anchors.fill: parent
            anchors.margins: units.gu(1)
        }
    }
}
