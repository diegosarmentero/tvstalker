import QtQuick 2.0
import Ubuntu.Components 0.1

Base {
    id: root

    signal login

    body: Column {
        id: col
        spacing: units.gu(6)
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            topMargin: units.gu(4)
            rightMargin: units.gu(6)
            leftMargin: units.gu(6)
        }

        Label {
            text: i18n.tr("<b>Follow your Tv Shows, check the airdates, share your shows with your friends and never miss an episode again!</b>")
            fontSize: "large"
            smooth: true
            width: parent.width
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            color: "white"
            opacity: .9
            style: Text.Raised
            styleColor: "black"
        }

        UbuntuShape {
            id: login_background
            color: "#24262c"
            height: col_login.height + units.gu(4)
            width: parent.width
            Column {
                id: col_login
                spacing: units.gu(2)
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                    topMargin: units.gu(2)
                    leftMargin: units.gu(2)
                    rightMargin: units.gu(2)
                }
                add: Transition {
                     NumberAnimation {
                         properties: "y"
                         easing.type: Easing.OutBounce
                     }
                 }

                Label {
                    text: i18n.tr("Username")
                    fontSize: "large"
                    color: Theme.palette.normal.baseText
                    opacity: .6
                    style: Text.Raised
                    styleColor: "black"
                }

                TextField {
                    id: text_username
                    width: col_login.width
                    hasClearButton: true
                    placeholderText: "Username"
                }

                Label {
                    text: i18n.tr("Password")
                    fontSize: "large"
                    color: Theme.palette.normal.baseText
                    opacity: .6
                    style: Text.Raised
                    styleColor: "black"
                }

                TextField {
                    id: text_password
                    width: col_login.width
                    hasClearButton: true
                    placeholderText: "Password"
                    echoMode: TextInput.Password
                }

                Loader {
                    id: loader
                    visible: check.checked ? true : false;
                    sourceComponent: check.checked ? register_component : undefined

                    Component {
                        id: register_component

                        Column {
                            spacing: units.gu(2)
                            Label {
                                text: i18n.tr("Re-type Password")
                                fontSize: "large"
                                color: Theme.palette.normal.baseText
                                opacity: .6
                                style: Text.Raised
                                styleColor: "black"
                            }

                            TextField {
                                id: text_password
                                width: col_login.width
                                hasClearButton: true
                                placeholderText: "Password"
                                echoMode: TextInput.Password
                            }

                            Label {
                                text: i18n.tr("Email")
                                fontSize: "large"
                                color: Theme.palette.normal.baseText
                                opacity: .6
                                style: Text.Raised
                                styleColor: "black"
                            }

                            TextField {
                                id: text_username
                                width: col_login.width
                                hasClearButton: true
                                placeholderText: "email@email.com"
                            }
                        }
                    }
                }

                Row {
                    spacing: units.gu(2)

                    CheckBox {
                        id: check
                        checked: false

                        onCheckedChanged: {
                            if(checked) {
                                button.text = i18n.tr("Register");
                            } else {
                                button.text = i18n.tr("Login");
                                loader.y = 0;
                            }
                        }
                    }
                    Label {
                        text: i18n.tr("New User?")
                        fontSize: "large"
                        color: Theme.palette.normal.baseText
                        opacity: .6
                        style: Text.Raised
                        styleColor: "black"
                        verticalAlignment: Text.AlignVCenter
                        height: check.height
                    }
                }

                Button {
                    id: button
                    anchors.right: parent.right
                    text: i18n.tr("Login")

                    onClicked: root.login();
                }
            }
        }
    }

}
