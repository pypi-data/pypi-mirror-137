/*****************************************************************************\
* (c) Copyright 2020 CERN for the benefit of the LHCb Collaboration           *
*                                                                             *
* This software is distributed under the terms of the GNU General Public      *
* Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   *
*                                                                             *
* In applying this licence, CERN does not waive the privileges and immunities *
* granted to it by virtue of its status as an Intergovernmental Organization  *
* or submit itself to any jurisdiction.                                       *
\*****************************************************************************/
/***
 * Application used for viewing analysis productions.
 */
Ext.define("LHCbDIRAC.AnalysisProductions.classes.AnalysisProductions", {
  extend: "Ext.dirac.core.Module",
  xtype: "layout-border",
  requires: [
    "LHCbDIRAC.AnalysisProductions.overrides.list.Tree",
    "LHCbDIRAC.AnalysisProductions.overrides.list.RootTreeItem",
    "Ext.layout.container.Border",
    "LHCbDIRAC.AnalysisProductions.classes.Browser",
  ],
  layout: "border",

  bodyBorder: false,

  defaults: {
    collapsible: true,
    split: true,
    bodyPadding: 0,
  },

  buildUI: function () {
    var me = this;
    me.mainContent = Ext.create("LHCbDIRAC.AnalysisProductions.classes.Browser", {
      region: "center",
    });
    me.launcher.title = "Analysis Productions";
    me.add([me.mainContent]);

    // Reconfigure the dataview load mask to cover the entire application
    Ext.ComponentQuery.query("dataview", me.mainContent)[0].loadMask = new Ext.LoadMask({
      msg: "Please wait...",
      target: me.mainContent,
      store: Ext.ComponentQuery.query("tree-list")[0].viewModel.getStore("selectedProduction"),
    });
  },
});
