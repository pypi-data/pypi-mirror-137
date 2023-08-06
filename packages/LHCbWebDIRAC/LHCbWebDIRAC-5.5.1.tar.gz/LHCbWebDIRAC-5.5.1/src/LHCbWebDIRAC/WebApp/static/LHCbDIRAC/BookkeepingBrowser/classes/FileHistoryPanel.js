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
Ext.define("LHCbDIRAC.BookkeepingBrowser.classes.FileHistoryPanel", {
  extend: "Ext.panel.Panel",
  layout: "border",
  defaults: {
    collapsible: true,
    split: true,
  },
  dataFields: [
    {
      name: "NumberofEvents",
    },
    {
      name: "TotalLuminosity",
    },
    {
      name: "StatisticsRequested",
    },
    {
      name: "Name",
    },
    {
      name: "WNMEMORY",
    },
    {
      name: "ExecTime",
    },
    {
      name: "FirstEventNumber",
    },
    {
      name: "CPUTime",
    },
    {
      name: "WNCPUPOWER",
    },
    {
      name: "EventInputStat",
    },
    {
      name: "Location",
    },
    {
      name: "DiracJobID",
    },
    {
      name: "WORKERNODE",
    },
    {
      name: "WNCPUHS06",
    },
    {
      name: "WNCACHE",
    },
    {
      name: "WNMODEL",
    },
  ],
  commands: [],
  current: -1,
  initComponent: function () {
    var me = this;
    me.callParent(arguments);

    var ajaxProxy = Ext.create("Ext.dirac.utils.DiracAjaxProxy", {
      url: GLOBAL.BASE_URL + me.applicationName + "/ancestors",
    });

    me.dataStore = Ext.create("Ext.dirac.utils.DiracJsonStore", {
      autoLoad: false,
      remoteSort: false,
      dontLoadOnCreation: true,
      proxy: ajaxProxy,
      fields: [
        {
          name: "FileId",
          type: "int",
        },
        {
          name: "FileName",
        },
        {
          name: "ADLER32",
        },
        {
          name: "CreationDate",
        },
        {
          name: "EventStat",
        },
        {
          name: "Eventtype",
        },
        {
          name: "Gotreplica",
        },
        {
          name: "GUI",
        },
        {
          name: "JobId",
          type: "int",
        },
        {
          name: "md5sum",
        },
        {
          name: "FileSize",
        },
        {
          name: "FullStat",
        },
        {
          name: "Dataquality",
        },
        {
          name: "FileInsertDate",
        },
        {
          name: "Luminosity",
        },
        {
          name: "InstLuminosity",
        },
      ],
      scope: me,
      sorters: [
        {
          property: "FileName",
          direction: "DESC",
        },
      ],
    });

    var columns = {
      FileId: {
        dataIndex: "FileId",
        properties: {
          width: 40,
          hidden: true,
        },
      },
      FileName: {
        dataIndex: "FileName",
        properties: {
          width: 200,
        },
      },
      ADLER32: {
        dataIndex: "ADLER32",
        properties: {
          hidden: true,
        },
      },
      CreationDate: {
        dataIndex: "CreationDate",
      },
      EventStat: {
        dataIndex: "EventStat",
      },
      Gotreplica: {
        properties: {
          hidden: true,
        },
        dataIndex: "Gotreplica",
      },
      GUI: {
        properties: {
          hidden: true,
        },
        dataIndex: "GUI",
      },
      JobId: {
        properties: {
          hidden: true,
        },
        dataIndex: "JobId",
      },
      md5sum: {
        properties: {
          hidden: true,
        },
        dataIndex: "md5sum",
      },
      FileSize: {
        dataIndex: "FileSize",
      },
      FullStat: {
        dataIndex: "FullStat",
      },
      Dataquality: {
        dataIndex: "Dataquality",
      },
      FileInsertDate: {
        dataIndex: "FileInsertDate",
        properties: {
          hidden: true,
        },
      },
      Luminosity: {
        dataIndex: "Luminosity",
        properties: {
          hidden: true,
        },
      },
      InstLuminosity: {
        dataIndex: "InstLuminosity",
        properties: {
          hidden: true,
        },
      },
    };
    me.fileGrid = Ext.create("Ext.dirac.utils.DiracGridPanel", {
      store: me.dataStore,
      oColumns: columns,
      stateful: true,
      stateId: "BookkeepingFileHistory",
      scope: me,
      viewConfig: {
        stripeRows: true,
        enableTextSelection: true,
      },
      dockedItems: [
        {
          xtype: "toolbar",
          dock: "bottom",
          items: [
            {
              xtype: "button",
              text: "Back",
              iconCls: "bk-icon-back",
              handler: function () {
                if (me.current - 1 >= 0) {
                  me.current -= 1;
                  me.fileGrid.getStore().loadData(me.commands[me.current]);
                }
              },
            },
            {
              xtype: "button",
              text: "Next",
              iconCls: "bk-icon-next",
              handler: function () {
                var lfn = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.fileGrid, "FileName");
                me.loadData(lfn);
              },
            },
            {
              xtype: "button",
              text: "Close",
              iconCls: "bk-icon-close",
              handler: function () {
                me.fireEvent("closeFileHistory", me);
              },
            },
          ],
        },
      ],
      region: "center",
      listeners: {
        itemclick: function (table, record, item, index, e, eOpts) {
          me.setLoading("Loading job information");
          Ext.Ajax.request({
            url: GLOBAL.BASE_URL + me.applicationName + "/jobinfo",
            method: "POST",
            params: {
              lfn: record.get("FileName"),
            },
            scope: me,
            success: function (response) {
              me.setLoading(false);
              var jsonData = Ext.JSON.decode(response.responseText);
              if (jsonData["success"] == "true") {
                var data = {};
                // we have to convert to the right data format
                for (var i = 0; i < jsonData["result"].length; i++) {
                  data[jsonData["result"][i][0]] = jsonData["result"][i][1];
                }
                me.stepview.items.getAt(0).getStore().loadData([data]);
                me.stepview.expand();
                me.stepview.show();
              } else {
                GLOBAL.APP.CF.alert(jsonData["error"], "Error");
              }
            },
          });
          return true;
        },
      },
    });

    me.fileGrid.store.on("load", function (fgrid, records, successful, operation, eOpts) {
      var values = [];
      for (var i = 0; i < records.length; i++) {
        values.push(records[i].getData());
      }
      me.current += 1;
      me.commands[me.current] = values;
    });

    var viewStore = Ext.create("Ext.data.Store", {
      fields: me.dataFields,
    });
    var tpl = new Ext.XTemplate(
      '<tpl for=".">',
      '<div style="margin-bottom: 10px;" class="dataset-statistics">',
      "<b>Dirac JobID:</b> {DiracJobID}<br/>",
      "<b>Name:</b> {Name}<br/>",
      "<b>Number of Events:</b> {NumberofEvents}<br/>",
      "<b>Total Luminosity:</b> {TotalLuminosity}<br/>",
      "<b>Statistics Requested:</b> {StatisticsRequested}<br/>",
      "<b>WNMEMORY:</b> {WNMEMORY}<br/>",
      "<b>ExecTime:</b> {ExecTime}<br/>",
      "<b>FirstEventNumber:</b> {FirstEventNumber}<br/>",
      "<b>CPUTime:</b> {CPUTime}<br/>",
      "<b>WNCPUPOWER:</b> {WNCPUPOWER}<br/>",
      "<b>Dirac Version:</b> {DiracVersion}<br/>",
      "<b>EventInputStat:</b> {EventInputStat}<br/>",
      "<b>Location:</b> {Location}<br/>",
      "<b>WORKERNODE:</b> {WORKERNODE}<br/>",
      "<b>WNCPUHS06:</b> {WNCPUHS06}<br/>",
      "<b>WNCACHE:</b> {WNCACHE}<br/>",
      "<b>WNMODEL:</b> {WNMODEL}<br/>",
      "</div>",
      "</tpl>"
    );

    me.stepview = new Ext.panel.Panel({
      region: "east",
      title: "Job attributtes",
      scrollable: true,
      collapsible: true,
      split: true,
      margins: "2 0 2 0",
      cmargins: "2 2 2 2",
      bodyStyle: "padding: 5px",
      width: 400,
      labelAlign: "top",
      minWidth: 200,
      hidden: true,
      listeners: {
        collapse: function (panel, eOpts) {
          panel.hide();
        },
      },
      items: new Ext.view.View({
        tpl: tpl,
        store: viewStore,
        itemSelector: "div.dataset-statistics",
        autoHeight: true,
      }),
      bodyStyle: "padding: 5px",
    });
    me.add([me.stepview, me.fileGrid]);
  },
  loadData: function (lfn) {
    var me = this;
    if (lfn === undefined || lfn == "") {
      Ext.dirac.system_info.msg("Error", "Please select a File Name!");
      return;
    }
    me.fileGrid.store.proxy.extraParams = {
      lfn: lfn,
    };
    me.fileGrid.store.load();
  },
});
