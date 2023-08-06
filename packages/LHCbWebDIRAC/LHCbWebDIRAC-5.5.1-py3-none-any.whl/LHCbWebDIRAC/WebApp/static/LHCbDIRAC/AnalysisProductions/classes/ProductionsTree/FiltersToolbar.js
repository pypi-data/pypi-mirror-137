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
Ext.define("LHCbDIRAC.AnalysisProductions.classes.ProductionsTree.FiltersToolbar", {
  extend: "Ext.toolbar.Toolbar",
  alias: "widget.AnalysisProductions.classes.ProductionsTree.FiltersToolbar",
  vertical: true,
  border: false,
  items: [
    {
      xtype: "checkbox",
      boxLabel: "Show Archived",
      reference: "filterShowArchived",
      value: true, // TODO: This should be false but the datachanged listener is needed
      handler: "updateTreeFilters",
    },
    {
      xtype: "textfield",
      boxLabel: "Filter",
      label: "Filter",
      reference: "filterTextField",
      listeners: {
        change: {
          buffer: 100, // Fire at most 10 times per second
          fn: "updateTreeFilters",
        },
      },
    },
  ],
});
