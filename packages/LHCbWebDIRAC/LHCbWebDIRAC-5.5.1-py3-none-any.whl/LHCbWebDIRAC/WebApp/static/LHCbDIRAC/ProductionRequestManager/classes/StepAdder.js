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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.StepList", {
  extend: "Ext.grid.Panel",

  initComponent: function () {
    var me = this;

    me.store = Ext.create("Ext.data.JsonStore", {
      autoLoad: true,
      fields: [
        "StepId",
        "StepName",
        "ProcessingPass",
        "ApplicationName",
        "ApplicationVersion",
        "OptionFiles",
        "OptionsFormat",
        "isMulticore",
        "DDDB",
        "CONDDB",
        "DQTag",
        "ExtraPackages",
        "Visible",
        "Usable",
        "InputFileTypes",
        "OutputFileTypes",
        "textInputFileTypes",
        "textOutputFileTypes",
      ],
      remoteSort: true,
      proxy: {
        type: "ajax",
        url: GLOBAL.BASE_URL + "LHCbStepManager/getSteps",
        extraParams: me.stepfilter,
        params: me.stepfilter,
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

    me.store.sort("StepId", "DESC");
    me.store.load({
      params: {
        start: 0,
        limit: me.pagingBar.pageSize,
        params: me.stepfilter,
        Equal: "Yes",
      },
    });

    Ext.apply(this, {
      columns: [
        {
          header: "ID",
          sortable: true,
          dataIndex: "StepId",
          width: 60,
        },
        {
          header: "Name",
          sortable: true,
          dataIndex: "StepName",
          width: 160,
        },
        {
          header: "Processing pass",
          sortable: true,
          dataIndex: "ProcessingPass",
          width: 120,
        },
        {
          header: "App.",
          sortable: true,
          dataIndex: "ApplicationName",
          width: 60,
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
  Reload: function (equal) {
    var isEqual = Ext.JSON.encode(["Yes"]);
    var me = this;

    if (!equal) isEqual = Ext.JSON.encode(["No"]);
    me.store.proxy.extraParams.Equal = isEqual;
    me.store.load({
      params: {
        start: 0,
        limit: me.pagingBar.pageSize,
      },
    });
  },
});

Ext.define("LHCbDIRAC.ProductionRequestManager.classes.StepDetail", {
  extend: "Ext.panel.Panel",
  tplMarkup: [
    "{StepName}({StepId}/{ProcessingPass}) : {ApplicationName}-{ApplicationVersion}<br/>",
    "System config: {SystemConfig} MC TCK: {mcTCK}<br/>",
    "Options: {OptionFiles} Options format: {OptionsFormat} ",
    "Multicore: {isMulticore}<br/>",
    "DDDB: {DDDB} Condition DB: {CONDDB} DQTag: {DQTag}<br/>",
    "Extra: {ExtraPackages} ",
    "Runtime projects: {textRuntimeProjects}<br/>",
    "Visible: {Visible} Usable:{Usable}<br/>",
    "Input file types: {textInputFileTypes} ",
    "Output file types: {textOutputFileTypes}<br/><br/>",
  ],
  initComponent: function () {
    var me = this;
    me.pData = {};
    me.tpl = new Ext.Template(me.tplMarkup);
    me.callParent(arguments);
  },

  updateDetail: function (data) {
    var me = this;
    me.pData = data;
    me.tpl.overwrite(me.body, data);
  },

  data2edit: function (no) {
    var me = this;
    var v = {};
    for (var i = 0; i < me.pr.RemoteStepFields.length; ++i) v["p" + no + me.pr.LocalStepFields[i]] = me.pData[me.pr.RemoteStepFields[i]];

    v["p" + no + "Html"] = "<b>Step " + no + "</b> " + me.tpl.apply(me.pData);
    return v;
  },
});

Ext.define("LHCbDIRAC.ProductionRequestManager.classes.StepAdder", {
  extend: "Ext.window.Window",

  alias: "widget.stepadder",

  plain: true,
  resizable: false,
  modal: true,
  closeAction: "hide",
  initComponent: function () {
    var me = this;
    var pars = Ext.create("Ext.form.FieldSet", {
      region: "north",
      layout: "column",
      autoHeight: true,
      margins: "5 5 0 5",
      items: [
        {
          xtype: "checkbox",
          name: "nonequal",
          labelStyle: "width:200px",
          style: "margin-top:4px;",
          fieldLabel: "Show also non-coinciding steps",
          listeners: {
            change: function (chb, newValue, oldValue, eOpts) {
              me.onNonEqual(newValue);
            },
          },
        },
      ],
    });
    me.steplist = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.StepList", {
      region: "center",
      split: true,
      margins: "5 0 5 5",
      minWidth: 300,
      stepfilter: me.stepfilter,
    });
    me.steplist.getSelectionModel().on("select", me.onSelect, me);

    me.detail = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.StepDetail", {
      region: "east",
      split: true,
      width: 350,
      minWidth: 200,
      margins: "5 5 5 0",
      pr: me.pr,
      scope: me,
      scrollable: true,
      title: "Step details",
      bodyStyle: "padding-left:15px; padding-top:5px",

      html: "<p>Plese select a Step on the left side</p>",

      buttonAlign: "center",
      buttons: [
        {
          text: this.operation,
          name: "step-add",
          disabled: true,
          scope: me,
        },
        {
          text: "Cancel",
          handler: this.close,
          scope: this,
        },
      ],
    });

    Ext.apply(this, {
      title: this.operation + " Step",
      width: 800,
      height: 350,
      minWidth: 500,
      minHeight: 300,
      maximizable: true,
      resizable: true,
      modal: true,
      layout: "border",
      items: [pars, this.steplist, this.detail],
    });
    me.callParent(arguments);
  },
  onSelect: function (sm, row, rec) {
    var me = this;
    me.down("[name=step-add]").disable();
    me.setLoading(true);
    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + "LHCbStepManager/getStep",
      params: {
        StepId: Ext.JSON.encode(row.get("StepId")),
      },
      success: me.onStepLoaded,
      scope: me,
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
        me.setLoading(false);
      },
    });
  },
  onStepLoaded: function (response) {
    var me = this;
    me.setLoading(false);
    var value = Ext.JSON.decode(response.responseText);
    if (value.success == "false") {
      GLOBAL.APP.CF.alert(value.error, "error");
    } else {
      if (value.result) {
        me.detail.updateDetail(value.result);
        me.down("[name=step-add]").enable();
      } else {
        GLOBAL.APP.CF.alert("Please select simulation descriptions under MC directory!", "error");
      }
    }
  },
  onNonEqual: function (checked) {
    var me = this;
    me.steplist.Reload(!checked);
  },
});
