import QtQuick 2.0
import QtWebKit 3.0
import Ubuntu.Components 0.1
import "components"
//import U1db 1.0 as U1db

/*!
    \brief MainView with a Label and Button elements.
*/

MainView {
    id: main
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

//    U1db.Database {
//            id: aDatabase
//            path: "tvstalkerdb"
//    }

    Tabs {
        id: tabs
        anchors.fill: parent
        Tab {
            id: login
            title: "<font color='white'><b>Tv</font><font color='lightblue'>Stalker</b></font> Login"
            page: Login {
                onLogin: {
                    tabs.tabChildren = [home, friends, recommended, explore];
                }
            }
            /*Page {
                WebView {
                        id: webview
                        url: "http://tabugame.org/accounts/login/"
                        width: parent.width
                        height: parent.height
                        onNavigationRequested: {
                            // detect URL scheme prefix, most likely an external link
                            var schemaRE = /^\w+:/;
                            if (schemaRE.test(request.url)) {
                                request.action = WebView.AcceptRequest;
                            } else {
                                request.action = WebView.IgnoreRequest;
                                // delegate request.url here
                            }
                        }
                    }
            }*/


        }

        onSelectedTabIndexChanged: {
            if(selectedTabIndex == 2){
                console.log("diegooooooo");
            }
        }

    }

    Tab {
        id: home
        title: "<font color='white'><b>Tv</font><font color='lightblue'>Stalker</b></font>"
        page: Home {}
    }

    Tab {
        id: friends
        title: "<font color='white'><b>Fr</font><font color='lightblue'>iends</b></font>"
        page: Friends {}
    }

    Tab {
        id: recommended
        title: "<font color='white'><b>Re</font><font color='lightblue'>commended</b></font>"
        page: Recommended {}
    }

    Tab {
        id: explore
        title: "<font color='white'><b>Ex</font><font color='lightblue'>plore</b></font>"
        page: Explore {}
    }

}
