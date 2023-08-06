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
Ext.define("LHCbDIRAC.AnalysisProductions.classes.Browser", {
  header: false,
  frame: false,

  extend: "Ext.panel.Panel",
  xtype: "tree-list",
  title: "TreeList",
  requires: [
    "Ext.layout.container.VBox",
    "LHCbDIRAC.AnalysisProductions.classes.ProductionView.ProdView",
    "LHCbDIRAC.AnalysisProductions.classes.ViewModel",
    "LHCbDIRAC.AnalysisProductions.classes.ProductionsTree.TreeModel",
    "LHCbDIRAC.AnalysisProductions.classes.ProductionsTree.Controller",
    "LHCbDIRAC.AnalysisProductions.classes.ProductionsTree.FiltersToolbar",
  ],

  layout: "border",

  viewModel: {
    type: "AnalysisProductions.classes.ViewModel",
  },

  items: [
    /*
      Display a tree browser on the left hand side of the application pane
    */
    {
      region: "west",
      width: 250,
      split: true,
      reference: "treelistContainer",
      layout: {
        type: "vbox",
        align: "stretch",
      },
      border: false,
      frame: false,
      scrollable: "y",
      controller: "AnalysisProductions.classes.ProductionsTree.Controller",
      items: [
        {
          xtype: "treelist",
          reference: "prodList",
          store: {
            model: "LHCbDIRAC.AnalysisProductions.classes.ProductionsTree.TreeModel",
            rootVisible: false,
            autoLoad: true,
            filterer: "bottomup",
            // listeners: {
            //   // TODO: updateTreeFilters should be called when "datachanged"
            // }
          },
          expanderOnly: false,
          expanderFirst: true,
          singleExpand: false,
          animation: null,
        },
      ],
      bbar: [
        {
          xtype: "AnalysisProductions.classes.ProductionsTree.FiltersToolbar",
          dock: "bottom",
        },
      ],
    },
    /*
      Display a data view as the central content
    */
    {
      region: "center",
      xtype: "panel",
      cls: ["ap-info-display-panel"],
      layout: {
        type: "vbox",
        align: "stretch",
      },
      scrollable: "y",
      reference: "productionPanelParent",
      bodyPadding: 0,
      items: [
        {
          xtype: "panel",
          border: false,
          html: [
            '<div class="ap-view-header">',
            '  <div class="ap-header">',
            '    <button onClick="apCopyPatternsAsJSON(this);">Copy output patterns as JSON dictionary</button>',
            // TODO: This requires caching of responses on the sever side to work well
            // '    <button onClick="alert();">Download all metadata</button>',
            "  </div>",
            "  <p>Click on a heading to see more details about a specific production</p>",
            "</div>",
          ],
        },
        {
          xtype: "AnalysisProductions.classes.ProductionView.ProdView",
          bind: {
            store: "{selectedProduction}",
          },
        },
      ],
    },
  ],
});
