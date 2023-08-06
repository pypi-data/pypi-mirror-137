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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.StepsView", {
  extend: "Ext.panel.Panel",

  defaults: {
    bodyStyle: {
      background: "#E0E0E0",
      padding: "10px",
    },
  },
  initComponent: function () {
    var me = this;
    Ext.apply(me, {
      items: {
        baseCls: "x-plain",
        html: "",
      },
    });
    me.callParent(arguments);
  },

  updateDetail: function (data) {
    var me = this;
    var items = [];

    for (var i = 1; i < 20; ++i) {
      html = data["p" + i + "Html"];
      if (!html) break;
      items.push({
        width: 530,
        html: html,
        bodyStyle: {
          background: "#CCFFFF",
          padding: "10px",
        },
      });
      if (me.change_show)
        items.push({
          xtype: "button",
          text: "Replace",
          stepId: i,
          handler: me.change_handler,
          scope: me.change_scope,
          bodyStyle: {
            background: "#33CCFF",
            padding: "10px",
          },
        });
      else
        items.push({
          html: "",
        });
    }
    me.remove(0);

    if (items.length)
      me.add(
        Ext.apply({
          layout: {
            type: "table",
            columns: 2,
          },
          items: items,
        })
      );
    else
      me.add(
        Ext.apply({
          baseCls: "x-plain",
          html: "",
        })
      );
  },
});
