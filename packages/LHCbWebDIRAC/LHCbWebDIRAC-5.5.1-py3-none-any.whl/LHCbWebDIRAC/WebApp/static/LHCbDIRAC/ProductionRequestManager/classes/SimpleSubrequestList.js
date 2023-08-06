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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.SimpleSubrequestList", {
  extend: "Ext.grid.Panel",

  initComponent: function () {
    var me = this;

    me.store = Ext.create("Ext.data.JsonStore", {
      remoteSort: false,
      fields: [
        {
          name: "ID",
          type: "auto",
        },
        {
          name: "eventType",
        },
        {
          name: "eventNumber",
        },
        {
          name: "eventBK",
        },
        {
          name: "progress",
        },
        {
          name: "eventText",
        },
      ],
      proxy: {
        type: "ajax",
        url: GLOBAL.BASE_URL + "ProductionRequestManager/list",
        reader: {
          type: "json",
          rootProperty: "result",
        },
        listeners: {
          exception: function (proxy, response, operation) {
            GLOBAL.APP.CF.showAjaxErrorMessage(response);
          },
        },
      },
    });

    me.store.sort("ID", "ASC");

    me.checkboxFunctionDefinition = '<input type="checkbox" value="" onchange="';
    me.checkboxFunctionDefinition += "var oChecked=this.checked;";
    me.checkboxFunctionDefinition += "var oElems=Ext.query('#" + me.id + " input.checkrow');";
    me.checkboxFunctionDefinition += "for(var i=0;i<oElems.length;i++)oElems[i].checked = oChecked;";
    me.checkboxFunctionDefinition += '" class="dirac-table-main-check-box"/>';

    Ext.apply(me, {
      columns: [
        {
          header: me.checkboxFunctionDefinition,
          name: "Id",
          dataIndex: "ID",
          hideable: false,
          fixed: true,
          menuDisabled: true,
          align: "center",
          width: 36,
          sortable: false,
          renderer: function (val) {
            return '<input value="' + val + '" type="checkbox" class="checkrow" style="margin:0px;padding:0px"/>';
          },
        },
        {
          header: "Id",
          name: "Id",
          sortable: true,
          dataIndex: "ID",
        },
        {
          header: "Event type",
          sortable: true,
          dataIndex: "eventType",
        },
        {
          header: "",
          dataIndex: "eventText",
        },
        {
          header: "Events requested",
          sortable: true,
          dataIndex: "eventNumber",
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
    });
    me.callParent(arguments);
  },
});
