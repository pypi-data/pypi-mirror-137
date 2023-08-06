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
/*
  Avoids "Uncaught TypeError: node is null" when selecting items in a filtered Ext.list.Tree

  See also: https://forum.sencha.com/forum/showthread.php?360408-Ext-list-Tree-updateOverItem-null-reference-when-removing-tree-node
*/
Ext.define("LHCbDIRAC.AnalysisProductions.overrides.list.Tree", {
  override: "Ext.list.Tree",
  updateOverItem: function (over, wasOver) {
    var map = {},
      state = 2,
      c,
      node;
    // Walk up the node hierarchy starting at the "over" item and set their "over"
    // config appropriately (2 when over that row, 1 when over a descendant).
    //
    for (c = over; c; c = this.getItem(node.parentNode)) {
      node = c.getNode();
      map[node.internalId] = true;
      c.setOver(state);
      state = 1;
    }
    if (wasOver) {
      // If we wasOver something else previously, walk up that node hierarchy and
      // set their "over" to 0... until we encounter some node that we are still
      // "over" (as determined in previous loop).
      //
      for (c = wasOver; c; c = this.getItem(node.parentNode)) {
        node = c.getNode();
        if (!node || map[node.internalId]) {
          break;
        }
        c.setOver(0);
      }
    }
  },
});
