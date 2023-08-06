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
Ext.define("LHCbDIRAC.AnalysisProductions.classes.ProductionsTree.TreeModel", {
  extend: "Ext.data.TreeModel",
  fields: [
    { name: "name", type: "string" },
    { name: "requestIDs", type: "string", defaultValue: "[]" },
    { name: "archived", type: "boolean" },
    { name: "published", type: "boolean" },
    // Generic attributes
    { name: "iconCls", defaultValue: null },
    { name: "text", type: "string", mapping: "name" },
  ],
  proxy: {
    type: "ajax",
    url: GLOBAL.BASE_URL + "AnalysisProductions/listProductions",
  },
});
