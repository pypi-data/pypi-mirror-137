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
Ext.define("LHCbDIRAC.BookkeepingBrowser.classes.ProcessingPassViewer", {
  extend: "Ext.panel.Panel",
  layout: "border",
  defaults: {
    collapsible: true,
    split: true,
  },
  url: "",
  params: "",
  dataFields: [
    {
      name: "StepId",
      type: "int",
    },
    {
      name: "StepName",
    },
    {
      name: "ApplicationName",
    },
    {
      name: "ApplicationVersion",
    },
    {
      name: "OptionFiles",
    },
    {
      name: "ExtraPackages",
    },
    {
      name: "DDDB",
    },
    {
      name: "CONDDB",
    },
    {
      name: "Visible",
    },
  ],
  initComponent: function () {
    var me = this;
    me.callParent(arguments);
    var ajaxProxy = Ext.create("Ext.dirac.utils.DiracAjaxProxy", {
      url: me.url,
      extraParams: me.params,
    });
    me.dataStore = Ext.create("Ext.dirac.utils.DiracJsonStore", {
      autoLoad: false,
      remoteSort: false,
      dontLoadOnCreation: true,
      groupField: "StepName",
      proxy: ajaxProxy,
      fields: me.dataFields,
      scope: me,
      sorters: [
        {
          property: "StepId",
          direction: "DESC",
        },
      ],
    });

    var columns = {
      StepId: {
        dataIndex: "StepId",
        properties: {
          width: 80,
          hidden: false,
        },
      },
      "Step Name": {
        dataIndex: "StepName",
        properties: {
          width: 200,
        },
      },
      "Application Name": {
        dataIndex: "ApplicationName",
        properties: {
          hidden: false,
        },
      },
      "Application Version": {
        dataIndex: "ApplicationVersion",
      },
      "Option Files": {
        dataIndex: "OptionFiles",
      },
      "Extra Packages": {
        properties: {
          hidden: false,
        },
        dataIndex: "ExtraPackages",
      },
      DDDB: {
        properties: {
          hidden: false,
        },
        dataIndex: "DDDB",
      },
      CONDDB: {
        properties: {
          hidden: false,
        },
        dataIndex: "CONDDB",
      },
      Visible: {
        properties: {
          hidden: false,
        },
        dataIndex: "Visible",
      },
    };
    me.fileGrid = Ext.create("Ext.dirac.utils.DiracGridPanel", {
      store: me.dataStore,
      oColumns: columns,
      stateful: true,
      stateId: "BookkeepingProcessingPassView",
      scope: me,
      viewConfig: {
        stripeRows: true,
        enableTextSelection: true,
      },
      features: [
        {
          ftype: "grouping",
        },
      ],
      region: "center",
      listeners: {
        load: function (tore, operation, eOpts) {
          me.parentMenu.parent.getContainer().body.unmask();
        },
      },
    });

    /* me.fileGrid.store.proxy.extraParams = {
          stepName : me.parentMenu.stepName
        };*/
    me.fileGrid.store.load();
    me.add([me.fileGrid]);
  },
});
