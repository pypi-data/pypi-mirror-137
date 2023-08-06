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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.RequestDetail", {
  extend: "Ext.panel.Panel",

  tplSimMarkup: [
    "<b>ID:</b> {ID}<br/>",
    "<b>Name:</b> {reqName}<br/>",
    "<b>Type:</b> {reqType}<br/>",
    "<b>State:</b> {reqState}<br/>",
    "<b>Priority:</b> {reqPrio}<br/>",
    "<b>Author:</b> {reqAuthor} <b>WG:</b> {reqWG}<br/>",

    "<b>Event type:</b> {eventType} {eventText}<br/>",
    "<b>Number of events:</b> {eventNumber}<br/>",
    "{htmlTestState}",
    "<br>",

    "<b>Simulation Conditions:</b> {simDesc}<br/>",
    "<b>Beam:</b> {BeamCond} ",
    "<b>Beam energy:</b> {BeamEnergy} ",
    "<b>Generator:</b> {Generator} ",
    "<b>G4 settings:</b> {G4settings}<br/>",
    "<b>Magnetic field:</b> {MagneticField} ",
    "<b>Detector:</b> {DetectorCond} ",
    "<b>Luminosity:</b> {Luminosity}<br/><br/>",
    "<b>Processing Pass:</b> {pDsc}<br/>",
    "<b>MC Version:</b> {mcConfigVersion}<br/>",
    "{p1Html}{p2Html}{p3Html}{p4Html}",
    "{p5Html}{p6Html}{p7Html}{p8Html}{p9Html}",
    "{p10Html}{p11Html}{p12Html}{p13Html}{p14Html}",
    "{p15Html}{p16Html}{p17Html}{p18Html}{p19Html}<br/>",
    "<b>Inform also:</b> {reqInform}<br/><br/>",
    "<b>Comments</b><br/> {htmlReqComment}<br/>",
  ],

  tplRunMarkup: [
    "<b>ID:</b> {ID}<br/>",
    "<b>Name:</b> {reqName}<br/>",
    "<b>Type:</b> {reqType}<br/>",
    "<b>State:</b> {reqState}<br/>",
    "<b>Priority:</b> {reqPrio}<br/>",
    "<b>Author:</b> {reqAuthor}<br/>",

    "<b>Event type:</b> {eventType} {eventText}<br/>",
    "<b>Number of events:</b> {eventNumber}<br/><br>",

    "<b>Configuration:</b> {configName} <b>version:</b> {configVersion}<br>",
    "<b>Conditions:</b> {simDesc} <b>type:</b> {condType}<br/>",
    "<b>Processing pass:</b> {inProPass}<br/>",
    "<b>Input file type:</b> {inFileType}<br/>",
    "<b>DQ flag:</b> {inDataQualityFlag}<br/>",
    "<b>Input production:</b> {inProductionID}<br/>",
    "<b>TCKs:</b> {inTCKs}<br/><br/>",

    "<b>Processing Pass:</b> {pDsc}<br/>",
    "{p1Html}{p2Html}{p3Html}{p4Html}",
    "{p5Html}{p6Html}{p7Html}{p8Html}{p9Html}",
    "{p10Html}{p11Html}{p12Html}{p13Html}{p14Html}",
    "{p15Html}{p16Html}{p17Html}{p18Html}{p19Html}<br/>",

    "<b>Inform also:</b> {reqInform}<br/><br/>",
    "<b>Comments</b><br/> {htmlReqComment}<br/>",
  ],

  initComponent: function () {
    var me = this;
    me.tplSim = new Ext.Template(me.tplSimMarkup);
    me.tplRun = new Ext.Template(me.tplRunMarkup);
    me.callParent(arguments);
  },

  updateDetail: function (data) {
    var me = this;
    var eol = /\n/g;
    data.htmlReqComment = data.reqComment.replace(eol, "<br/>");
    if (data._is_leaf) data.htmlTestState = "<b>Test state:</b> " + data.TestState + "<br/>";
    else data.htmlTestState = "";
    if (data.reqType == "Simulation") {
      me.tplSim.overwrite(me.body, data);
    } else me.tplRun.overwrite(me.body, data);
  },

  onDataChanged: function (store) {
    var me = this;
    if (me.IDs) {
      for (var i = 0; i < me.IDs.length; ++i) {
        var nr = store.getAt(
          store.findBy(function (record, key) {
            var data = record.getData();
            if (data.ID == me.IDs[me.IDs.length - 1 - i]) {
              return true;
            }
            return false;
          })
        );

        if (!nr) {
          // !!! alert(this.IDs[this.IDs.length-1-i])
          return;
        }
        if (!r) r = nr.copy();
        else {
          if (nr.data.eventType) r.set("eventType", nr.data.eventType);
          if (nr.data.eventNumber) r.set("eventNumber", nr.data.eventNumber);
          if (nr.data.reqComment) r.set("reqComment", r.data.reqComment + "\n" + nr.data.reqComment);
          if (nr.data._is_leaf) r.set("_is_leaf", nr.data._is_leaf);
        }
      }
    } else {
      if (typeof me.ID == "undefined") return;
      var idx = store.find("ID", this.ID);
      if (idx >= 0) var r = store.getAt(idx);
    }
    if (typeof r != "undefined") me.updateDetail(r.data);
  },
});
