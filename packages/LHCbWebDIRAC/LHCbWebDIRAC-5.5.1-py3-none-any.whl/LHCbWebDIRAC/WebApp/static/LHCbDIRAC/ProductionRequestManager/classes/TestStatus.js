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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.TestStatus", {
  extend: "Ext.grid.Panel",

  initComponent: function () {
    var me = this;

    me.store = Ext.create("Ext.data.JsonStore", {
      fields: ["RequestID", "State", "Actual", "Link", "Time"],
      remoteSort: true,
      proxy: {
        type: "ajax",
        extraParams: { RequestID: me.pData.ID },
        url: GLOBAL.BASE_URL + "ProductionRequestManager/test_list",
        reader: {
          type: "json",
          rootProperty: "result",
        },
      },
    });

    me.pagingBar = new Ext.PagingToolbar({
      pageSize: 150,
      store: me.store,
      displayInfo: true,
      displayMsg: "Displaying {0} - {1} of {2}",
      emptyMsg: "No sutable steps found",
    });

    me.store.sort("RequestID", "ASC");
    //me.store.load();

    Ext.apply(this, {
      columns: [
        {
          header: "(Sub)Request",
          sortable: true,
          dataIndex: "RequestID",
        },
        {
          header: "State",
          sortable: true,
          dataIndex: "State",
          renderer: me.renderState,
        },
        {
          header: "Actual",
          sortable: true,
          dataIndex: "Actual",
          renderer: me.renderActual,
        },
        {
          header: "Link",
          sortable: true,
          dataIndex: "Link",
        },
        {
          header: "Time",
          sortable: true,
          dataIndex: "Time",
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
  renderActual: function (val) {
    if (val == null) return "";
    if (val == "0") return "No";
    return "Yes";
  },
  renderState: function (val) {
    if (val == null) return "Not tested";
    return val;
  },
});
