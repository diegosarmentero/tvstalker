import QtQuick 2.0
import Ubuntu.Components 0.1
import "components"

/*!
    \brief MainView with a Label and Button elements.
*/

MainView {
    id: main
    // objectName for functional testing purposes (autopilot-qt5)
    objectName: "TvStalker"
    state: "login"
    
    // Note! applicationName needs to match the .desktop filename
    applicationName: "TvStalker"
    backgroundColor: "#33363b"
    
    /* 
     This property enables the application to change orientation 
     when the device is rotated. The default is false.
    */
    automaticOrientation: true
    
    width: units.gu(100)
    height: units.gu(75)

    property string userTOKEN: ""
    
    Tabs {
        id: tabs
        anchors.fill: parent
        Tab {
            id: login
            title: "<font color='white'><b>Tv</font><font color='lightblue'>Stalker</b></font> Login"
            page: Login {
                id: loginPage
                onLogin: {
                    main.userTOKEN = token;
                    tabs.selectedTabIndex = 1;
                    home.page.show_loading();
                    home.page.init_user();
                    home.page.load_shows();
                    loginPage.enabled = false;
                    homePage.enabled = true;
                    recommendPage.enabled = true;
                    explorePage.enabled = true;
                }
            }
        }

        Tab {
            id: home
            title: i18n.tr("<font color='white'><b>Tv</font><font color='lightblue'>Stalker</b></font>")
            page: Home {
                id: homePage
                enabled: false
            }
        }

    //    Tab {
    //        id: friends
    //        title: i18n.tr("<font color='white'><b>Fr</font><font color='lightblue'>iends</b></font>")
    //        page: Friends {}
    //    }

        Tab {
            id: recommended
            title: "<font color='white'><b>Re</font><font color='lightblue'>commended</b></font>"
            page: Recommended {
                id: recommendPage
                enabled: false
            }
        }

        Tab {
            id: explore
            title: "<font color='white'><b>Ex</font><font color='lightblue'>plore</b></font>"
            page: Explore {
                id: explorePage
                enabled: false
            }
        }
    }

    function load_sections() {
        explorePage.load_explore();
        recommendPage.load_recommend();
    }

    function reload_shows(){
        homePage.load_shows();
    }
}
