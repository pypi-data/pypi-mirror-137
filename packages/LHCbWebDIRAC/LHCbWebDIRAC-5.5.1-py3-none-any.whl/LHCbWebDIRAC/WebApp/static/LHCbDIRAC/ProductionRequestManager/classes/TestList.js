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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.TestList", {
  extend: "Ext.grid.Panel",

  initComponent: function () {
    var me = this;

    me.store = Ext.create("Ext.data.JsonStore", {
      remoteSort: false,
      fields: ["WFName"],
      proxy: {
        type: "ajax",
        url: GLOBAL.BASE_URL + "ProductionRequestManager/templates",
        reader: {
          type: "json",
          rootProperty: "result",
        },
      },
    });

    me.store.load();

    Ext.apply(this, {
      columns: [
        {
          header: "Template",
          sortable: true,
          dataIndex: "WFName",
          renderer: function (value) {
            return value.replace(/_wizard\.py/, "");
          },
        },
      ],
      autoHeight: false,
      autoWidth: true,
      loadMask: true,
      region: "center",
      store: me.store,
      stripeRows: true,
      viewConfig: {
        forceFit: true,
      },
      bbar: me.pagingBar,
    });
    me.callParent(arguments);
  },
});
