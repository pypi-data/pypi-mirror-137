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
Ext.define("LHCbDIRAC.AnalysisProductions.classes.ViewModel", {
  extend: "Ext.app.ViewModel",
  requires: ["LHCbDIRAC.AnalysisProductions.classes.ProductionView.ProdModel"],

  alias: "viewmodel.AnalysisProductions.classes.ViewModel",

  stores: {
    selectedProduction: {
      model: "LHCbDIRAC.AnalysisProductions.classes.ProductionView.ProdModel",
      autoLoad: true,
      proxy: {
        type: "ajax",
        url: GLOBAL.BASE_URL + "AnalysisProductions/getProduction",
        timeout: 600000, // 10 minuites
        reader: {
          type: "json",
        },
        extraParams: {
          requestIDs: "{selectedRequestIDs}",
        },
      },
      updateProxy: function (proxy) {
        proxy.onAfter("extraparamschanged", this.load, this);
      },
    },
  },

  formulas: {
    selectedRequestIDs: function (get) {
      var selection = get("prodList.selection");
      if (selection) {
        return selection.get("requestIDs");
      } else {
        return Ext.JSON.encode([]);
      }
    },
  },
});
