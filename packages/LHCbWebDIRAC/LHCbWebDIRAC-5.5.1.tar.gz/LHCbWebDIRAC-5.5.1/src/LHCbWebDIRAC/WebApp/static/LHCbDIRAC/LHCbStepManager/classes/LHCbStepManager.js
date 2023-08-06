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
/*
 * ToDo AZ: Hack to add Date type field into selector should do
 * Ext.form.field.Date based DiracDateField, and add support to the
 * DiracBaseSelector
 *
 * It has no <Enter> listener, but I do not really miss it
 */
Ext.define("LHCbDIRAC.DiracDateField", {
  extend: "Ext.form.field.Date",
  getValue: function () {
    var me = this;
    return me.getRawValue();
  },
});

/*
 * Ajax based Combobox with one special features: in adds extraValues to the
 * list it display '' (empty value) correctly
 */
Ext.define("LHCbDIRAC.LHCbStepManager.ComboBox", {
  extend: "Ext.form.field.ComboBox",

  requires: ["Ext.form.field.ComboBox", "Ext.data.Store", "Ext.data.proxy.Memory", "Ext.data.reader.Json", "Ext.XTemplate"],

  /*
   * url - URL to get data from
   */
  url: "",

  /*
   * displayField - expect { success: 'true', result: [ { displayField:
   * value}, ... ] } from the server
   */

  /*
   * valueField - if set in addition to displayField (and is different),
   * expect { success: 'true', result: [ { displayField: value, valueField:
   * value }, ... ] } from the server
   */

  /*
   * extraValues - add this values to the beginning of the list, if there
   * are not there
   */
  extraValues: [],

  initComponent: function () {
    var me = this;

    var fields = [
      {
        name: me.displayField,
      },
    ];
    if (me.valueField && me.valueField != me.displayField)
      fields.push({
        name: me.valueField,
      });

    var ajaxStore = new Ext.data.Store({
      proxy: {
        type: "ajax",
        url: me.url,
        reader: {
          type: "json",
          rootProperty: "result",
          successProperty: "success",
        },
      },
      fields: fields,
      autoLoad: true,
      loading: true,
      listeners: {
        load: {
          fn: me.__onStoreLoad,
          scope: me,
        },
      },
    });

    Ext.apply(me, {
      store: ajaxStore,
      queryMode: "local",
      /* This template makes empty value visible with normal height */
      tpl: Ext.create("Ext.XTemplate", '<tpl for=".">', '<div class="x-boundlist-item">{' + me.displayField + "}&nbsp;</div>", "</tpl>"),
    });
    me.callParent(arguments);
  },

  __insertValue: function (i, value) {
    var me = this;
    var store = me.getStore();
    var extraRow = {};
    extraRow[me.displayField] = value;
    if (me.valueField != me.displayField) extraRow[me.valueField] = value;
    store.insert(i, [extraRow]);
  },

  /*
   * Prepend extraValues to the store
   */
  __onStoreLoad: function (store, records, successful, op) {
    var me = this;

    if (!me.extraValues) return;

    if (!successful) store.removeAll();

    for (var i = 0; i < me.extraValues.length; ++i) {
      var value = me.extraValues[i];
      if ((i > 0 && value == "") || store.find(me.displayField, value) >= 0) continue;
      me.__insertValue(i, value);
    }
  },

  /*
   * Append extraValue, visualize it and reload
   */
  setAndReload: function (value, params) {
    var me = this;
    params = typeof params == "undefined" ? {} : params;
    var store = me.getStore();
    if (me.extraValues && me.extraValues[0] == "") me.extraValues = [""];
    else me.extraValues = [];
    if (value != "") me.extraValues.push(value);
    /*
     * if( store.find( me.displayField, value) < 0 ) me.__insertValue( 0,
     * value );
     */
    store.removeAll(false);
    me.__insertValue(0, value);
    me.setValue(value);
    store.load(params);
  },
});

/**
 * RegisterFileType
 *
 * @extends Ext.Window Dialog to register the new type
 */
Ext.define("LHCbDIRAC.LHCbStepManager.RegisterFileType", {
  extend: "Ext.window.Window",

  requires: ["Ext.form.Panel", "Ext.form.field.Text", "Ext.Ajax"],

  /*
   * addFileTypeURL - how to add new File Type
   */
  addFileTypeURL: "",

  initComponent: function () {
    var me = this;

    me.form = new Ext.form.Panel({
      frame: true,
      items: [
        {
          xtype: "textfield",
          fieldLabel: "Name",
          name: "Name",
          anchor: "100%",
        },
        {
          xtype: "textfield",
          fieldLabel: "Description",
          name: "Description",
          anchor: "100%",
        },
      ],
    });

    Ext.apply(me, {
      title: "Register new File Type",
      modal: true,
      layout: "fit",
      bodyBorder: false,
      border: 0,
      items: me.form,
      dockedItems: [
        {
          xtype: "toolbar",
          dock: "bottom",
          layout: {
            pack: "left",
          },
          items: [
            {
              text: "Register",
              handler: me.__onRegister,
              scope: me,
              iconCls: "dirac-icon-submit",
            },
            {
              text: "Cancel",
              handler: me.close,
              scope: me,
              iconCls: "toolbar-other-close",
            },
          ],
          defaults: {
            margin: 3,
          },
        },
      ],
    });
    me.callParent(arguments);
  },

  initEvents: function () {
    var me = this;

    me.callParent(arguments);
    me.fireEvent("registered");
  },

  __onRegister: function (b, e) {
    var me = this;
    var values = me.form.getValues();
    if (!values["Name"] || !values["Description"]) {
      Ext.MessageBox.show({
        title: "Incomplete",
        msg: "Please fill both fields",
        buttons: Ext.MessageBox.OK,
        icon: Ext.MessageBox.ERROR,
      });
      return;
    }
    Ext.Ajax.request({
      url: me.addFileTypeURL,
      method: "POST",
      params: values,
      scope: me,
      success: function (response) {
        var me = this;
        var jsonData = Ext.JSON.decode(response.responseText);
        if (jsonData["success"] == "true") {
          me.fireEvent("registered", me);
          me.close();
        } else {
          Ext.Msg.alert("Error", jsonData["error"]);
        }
      },
      failure: function (response) {
        var me = this;
        Ext.Msg.alert("Error", me.addFileTypeURL + " : " + response.statusText);
      },
    });
  },
});

/**
 * FileTypeListEditor
 *
 * @extends Ext.form.FieldSet For embeddning list editor
 */
Ext.define("LHCbDIRAC.LHCbStepManager.FileTypeListEditor", {
  extend: "Ext.form.FieldSet",

  requires: ["Ext.form.FieldSet", "Ext.form.field.ComboBox", "Ext.data.ArrayStore", "Ext.grid.Panel", "Ext.menu.Menu"],

  /*
   * fileTypeURL - where to get FileTypes
   */
  fileTypeURL: "",

  /*
   * addFileTypeURL - how to add new File Type
   */
  addFileTypeURL: "",

  initComponent: function () {
    var me = this;

    var store = new Ext.data.ArrayStore({
      fields: [
        {
          name: "FileType",
        },
      ],
      data: [],
    });

    me.grid = new Ext.grid.Panel({
      anchor: "100%",
      height: 150,
      style: "padding-bottom:5px",
      store: store,
      columns: [
        {
          header: "File type",
          dataIndex: "FileType",
          flex: 1,
        },
      ],
      stripeRows: true,
    });
    me.grid.on("itemclick", me.__onRowClick, me);

    me.menu = new Ext.menu.Menu();
    me.menu.add({
      handler: function () {
        var me = this;
        var r = me.grid.getSelectionModel().getLastSelected();
        me.grid.store.remove(r);
      },
      scope: me,
      text: "Remove",
    });

    me.fileTypeStore = new Ext.data.Store({
      proxy: {
        type: "ajax",
        url: me.fileTypeURL,
        reader: {
          type: "json",
          rootProperty: "result",
          successProperty: "success",
        },
      },
      fields: [
        {
          name: "Name",
        },
        {
          name: "Description",
        },
        {
          name: "Label",
          convert: function (value, record) {
            return record.get("Name") + " (" + record.get("Description") + ")";
          },
        },
      ],
      autoLoad: true,
      loading: true,
      listeners: {
        load: function (store, records, successful) {
          if (!successful) store.removeAll();
          store.insert(0, {
            Name: " ",
            Description: "register new file type",
          });
        },
      },
    });

    me.ftCombo = new Ext.form.field.ComboBox({
      store: me.fileTypeStore,
      displayField: "Label",
      valueField: "Name",
      forceSelection: true,
      queryMode: "local",
      triggerAction: "all",
      selectOnFocus: true,
      emptyText: "select file type",
      flex: 1,
      submitValue: false,
    });

    Ext.apply(me, {
      layout: "anchor",
      items: [
        {
          xtype: "fieldcontainer",
          fieldLabel: "File type",
          layout: "hbox",
          labelWidth: 60,
          items: [
            me.ftCombo,
            {
              xtype: "splitter",
            },
            {
              xtype: "button",
              text: "Add",
              handler: me.__onAddFileType,
              scope: me,
            },
          ],
        },
        me.grid,
      ],
    });
    me.callParent(arguments);
  },

  initEvents: function () {
    var me = this;

    me.callParent(arguments);
    me.fireEvent("registered");
  },

  __onAddFileType: function () {
    var me = this;
    var store = me.grid.store;
    var filetype = me.ftCombo.getValue();

    if (!filetype) return;

    if (filetype == " ") {
      var dlg = Ext.create("LHCbDIRAC.LHCbStepManager.RegisterFileType", {
        addFileTypeURL: me.addFileTypeURL,
      });
      dlg.on(
        "registered",
        function () {
          me.fireEvent("registered", me);
        },
        me
      );
      dlg.show();
      return;
    }

    if (store.find("FileType", filetype) >= 0) return;
    store.add({
      FileType: filetype,
    });
  },

  __onRowClick: function (grid, record, item, index, e, eOpts) {
    var me = this;
    me.menu.showAt(e.getXY());
  },

  reloadFileTypes: function () {
    var me = this;

    me.ftCombo.setValue("");
    me.fileTypeStore.reload("");
  },

  setValue: function (filetypes) {
    var me = this;
    var store = me.grid.store;

    me.reloadFileTypes();

    store.removeAll();
    if (filetypes) for (var i = 0; i < filetypes.length; ++i) store.add(filetypes[i]);

    me.fileTypeStore.reload();
  },

  getValue: function (filetypes) {
    var me = this;

    var recs = me.grid.store.getRange();
    var types = [];
    for (var i = 0; i < recs.length; ++i) types[types.length] = recs[i].data;
    return Ext.JSON.encode(types);
  },
});

/*
 * Editor dialog for steps
 */
Ext.define("LHCbDIRAC.LHCbStepManager.Editor", {
  extend: "Ext.form.Panel",

  requires: ["Ext.form.Panel", "Ext.dirac.utils.DiracAjaxProxy", "Ext.dirac.utils.DiracJsonStore"],

  /**
   * stepManager - we need it for Application Name
   */

  initComponent: function () {
    var me = this;

    me.appCombo = Ext.create("LHCbDIRAC.LHCbStepManager.ComboBox", {
      flex: 1,
      name: "ApplicationName",
      forceSelection: true,
      emptyText: "Select application name",
      extraValues: [""],
      selectOnFocus: true,
      url: GLOBAL.BASE_URL + me.stepManager.applicationName + "/getApplications",
      displayField: "v",
      listeners: {
        select: {
          fn: me.__onAppSelect,
          scope: me,
        },
      },
    });

    me.verCombo = Ext.create("LHCbDIRAC.LHCbStepManager.ComboBox", {
      flex: 1,
      name: "ApplicationVersion",
      forceSelection: true,
      emptyText: "and version",
      extraValues: [""],
      selectOnFocus: true,
      url: GLOBAL.BASE_URL + me.stepManager.applicationName + "/getAppVersions",
      displayField: "v",
    });

    me.opfCombo = Ext.create("LHCbDIRAC.LHCbStepManager.ComboBox", {
      name: "OptionsFormat",
      fieldLabel: "Options format",
      forceSelection: true,
      extraValues: [""],
      selectOnFocus: true,
      anchor: "50%",
      url: GLOBAL.BASE_URL + me.stepManager.applicationName + "/getAppOptionsFormats",
      displayField: "v",
    });

    me.rtpCombo = Ext.create("LHCbDIRAC.LHCbStepManager.ComboBox", {
      name: "RuntimeProjectStepId",
      fieldLabel: "Runtime project",
      forceSelection: true,
      emptyText: "Select Runtime Project if desired",
      extraValues: [""],
      selectOnFocus: true,
      url: GLOBAL.BASE_URL + me.stepManager.applicationName + "/getRuntimeProjects",
      displayField: "text",
      valueField: "id",
      anchor: "50%",
    });

    me.cdbCombo = Ext.create("LHCbDIRAC.LHCbStepManager.ComboBox", {
      name: "CONDDB",
      fieldLabel: "CondDB",
      forceSelection: false,
      extraValues: [""],
      selectOnFocus: true,
      anchor: "50%",
      url: GLOBAL.BASE_URL + me.stepManager.applicationName + "/getBKTags?tag=CONDDB",
      displayField: "v",
    });

    me.ddbCombo = Ext.create("LHCbDIRAC.LHCbStepManager.ComboBox", {
      name: "DDDB",
      fieldLabel: "DDDB",
      forceSelection: false,
      extraValues: [""],
      selectOnFocus: true,
      anchor: "50%",
      url: GLOBAL.BASE_URL + me.stepManager.applicationName + "/getBKTags?tag=DDDB",
      displayField: "v",
    });

    me.dqtCombo = Ext.create("LHCbDIRAC.LHCbStepManager.ComboBox", {
      name: "DQTag",
      fieldLabel: "DQTag",
      forceSelection: false,
      extraValues: [""],
      selectOnFocus: true,
      anchor: "50%",
      url: GLOBAL.BASE_URL + me.stepManager.applicationName + "/getBKTags?tag=DQTag",
      displayField: "v",
    });

    me.ift = Ext.create("LHCbDIRAC.LHCbStepManager.FileTypeListEditor", {
      title: "Input",
      flex: 1,
      fileTypeURL: GLOBAL.BASE_URL + me.stepManager.applicationName + "/getFileTypes",
      addFileTypeURL: GLOBAL.BASE_URL + me.stepManager.applicationName + "/addFileType",
    });
    me.ift.on("registered", me.__reloadFileTypes, me);
    me.oft = Ext.create("LHCbDIRAC.LHCbStepManager.FileTypeListEditor", {
      title: "Output",
      flex: 1,
      fileTypeURL: GLOBAL.BASE_URL + me.stepManager.applicationName + "/getFileTypes",
      addFileTypeURL: GLOBAL.BASE_URL + me.stepManager.applicationName + "/addFileType",
    });
    me.oft.on("registered", me.__reloadFileTypes, me);

    Ext.apply(me, {
      bodyPadding: 5,
      title: "New step",
      items: [
        {
          xtype: "textfield",
          fieldLabel: "Name",
          name: "StepName",
          anchor: "98%",
        },
        {
          xtype: "textfield",
          fieldLabel: "Processing pass",
          name: "ProcessingPass",
          anchor: "50%",
        },
        {
          xtype: "fieldcontainer",
          fieldLabel: "Application",
          anchor: "50%",
          layout: "hbox",
          items: [
            me.appCombo,
            {
              xtype: "splitter",
            },
            me.verCombo,
          ],
        },
        {
          xtype: "textfield",
          fieldLabel: "System config",
          name: "SystemConfig",
          anchor: "98%",
        },
        {
          xtype: "textfield",
          fieldLabel: "MC TCK",
          name: "mcTCK",
          anchor: "98%",
        },
        {
          xtype: "textfield",
          fieldLabel: "Option files",
          name: "OptionFiles",
          anchor: "98%",
        },
        me.opfCombo,
        {
          xtype: "combo",
          fieldLabel: "Multicore",
          name: "isMulticore",
          store: [
            ["Y", "Yes"],
            ["N", "No"],
          ],
          forceSelection: true,
          mode: "local",
          triggerAction: "all",
          selectOnFocus: true,
        },
        {
          xtype: "textfield",
          fieldLabel: "Extra packages",
          name: "ExtraPackages",
          anchor: "98%",
        },
        me.rtpCombo,
        me.cdbCombo,
        me.ddbCombo,
        me.dqtCombo,
        {
          xtype: "combo",
          fieldLabel: "Visible",
          name: "Visible",
          store: [
            ["Y", "Yes"],
            ["N", "No"],
          ],
          forceSelection: true,
          mode: "local",
          triggerAction: "all",
          selectOnFocus: true,
        },
        {
          xtype: "combo",
          fieldLabel: "Usable",
          name: "Usable",
          store: ["Yes", "Not ready", "Obsolete"],
          forceSelection: true,
          mode: "local",
          triggerAction: "all",
          selectOnFocus: true,
        },
        {
          xtype: "fieldcontainer",
          fieldLabel: "File types",
          anchor: "98%",
          layout: "hbox",
          items: [
            me.ift,
            {
              xtype: "splitter",
            },
            me.oft,
          ],
        },
        {
          xtype: "hidden",
          name: "InputFileTypes",
        },
        {
          xtype: "hidden",
          name: "OutputFileTypes",
        },
        {
          xtype: "hidden",
          name: "StepId",
        },
      ],

      dockedItems: [
        {
          xtype: "toolbar",
          dock: "bottom",
          layout: {
            pack: "left",
          },
          items: [
            {
              text: "Save",
              handler: me.__onSave,
              scope: me,
              iconCls: "dirac-icon-submit",
            },
            {
              text: "Cancel",
              handler: me.__onCancel,
              scope: me,
              iconCls: "toolbar-other-close",
            },
          ],
          defaults: {
            margin: 3,
          },
        },
      ],
    });
    me.callParent(arguments);
  },

  initEvents: function () {
    var me = this;

    me.callParent(arguments);
    me.fireEvent("saved");
    me.fireEvent("cancelled");
  },

  setData: function (data) {
    var me = this;

    if (!data) {
      me.setData({
        StepId: 0,
        StepName: "",
        ProcessingPass: "",
        ApplicationName: "",
        ApplicationVersion: "",
        SystemConfig: "",
        mcTCK: "",
        OptionFiles: "",
        OptionsFormat: "",
        isMulticore: "N",
        ExtraPackages: "",
        RuntimeProjects: [],
        CONDDB: "",
        DDDB: "",
        DQTag: "",
        Visible: "Y",
        Usable: "Yes",
        InputFileTypes: [],
        OutputFileTypes: [],
      });
      return;
    }
    if (data["StepId"]) me.setTitle("Edit step " + data["StepId"]);
    else me.setTitle("New step definition");

    if (data["RuntimeProjects"] && data["RuntimeProjects"].length) data["RuntimeProjectStepId"] = data["RuntimeProjects"][0]["StepId"];
    else data["RuntimeProjectStepId"] = "";

    var app = data["ApplicationName"];
    me.appCombo.setAndReload(app);
    me.verCombo.setAndReload(data["ApplicationVersion"], {
      params: {
        app: app.toUpperCase(),
      },
    });
    me.opfCombo.setAndReload(data["OptionsFormat"], {
      params: {
        app: app,
      },
    });
    me.rtpCombo.setAndReload(data["RuntimeProjects"]);
    me.cdbCombo.setAndReload(data["CONDDB"]);
    me.ddbCombo.setAndReload(data["DDDB"]);
    me.dqtCombo.setAndReload(data["DQTag"]);

    me.getForm().setValues(data);
    me.ift.setValue(data["InputFileTypes"]);
    me.oft.setValue(data["OutputFileTypes"]);
  },

  __onAppSelect: function () {
    var me = this;
    var app = me.appCombo.getValue();
    me.verCombo.setAndReload("", {
      params: {
        app: app.toUpperCase(),
      },
    });
    me.opfCombo.setAndReload("", {
      params: {
        app: app,
      },
    });
  },

  __reloadFileTypes: function () {
    var me = this;

    me.ift.reloadFileTypes();
    me.oft.reloadFileTypes();
  },

  __onCancel: function () {
    var me = this;

    me.fireEvent("cancelled", me);
  },

  __onSave: function () {
    var me = this;
    var form = me.getForm();

    form.findField("InputFileTypes").setValue(me.ift.getValue());
    form.findField("OutputFileTypes").setValue(me.oft.getValue());

    if (
      form.findField("OutputFileTypes").getValue() == "[]" ||
      !form.findField("StepName").getValue() ||
      !form.findField("ProcessingPass").getValue()
    ) {
      Ext.Msg.alert("Error", "Name, processing pass and output file types should be specified");
      return;
    }

    form.submit({
      failure: function (form, action) {
        var me = this;
        Ext.Msg.alert("Error", action.url + " : " + action.response.statusText);
      },
      success: function (form, action) {
        var me = this;
        if (action.result["success"] == "true") {
          me.fireEvent("saved", me);
        } else {
          Ext.Msg.alert("Error", action.result["error"]);
        }
      },
      scope: this,
      url: GLOBAL.BASE_URL + me.stepManager.applicationName + "/saveStep",
      submitEmptyText: false,
      waitMsg: "Saving step",
    });
  },
});

Ext.define("LHCbDIRAC.LHCbStepManager.classes.LHCbStepManager", {
  extend: "Ext.dirac.core.Module",

  requires: [
    "Ext.panel.Panel",
    "Ext.form.field.Date",
    "Ext.grid.plugin.RowExpander",
    "Ext.dirac.utils.DiracBaseSelector",
    "Ext.dirac.utils.DiracAjaxProxy",
    "Ext.dirac.utils.DiracJsonStore",
    "Ext.dirac.utils.DiracGridPanel",
    "Ext.dirac.utils.DiracPagingToolbar",
    "Ext.dirac.utils.DiracApplicationContextMenu",
    "Ext.dirac.utils.GridPanel",
  ],

  viewPanelExpanded: false,
  loadState: function (data) {
    var me = this;
    me.grid.loadState(data);
    me.leftPanel.loadState(data);
    if (data.leftPanelCollapsed) {
      me.left.panel.collapse();
    }
  },

  getStateData: function () {
    var me = this;
    var oReturn = {
      leftMenu: me.leftPanel.getStateData(),
      grid: me.grid.getStateData(),
      leftPanelCollapsed: me.leftPanel.collapsed,
    };
    return oReturn;
  },

  initComponent: function () {
    var me = this;
    var oDimensions = GLOBAL.APP.MAIN_VIEW.getViewMainDimensions();

    me.launcher.title = "LHCb Step Manager";
    me.launcher.maximized = false;
    me.launcher.width = oDimensions[0];
    me.launcher.height = oDimensions[1] - GLOBAL.APP.MAIN_VIEW.taskbar ? GLOBAL.APP.MAIN_VIEW.taskbar.getHeight() : 0;
    me.launcher.x = 0;
    me.launcher.y = 0;

    Ext.apply(me, {
      layout: "card",
      bodyBorder: false,
    });

    me.callParent(arguments);
  },

  dataFields: [
    {
      name: "StepIdCheckBox",
      mapping: "StepId",
    },
    {
      name: "StepId",
      type: "int",
    },
    {
      name: "StepName",
    },
    {
      name: "ProcessingPass",
    },
    {
      name: "ApplicationName",
    },
    {
      name: "ApplicationVersion",
    },
    {
      name: "Visible",
    },
    {
      name: "Usable",
    },
    {
      name: "SystemConfig",
    },
    {
      name: "mcTCK",
    },
    {
      name: "OptionFiles",
    },
    {
      name: "OptionsFormat",
    },
    {
      name: "isMulticore",
    },
    {
      name: "DDDB",
    },
    {
      name: "CONDDB",
    },
    {
      name: "DQTag",
    },
    {
      name: "ExtraPackages",
    },
    {
      name: "RuntimeProjects",
    },
    {
      name: "textRuntimeProjects",
    },
    {
      name: "InputFileTypes",
    },
    {
      name: "OutputFileTypes",
    },
    {
      name: "textInputFileTypes",
    },
    {
      name: "textOutputFileTypes",
    },
  ],

  renderVisible: function (val) {
    if (val == "Y") return "Yes";
    return "No";
  },

  buildUI: function () {
    var me = this;

    /*
     * Left panel
     */
    var selectors = {
      ApplicationName: "Application",
      ApplicationVersion: "Application Version",
      Visible: "Visible",
      Usable: "Usable",
    };

    var textFields = {
      ProcessingPass: {
        name: "Processing pass",
        type: "originalText" /* Bug Workaround */,
        properties: {
          canDisable: false,
        },
      },
      StepId: {
        name: "StepId",
        type: "originalText" /* Bug Workaround */,
        properties: {
          canDisable: false,
        },
      },
      /*
       * 'StartDate' : { name : "Registered after (YYYY.mm.dd)", type :
       * "originalText", properties : { canDisable : false } }
       */
    };

    var properties = [[]];
    var map = [
      ["ApplicationName", "ApplicationName"],
      ["ApplicationVersion", "ApplicationVersion"],
      ["Visible", "Visible"],
      ["Usable", "Usable"],
      ["ProcessingPass", "ProcessingPass"],
      ["StepId", "StepId"],
      ["StartDate", "StartDate"],
    ];

    me.leftPanel = Ext.create("Ext.dirac.utils.DiracBaseSelector", {
      scope: me,
      cmbSelectors: selectors,
      textFields: textFields,
      hasTimeSearchPanel: false,
      datamap: map,
      url: "LHCbStepManager/getSelectionData",
      properties: properties,
    });

    me.leftPanel.cmbSelectors["ApplicationVersion"].on("expand", function (field, eOpts) {
      me.leftPanel.setLoading("Loading Application vesrion ... ");
      Ext.Ajax.request({
        url: GLOBAL.BASE_URL + "LHCbStepManager/getAppVersions",
        params: {
          app: me.leftPanel.cmbSelectors["ApplicationName"].getValue()[0].toUpperCase(),
        },
        scope: me,
        success: function (response) {
          var me = this;
          me.leftPanel.setLoading(false);
          var response = Ext.JSON.decode(response.responseText);

          if (response.success == "false") {
            Ext.dirac.system_info.msg("Error", response.error);
            return;
          }
          var dataOptions = [];
          for (var i = 0; i < response.result.length; i++) dataOptions.push([response.result[i].v, response.result[i].v]);

          var oNewStore = new Ext.data.ArrayStore({
            fields: ["value", "text"],
            data: dataOptions,
          });

          me.leftPanel.cmbSelectors["ApplicationVersion"].refreshStore(oNewStore);
        },
        failure: function (response) {
          GLOBAL.APP.CF.showAjaxErrorMessage(response);
          me.leftPanel.setLoading(false);
        },
      });
    });

    var startDate = Ext.create("LHCbDIRAC.DiracDateField", {
      labelAlign: "top",
      anchor: "100%",
      format: "Y.m.d",
      enableKeyEvents: true,

      fieldLabel: "Registered after (YYYY.mm.dd)",
      scope: me,
      canDisable: false,
      type: "originalText" /* Bug Workaround */,
    });
    me.leftPanel.textFields["StartDate"] = startDate;
    me.leftPanel.add(startDate);

    /*
     * Grid
     */
    var oProxy = Ext.create("Ext.dirac.utils.DiracAjaxProxy", {
      url: GLOBAL.BASE_URL + me.applicationName + "/getSteps",
    });

    me.dataStore = Ext.create("Ext.dirac.utils.DiracJsonStore", {
      autoLoad: false,
      proxy: oProxy,
      fields: me.dataFields,
      scope: me,
      sorters: [
        {
          property: "StepId",
          direction: "DESC",
        },
      ],
    });

    var oColumns = {
      checkBox: {
        dataIndex: "StepIdCheckBox",
      },
      Id: {
        dataIndex: "StepId",
        properties: {
          width: 80,
        },
      },
      Name: {
        dataIndex: "StepName",
        properties: {
          width: 200,
        },
      },
      "Processing pass": {
        dataIndex: "ProcessingPass",
        properties: {
          width: 150,
        },
      },
      Application: {
        dataIndex: "ApplicationName",
      },
      Version: {
        dataIndex: "ApplicationVersion",
      },
      Visible: {
        dataIndex: "Visible",
        renderer: me.renderVisible,
      },
      Usable: {
        dataIndex: "Usable",
      },
    };

    var toolButtons = {
      Protected: [
        {
          text: "New",
          handler: me.__newStep,
          properties: {
            tooltip: "Create new Step definition",
          },
          property: "StepAdministrator",
        },
      ],
    };

    var pagingToolbar = Ext.create("Ext.dirac.utils.DiracPagingToolbar", {
      toolButtons: toolButtons,
      property: "StepAdministrator",
      store: me.dataStore,
      scope: me,
    });

    var menuitems = {
      Visible: [
        {
          text: "Window view",
          handler: me.__windowViewStep,
          properties: {
            tooltip: "Click to show the details for the selected Step",
          },
        },
        {
          text: "View",
          handler: me.__viewStep,
          properties: {
            tooltip: "Click to show the details for the selected Step",
            iconCls: "dirac-icon-text",
          },
        },
        {
          text: "Requests",
          handler: me.__requests,
          properties: {
            tooltip: "Shows the productions requests, which are using this step",
          },
        },
      ],
    };
    // AZ: Todo. It does not work in one go, DiracApplicationContextMenu bug
    if (me.__isStepAdministrator())
      menuitems["Protected"] = [
        {
          text: "Edit",
          handler: me.__editStep,
          properties: {
            tooltip: "Click to edit selected Step",
          },
          property: "StepAdministrator",
        },
        {
          text: "-",
        },
        {
          text: "Duplicate",
          handler: me.__duplicateStep,
          properties: {
            tooltip: "Duplicate selected step",
          },
          property: "StepAdministrator",
        },
        {
          text: "Delete",
          handler: me.__deleteStep,
          properties: {
            tooltip: "Delete selected step",
          },
          property: "StepAdministrator",
        },
      ];

    me.contextGridMenu = new Ext.dirac.utils.DiracApplicationContextMenu({
      menu: menuitems,
      scope: me,
    });

    var expanderTplBody = [
      "<b>System config:</b> {SystemConfig}<br/>",
      "<b>MC TCK:</b> {mcTCK}<br/>",
      "<b>Options:</b> {OptionFiles}<br/>",
      "<b>Options format:</b> {OptionsFormat}<br/>",
      "<b>DDDB:</b> {DDDB} <b>Condition DB:</b> {CONDDB}<br/> <b>DQTag:</b> {DQTag}<br/>",
      "<b>Extra:</b> {ExtraPackages} <b>Multicore:</b> {isMulticore}<br/>",
      "<b>Runtime projects:</b> {textRuntimeProjects}<br/>",
    ];

    me.grid = Ext.create("Ext.dirac.utils.DiracGridPanel", {
      store: me.dataStore,
      oColumns: oColumns,
      contextMenu: me.contextGridMenu,
      pagingToolbar: pagingToolbar,
      scope: me,
      region: "center",
      plugins: [
        {
          ptype: "rowexpander",
          rowBodyTpl: expanderTplBody,
        },
      ],
    });

    me.grid.on("itemclick", function (gw, record, item, index, e, eOpts) {
      if (me.viewPanelExpanded) me.__viewStep();
    });

    me.leftPanel.setGrid(me.grid);

    var viewStore = Ext.create("Ext.data.Store", {
      fields: me.dataFields,
    });
    var tpl = new Ext.XTemplate(
      '<tpl for=".">',
      '<div style="margin-bottom: 10px;" class="dataset-statistics">',
      "<b>ID:</b> {StepId}<br/>",
      "<b>Name:</b> {StepName}<br/>",
      "<b>Processing pass:</b> {ProcessingPass}<br/>",
      "<b>Application:</b> {ApplicationName} {ApplicationVersion}<br/>",
      "<b>System config:</b> {SystemConfig}<br/>",
      "<b>MC TCK:</b> {mcTCK}<br/>",
      "<b>Options:</b> {OptionFiles}<br/>",
      "<b>Options format:</b> {OptionsFormat}<br/>",
      "<b>Multicore:</b> {isMulticore}<br/>",
      "<b>DDDB:</b> {DDDB}<br/>",
      "<b>Condition DB:</b> {CONDDB}<br/>",
      "<b>DQTag:</b> {DQTag}<br/>",
      "<b>Extra:</b> {ExtraPackages}<br/>",
      "<b>Runtime projects:</b> {textRuntimeProjects}<br/>",
      "<b>Visible:</b> {Visible}<br/>",
      "<b>Usable:</b> {Usable}<br/>",
      "<b>Input file types:</b> {textInputFileTypes}<br/>",
      "<b>Output file types:</b> {textOutputFileTypes}<br/>",
      "</div>",
      "</tpl>"
    );

    me.stepview = new Ext.panel.Panel({
      region: "east",
      scrollable: true,
      collapsible: true,
      split: true,
      margins: "2 0 2 0",
      cmargins: "2 2 2 2",
      bodyStyle: "padding: 5px",
      width: 600,
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

    me.browserPanel = new Ext.create("Ext.panel.Panel", {
      layout: "border",
      defaults: {
        collapsible: true,
        split: true,
      },
      items: [me.leftPanel, me.grid, me.stepview],
    });

    me.editPanel = new Ext.create("LHCbDIRAC.LHCbStepManager.Editor", {
      stepManager: me,
    });
    me.editPanel.on("saved", me.__onEditorSave, me);
    me.editPanel.on("cancelled", me.__onEditorCancel, me);

    me.add([me.browserPanel, me.editPanel]);
  },

  __isStepAdministrator: function () {
    return "properties" in GLOBAL.USER_CREDENTIALS && Ext.Array.indexOf(GLOBAL.USER_CREDENTIALS.properties, "StepAdministrator") != -1;
  },

  __viewStep: function () {
    var me = this;
    me.viewPanelExpanded = true;
    var oId = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "StepId");
    me.getContainer().setLoading(true);
    Ext.Ajax.request({
      url: GLOBAL.BASE_URL + me.applicationName + "/getStep",
      method: "POST",
      params: {
        StepId: oId,
      },
      scope: me,
      success: function (response) {
        me.getContainer().setLoading(false);
        var jsonData = Ext.JSON.decode(response.responseText);
        if (jsonData["success"] == "true") {
          me.stepview.items.getAt(0).getStore().loadData([jsonData["result"]]);
          //me.getLayout().setActiveItem(2);
          me.stepview.expand();
          me.stepview.show();
        } else {
          GLOBAL.APP.CF.alert(jsonData["error"], "Error");
        }
      },
    });
  },
  __windowViewStep: function () {
    var me = this;
    var oId = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "StepId");
    me.getContainer().setLoading(true);
    Ext.Ajax.request({
      url: GLOBAL.BASE_URL + me.applicationName + "/getStep",
      method: "POST",
      params: {
        StepId: oId,
      },
      scope: me,
      success: function (response) {
        me.getContainer().setLoading(false);
        me.getContainer().body.unmask();
        var jsonData = Ext.JSON.decode(response.responseText);
        if (jsonData["success"] == "true") {
          var tplMarkup = [
            "<b>ID:</b> {StepId}<br/>",
            "<b>Name:</b> {StepName}<br/>",
            "<b>Processing pass:</b> {ProcessingPass}<br/>",
            "<b>Application:</b> {ApplicationName} {ApplicationVersion}<br/>",
            "<b>System config:</b> {SystemConfig}<br/>",
            "<b>MC TCK:</b> {mcTCK}<br/>",
            "<b>Options:</b> {OptionFiles}<br/>",
            "<b>Options format:</b> {OptionsFormat}<br/>",
            "<b>Multicore:</b> {isMulticore}<br/>",
            "<b>DDDB:</b> {DDDB}<br/>",
            "<b>Condition DB:</b> {CONDDB}<br/>",
            "<b>DQTag:</b> {DQTag}<br/>",
            "<b>Extra:</b> {ExtraPackages}<br/>",
            "<b>Runtime projects:</b> {textRuntimeProjects}<br/>",
            "<b>Visible:</b> {Visible}<br/>",
            "<b>Usable:</b> {Usable}<br/>",
            "<b>Input file types:</b> {textInputFileTypes}<br/>",
            "<b>Output file types:</b> {textOutputFileTypes}<br/>",
          ];
          me.getContainer().oprPrepareAndShowWindowTpl(tplMarkup, jsonData["result"], "Step " + oId);
        } else {
          GLOBAL.APP.CF.alert(jsonData["error"], "Error");
        }
      },
    });
  },
  __editOrDuplicateStep: function (duplicate) {
    var me = this;

    duplicate = typeof duplicate == "undefined" ? false : duplicate;

    var oId = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "StepId");
    Ext.Ajax.request({
      url: GLOBAL.BASE_URL + me.applicationName + "/getStep",
      method: "POST",
      params: {
        StepId: oId,
      },
      scope: me,
      success: function (response) {
        me.getContainer().body.unmask();
        var jsonData = Ext.JSON.decode(response.responseText);
        if (jsonData["success"] == "true") {
          if (duplicate) jsonData["result"]["StepId"] = 0;
          me.editPanel.setData(jsonData["result"]);
          me.getLayout().setActiveItem(1);
        } else {
          GLOBAL.APP.CF.alert(jsonData["error"], "Error");
        }
      },
    });
  },

  __editStep: function () {
    var me = this;

    me.__editOrDuplicateStep(false);
  },

  __duplicateStep: function () {
    var me = this;

    me.__editOrDuplicateStep(true);
  },

  __newStep: function () {
    var me = this;

    me.editPanel.setData();
    me.getLayout().setActiveItem(1);
  },

  __onEditorCancel: function () {
    var me = this;

    me.getLayout().setActiveItem(0);
  },

  __onEditorSave: function () {
    var me = this;

    me.getLayout().setActiveItem(0);
    me.grid.getStore().reload();
  },

  __doDeleteStep: function (oId) {
    var me = this;

    Ext.Ajax.request({
      url: GLOBAL.BASE_URL + me.applicationName + "/deleteStep",
      method: "POST",
      params: {
        StepId: oId,
      },
      scope: me,
      success: function (response) {
        var me = this;
        var jsonData = Ext.JSON.decode(response.responseText);
        if (jsonData["success"] == "true") me.grid.getStore().reload();
        else Ext.Msg.alert("Error", jsonData["error"]);
      },
    });
  },

  __deleteStep: function () {
    var me = this;

    var oId = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "StepId");
    Ext.MessageBox.confirm(
      "Message",
      "Do you really want to delete Step " + oId + "?",
      function (btn) {
        if (btn == "yes") me.__doDeleteStep(oId);
      },
      me
    );
  },
  __requests: function () {
    var me = this;
    var oId = GLOBAL.APP.CF.getFieldValueFromSelectedRow(me.grid, "StepId");

    var oFields = ["RequestId", "RequestName", "RequestWG", "RequestAuthor"];

    var oColumns = [
      {
        text: "RequestId",
        flex: 1,
        sortable: true,
        dataIndex: "RequestId",
      },
      {
        text: "RequestName",
        flex: 1,
        sortable: true,
        dataIndex: "RequestName",
      },
      {
        text: "RequestWG",
        flex: 1,
        sortable: true,
        dataIndex: "RequestWG",
      },
      {
        text: "RequestAuthor",
        flex: 1,
        sortable: true,
        dataIndex: "RequestAuthor",
      },
    ];

    var oGrid = Ext.create("Ext.dirac.utils.GridPanel", {
      oFields: oFields,
      oColumns: oColumns,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/getRequest",
      params: {
        StepId: oId,
      },
      menu: null,
      parent: me,
      selType: "cellmodel",
    });
    me.getContainer().showInWindow("The following requests are using step:" + oId, oGrid);
  },
});
