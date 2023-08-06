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
/*******************************************************************************
 * It is the LHCb specific transformation monitor page.
 */
Ext.define("LHCbDIRAC.LHCbTransformationMonitor.classes.LHCbTransformationMonitor", {
  extend: "DIRAC.TransformationMonitor.classes.TransformationMonitor",

  initComponent: function () {
    var me = this;
    me.callParent();
    me.launcher.title = "LHCb Transformation Monitor";
    me.applicationsToOpen = {
      JobMonitor: "LHCbDIRAC.LHCbJobMonitor.classes.LHCbJobMonitor",
      ProductionRequestManager: "LHCbDIRAC.ProductionRequestManager.classes.ProductionRequestManager",
    };
  },
  buildUI: function () {
    var me = this;
    me.callParent();

    var menuItem = Ext.create("Ext.menu.Item", {
      text: "Run Status",
      handler: me.__runStatus,
      tooltip: "Click to show the run status of the selected transformation.",
      scope: me,
    });
    me.grid.contextMenu.add(menuItem);

    var showRequest = Ext.create("Ext.menu.Item", {
      text: "Show request",
      handler: me.__showRequest,
      tooltip: "Click to show the request.",
      scope: me,
    });
    me.grid.contextMenu.add(showRequest);
    me.grid.contextMenu.add({
      xtype: "menuseparator",
    });
    var hotproduction = Ext.create("Ext.menu.Item", {
      text: "Hot",
      menu: [
        {
          text: "Add",
          handler: me.__changeHotFlag.bind(me, true),
        },
        {
          text: "Remove",
          handler: me.__changeHotFlag.bind(me, false),
        },
      ],
    });

    me.grid.contextMenu.add(hotproduction);

    me.leftPanel.addTextFieldSelector({
      Hot: {
        name: "Hot",
        fieldLabel: "Show hot productions only",
        type: "checkbox",
      },
    });
  },
  __runStatus: function () {
    var me = this;
    var oId = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "TransformationID");

    me.grid.body.mask("Wait ...");

    var url = GLOBAL.BASE_URL + me.applicationName + "/showRunStatus";
    var params = {
      TransformationId: oId,
    };

    var oFields = [
      "Status",
      "LastUpdate",
      "Files_PercentProcessed",
      "TransformationID",
      "Files_Total",
      "Files_Assigned",
      "RunNumber",
      "SelectedSite",
      "Files_Problematic",
      "Files_Processed",
      "Files_ApplicationCrash",
      "Files_Unused",
      "Files_MaxReset",
      "LastUpdate",
    ];

    var oColumns = [
      {
        text: "RunNumber",
        flex: 1,
        sortable: true,
        dataIndex: "RunNumber",
      },
      {
        text: "Status",
        flex: 1,
        sortable: true,
        dataIndex: "Status",
      },
      {
        text: "Selected Site",
        flex: 1,
        sortable: true,
        dataIndex: "SelectedSite",
      },
      {
        text: "Files",
        flex: 1,
        sortable: true,
        dataIndex: "Files_Total",
      },
      {
        text: "Processed(%)",
        flex: 1,
        sortable: true,
        dataIndex: "Files_PercentProcessed",
      },
      {
        text: "Unused",
        flex: 1,
        sortable: true,
        dataIndex: "Files_Unused",
      },
      {
        text: "Assigned",
        flex: 1,
        sortable: true,
        dataIndex: "Files_Assigned",
      },
      {
        text: "Processed",
        flex: 1,
        sortable: true,
        dataIndex: "Files_Processed",
      },
      {
        text: "Problematic",
        flex: 1,
        sortable: true,
        dataIndex: "Files_Problematic",
      },
      {
        text: "Max Reset",
        flex: 1,
        sortable: true,
        dataIndex: "Files_MaxReset",
      },
      {
        text: "Last Update",
        flex: 1,
        sortable: true,
        dataIndex: "LastUpdate",
      },
    ];

    var oGrid = me.__createStatusGridPanel(oFields, oColumns, url, params);
    var oMenu = new Ext.menu.Menu({
      items: [
        {
          text: "Show Jobs",
          handler: me.__showJobs.bind(oGrid, me.grid, me),
        },
        {
          text: "Flush",
          handler: me.__flushRun.bind(oGrid, me.grid),
        },
        {
          text: "Set site",
          parent: me,
          listeners: {
            focus: function (item, eOpts) {
              // We can fill the submenu by using an AJAX request!
              item.setIconCls("loading_item");
              if (!item.menu.isLoaded) {
                Ext.Ajax.request({
                  url: GLOBAL.BASE_URL + me.applicationName + "/getTier1Sites",
                  scope: item,
                  failure: function (responseText) {
                    alert(responseText.statusText);
                  },
                  success: function (response) {
                    var me = this;
                    var response = Ext.JSON.decode(response.responseText);
                    if (response.success == true) {
                      for (var i = 0; i < response.data.length; i++) {
                        item.menu.add({
                          text: response.data[i],
                          handler: me.parent.__setSite.bind(oGrid, me.parent.grid, response.data[i]),
                        });
                      }
                    } else {
                      alert(response["errors"]);
                    }
                    item.menu.isLoaded = true;
                    item.setIconCls("undefined");
                  },
                  failure: function (response) {
                    GLOBAL.APP.CF.showAjaxErrorMessage(response);
                  },
                });
              } else {
                item.setIconCls("undefined");
              }
            },
          },
          menu: {
            isLoaded: false,
            items: [],
          },
        },
      ],
    });
    oGrid.menu = oMenu;
    me.getContainer().showInWindow("Run status for production:" + oId, oGrid);
    me.grid.body.unmask();
  },
  __showJobs: function (parentGrid, parentWidget) {
    var me = this;
    var oTransFormationId = GLOBAL.APP.CF.getFieldValueFromSelectedRow(parentGrid, "TransformationID");
    var oRunNumberId = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me, "RunNumber");
    var sTransformationId = GLOBAL.APP.CF.zfill(oTransFormationId, 8);
    var setupdata = {};
    setupdata.data = {};
    setupdata.currentState = oTransFormationId + "->" + oRunNumberId;
    setupdata.data.leftMenu = {};
    setupdata.data.leftMenu.selectors = {};
    setupdata.data.leftMenu.selectors.jobGroup = {
      data_selected: [sTransformationId],
      hidden: false,
      not_selected: false,
    };
    setupdata.data.leftMenu.RunNumbers = oRunNumberId;
    GLOBAL.APP.MAIN_VIEW.createNewModuleContainer({
      objectType: "app",
      moduleName: parentWidget.applicationsToOpen["JobMonitor"],
      setupData: setupdata,
    });
  },
  __showRequest: function () {
    var me = this;
    var oId = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "TransformationFamily");
    var setupdata = {
      data: {
        leftMenu: {
          idF: oId,
        },
      },
      currentState: oId,
    };

    GLOBAL.APP.MAIN_VIEW.createNewModuleContainer({
      objectType: "app",
      moduleName: me.applicationsToOpen["ProductionRequestManager"],
      setupData: setupdata,
    });
  },
  __changeHotFlag: function (hotFlag) {
    var me = this;
    var id = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "TransformationID");
    Ext.Ajax.request({
      method: "POST",
      params: {
        Production: id,
        Hot: hotFlag,
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
      success: function (response) {
        var response = Ext.JSON.decode(response.responseText);
        if (response.success == true) {
          Ext.dirac.system_info.msg("Notification", "The hot flag of the transformation" + response["result"] + " has changed!");
          me.grid.getStore().reload();
        } else {
          alert(response["error"]);
        }
      },
      url: GLOBAL.BASE_URL + me.applicationName + "/changeHotFlag",
    });
  },
});
