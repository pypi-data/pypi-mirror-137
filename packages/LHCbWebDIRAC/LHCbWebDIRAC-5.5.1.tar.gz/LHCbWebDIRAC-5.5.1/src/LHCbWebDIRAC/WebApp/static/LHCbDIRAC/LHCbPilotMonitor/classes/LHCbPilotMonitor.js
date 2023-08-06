/*****************************************************************************\
* (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           *
*                                                                             *
* This software is distributed under the terms of the GNU General Public      *
* Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   *
*                                                                             *
* In applying this licence, CERN does not waive the privileges and immunities *
* granted to it by virtue of its status as an Intergovernmental Organization  *
* or submit itself to any jurisdiction.                                       *
\*****************************************************************************/
/**
 * It is used to open the LHCb specific JobMonitor application
 */
Ext.define("LHCbDIRAC.LHCbPilotMonitor.classes.LHCbPilotMonitor", {
  extend: "DIRAC.PilotMonitor.classes.PilotMonitor",
  initComponent: function () {
    var me = this;
    me.callParent();
    me.launcher.title = "LHCb Pilot Monitor";
    me.applicationsToOpen = {
      JobMonitor: "LHCbDIRAC.LHCbJobMonitor.classes.LHCbJobMonitor",
    };
  },
});
