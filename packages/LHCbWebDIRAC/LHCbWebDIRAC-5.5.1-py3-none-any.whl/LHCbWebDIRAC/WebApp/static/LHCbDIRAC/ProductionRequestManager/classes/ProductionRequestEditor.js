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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.ProductionRequestEditor", {
  extend: "Ext.form.Panel",

  requires: [
    "Ext.form.Panel",
    "Ext.dirac.utils.DiracAjaxProxy",
    "Ext.dirac.utils.DiracJsonStore",
    "LHCbDIRAC.ProductionRequestManager.classes.ComboBox",
    "LHCbDIRAC.ProductionRequestManager.classes.BkSimCondBrowser",
    "LHCbDIRAC.ProductionRequestManager.classes.BookkeepingInputDataBrowser",
    "LHCbDIRAC.ProductionRequestManager.classes.StepsView",
    "LHCbDIRAC.ProductionRequestManager.classes.StepAdder",
    "LHCbDIRAC.ProductionRequestManager.classes.PrWorkflow",
  ],

  /**
   * stepManager - we need it for Application Name
   */
  LocalStepFields: [
    "Step",
    "Name",
    "Pass",
    "App",
    "Ver",
    "SConf",
    "mcTCK",
    "Opt",
    "OptF",
    "IsM",
    "DDDb",
    "CDb",
    "DQT",
    "EP",
    "TRP",
    "Vis",
    "Use",
    "IFT",
    "OFT",
    "Html",
  ],
  RemoteStepFields: [
    "StepId",
    "StepName",
    "ProcessingPass",
    "ApplicationName",
    "ApplicationVersion",
    "SystemConfig",
    "mcTCK",
    "OptionFiles",
    "OptionsFormat",
    "isMulticore",
    "DDDB",
    "CONDDB",
    "DQTag",
    "ExtraPackages",
    "textRuntimeProjects",
    "Visible",
    "Usable",
    "textInputFileTypes",
    "textOutputFileTypes",
  ],

  initComponent: function () {
    var me = this;

    me.simCondBtn = Ext.create(Ext.button.Button, {
      text: "Select from BK",
      handler: me.onSelectFromBk,
      scope: me,
    });

    me.simCond = Ext.create(Ext.form.FieldSet, {
      title: 'Simulation Conditions  <font color="red">(not registered yet)</font>',
      autoHeight: true,
      width: 622,
      defaultType: "textfield",
      items: [
        {
          xtype: "panel",
          layout: "column",
          autoHeight: true,
          anchor: "98%",
          items: [
            {
              width: 500,
              autoHeight: true,
              xtype: "textfield",
              fieldLabel: "Description",
              name: "simDesc",
              anchor: "100%",
            },
            me.simCondBtn,
            {
              xtype: "hiddenfield",
              name: "simCondID",
            },
          ],
        },
        {
          xtype: "panel",
          layout: "column",
          anchor: "98%",
          autoHeight: true,
          defaultType: "textfield",
          defaults: {
            width: 250,
            frame: false,
          },
          items: [
            {
              fieldLabel: "Beam",
              name: "BeamCond",
              width: 300,
            },
            {
              fieldLabel: "Beam energy",
              name: "BeamEnergy",
            },
            {
              fieldLabel: "Generator",
              name: "Generator",
              width: 300,
            },
            {
              fieldLabel: "G4 settings",
              name: "G4settings",
            },
            {
              fieldLabel: "Magnetic field",
              name: "MagneticField",
              width: 300,
            },
            {
              fieldLabel: "Detector",
              name: "DetectorCond",
            },
            {
              fieldLabel: "Luminosity",
              name: "Luminosity",
              width: 300,
            },
            {
              xtype: "hidden",
              name: "condType",
              width: 300,
            },
          ],
        },
      ],
    });

    me.inDataBtn = Ext.create("Ext.button.Button", {
      xtype: "button",
      text: "Select from BK",
      handler: me.onSelectInputFromBk,
      scope: me,
    });

    var id_items = [
      {
        xtype: "panel",
        layout: "column",
        defaults: {
          xtype: "displayfield",
        },
        items: [
          {
            xtype: "textfield",
            width: 500,
            fieldLabel: "Conditions",
            name: "simDesc",
          },
          me.inDataBtn,
          {
            xtype: "hidden",
            name: "simCondID",
          },
          /*
           * , { xtype : 'hidden', name : 'condType' }, { xtype :
           * 'hidden', name : 'BeamCond' }, { xtype : 'hidden', name :
           * 'MagneticField' }, { xtype : 'hidden', name : 'Generator' }, {
           * xtype : 'hidden', name : 'G4settings' }, { xtype :
           * 'hidden', name : 'Luminosity' }, { xtype : 'hidden', name :
           * 'DetectorCond' }, { xtype : 'hidden', name : 'BeamEnergy' },
           */ {
            xtype: "panel",
            layout: "column",
            autoHeight: true,
            defaultType: "textfield",
            defaults: {
              width: 250,
              scrollable: true,
              submitEmptyText: false,
            },
            items: [
              {
                fieldLabel: "Config",
                name: "configName",
                width: 300,
                setReadOnly: true,
                fieldStyle: "background-color: #FFFFCC; background-image: none;",
              },
              {
                fieldLabel: "version",
                name: "configVersion",
                setReadOnly: true,
                fieldStyle: "background-color: #FFFFCC; background-image: none;",
              },
              {
                fieldLabel: "Processing Pass",
                name: "inProPass",
                width: 300,
                scrollable: true,
                readOnly: true,
                fieldStyle: "background-color: #FFFFCC; background-image: none;",
              },
              {
                fieldLabel: "File type",
                name: "inFileType",
                setReadOnly: true,
                fieldStyle: "background-color: #FFFFCC; background-image: none;",
              },
              {
                xtype: "dirac.combobox",
                fieldLabel: "DQ flag",
                multiSelect: true,
                name: "inDataQualityFlag",
                extraValues: [""],
                valueField: "v",
                displayField: "v",
                forceSelection: false,
                selectOnFocus: true,
                width: 300,
                url: GLOBAL.BASE_URL + "ProductionRequestManager/bkk_dq_list",
              },
              {
                xtype: "dirac.combobox",
                fieldLabel: "Production",
                name: "inProductionID",
                displayField: "text",
                multiSelect: true,
                extraValues: [""],
                valueField: "id",
                forceSelection: false,
                selectOnFocus: true,
                url: GLOBAL.BASE_URL + "ProductionRequestManager/bkk_input_prod",
              },
              {
                xtype: "dirac.combobox",
                name: "inTCKs",
                width: 300,
                fieldLabel: "TCKs",
                multiSelect: true,
                forceSelection: false,
                displayField: "text",
                valueField: "id",
                extraValues: [""],
                selectOnFocus: true,
                anchor: "50%",
                url: GLOBAL.BASE_URL + "ProductionRequestManager/bkk_input_tcks",
              },
            ],
          },
        ],
      },
    ];

    me.inData = Ext.create("Ext.form.FieldSet", {
      title: "Input data",
      autoHeight: true,
      width: 622,
      layout: "form",
      defaultType: "textfield",
      items: id_items,
    });

    me.addStepBtn = Ext.create("Ext.button.Button", {
      text: "Add step",
      handler: me.onAddStepBtn,
      name: "addStepButton",
      scope: me,
    });

    me.delStepBtn = Ext.create("Ext.button.Button", {
      text: "Delete last step",
      handler: me.onDelStepBtn,
      name: "deleteStepButton",
      scope: me,
      hidden: true,
    });

    me.stepPanel = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.StepsView", {
      change_show: true,
      change_handler: me.onStepReplaceBtn,
      change_scope: me,
      layout: "fit",
    });

    var proPassItems = [
      me.stepPanel,
      {
        xtype: "hiddenfield",
        name: "pID",
      },
      {
        xtype: "hiddenfield",
        name: "pAll",
      },
      {
        xtype: "hiddenfield",
        name: "pDsc",
      },
    ];

    for (var i = 1; i < 20; ++i)
      for (var j = 0; j < me.LocalStepFields.length; ++j)
        proPassItems.push({
          xtype: "hiddenfield",
          name: "p" + i + me.LocalStepFields[j],
        });
    proPassItems.push(me.addStepBtn);
    proPassItems.push(me.delStepBtn);
    me.proPass = Ext.create("Ext.form.FieldSet", {
      title: "Processing Pass ()",
      autoHeight: true,
      width: 622,
      layout: "column",
      items: proPassItems, // me.addStepBtn,me.delStepBtn],
      // buttons : [me.addStepBtn, me.delStepBtn],
      // dockedItems : [me.addStepBtn, me.delStepBtn],
      buttonAlign: "left",
    });

    var req_items = [
      {
        xtype: "textfield",
        fieldLabel: "Name",
        name: "reqName",
        emptyText: "Arbitrary string for your convenience",
        anchor: "70%",
      },
      {
        xtype: "panel",
        layout: "column",
        anchor: "98%",
        items: [
          {
            layout: "column",
            autoHeight: true,
            defaultType: "combo",
            defaults: {
              fieldStyle: "background-color: #FFFFCC; background-image: none;",
              submitEmptyText: false,
            },
            bodyPadding: 5,
            items: [
              {
                xtype: "hiddenfield",
                name: "ID",
              },
              {
                xtype: "hiddenfield",
                name: "_parent",
              },
              {
                xtype: "textfield",
                fieldLabel: "Type",
                name: "reqType",
                readOnly: true,
                columnWidth: 0.25,
              },
              {
                fieldLabel: "Priority",
                name: "reqPrio",
                store: ["1a", "1b", "2a", "2b"],
                forceSelection: true,
                mode: "local",
                selectOnFocus: true,
                columnWidth: 0.25,
              },
              {
                xtype: "textfield",
                readOnly: true,
                fieldLabel: "State",
                name: "currentState",
                columnWidth: 0.25,
              },
              {
                xtype: "hiddenfield",
                name: "reqState",
              },
              {
                xtype: "textfield",
                readOnly: true,
                fieldLabel: "Author",
                name: "reqAuthor",
                columnWidth: 0.25,
              },
            ],
          },
        ],
      },
      {
        xtype: "textfield",
        fieldLabel: "Inform also",
        name: "reqInform",
        anchor: "98%",
        emptyText: "List of DIRAC users and/or mail addresses",
      },
    ];

    req_items.push({
      xtype: "textfield",
      fieldLabel: "MC Config",
      name: "mcConfigVersion",
      anchor: "98%",
      emptyText: "BK configuration version",
    });

    req_items.push({
      xtype: "dirac.combobox",
      fieldLabel: "WG",
      name: "reqWG",
      anchor: "50%",
      extraValues: [""],
      displayField: "text",
      valueField: "name",
      queryMode: "local",
      selectOnFocus: true,
      emptyText: "Select a working group",
      submitEmptyText: false,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/getWG",
    });

    req_items.push({
      xtype: "datefield",
      anchor: "50%",
      fieldLabel: "StartingDate",
      name: "StartingDate",
      format: "Y-m-d",
      emptyText: Ext.Date.format(Ext.Date.add(new Date(), Ext.Date.YEAR, 9), "Y-m-d"),
      scope: me,
      validate: function () {
        var me = this;
        if (me.up("form").data.type != "Simulation" || me.up("form").data.state != "New" || me.up("form").data.isModel == 1) return true;
        var now = Ext.Date.format(new Date(), "Y-m-d");
        var sValue = Ext.Date.format(me.getValue(), "Y-m-d");
        if (sValue == "") {
          if (me.up("form").data.state == "New") {
            me.markInvalid("Please specify a date");
            return false;
          } else {
            return true;
          }
        }
        fields = me.up("fieldset").items;
        if (sValue <= now) {
          Ext.dirac.system_info.msg("Error", "Please do not give a date, which was in the past!", "error");
          me.markInvalid("Please do not give a date, which was in the past!");
          return false;
        }
        me.clearInvalid();
        return true;
      },
      validateOnChange: true,
      validateOnBlur: false,
    });

    req_items.push({
      xtype: "datefield",
      anchor: "50%",
      fieldLabel: "FinalizationDate",
      name: "FinalizationDate",
      format: "Y-m-d",
      scope: me,
      emptyText: Ext.Date.format(Ext.Date.add(new Date(), Ext.Date.YEAR, 10), "Y-m-d"),
      validate: function () {
        var me = this;
        if (me.up("form").data.type != "Simulation" || me.up("form").data.state != "New" || me.up("form").data.isModel == 1) return true;
        var now = Ext.Date.format(new Date(), "Y-m-d");
        var sValue = Ext.Date.format(me.getValue(), "Y-m-d");
        if (sValue == "") {
          if (me.up("form").data.state == "New") {
            me.markInvalid("Please specify a date");
            return false;
          } else {
            return true;
          }
        }
        fields = me.up("fieldset").items;
        var startDateWidget = fields.findBy(function (value) {
          if (value.name == "StartingDate") return value;
        });
        var startDate = Ext.Date.format(startDateWidget.getValue(), "Y-m-d");
        if (sValue <= now || sValue <= startDate) {
          Ext.dirac.system_info.msg("Error", "The request can not finish before start!", "error");
          me.markInvalid("The request can not finish before start !");
          return false;
        }
        me.clearInvalid();
        return true;
      },
      validateOnChange: true,
      validateOnBlur: false,
    });

    req_items.push({
      xtype: "textfield",
      fieldLabel: "RetentionRate",
      anchor: "100%",
      name: "RetentionRate",
      value: "1",
      validate: function () {
        var me = this;
        if (me.up("form").data.type != "Simulation") return true;
        if (me.getValue() > 1) {
          Ext.dirac.system_info.msg("Error", "The retention rate must be <=1", "error");
          me.markInvalid("It must be <=1!");
          return false;
        }

        me.clearInvalid();
        return true;
      },
      validateOnChange: true,
      validateOnBlur: false,
    });

    req_items.push({
      xtype: "dirac.combobox",
      fieldLabel: "Fast Simulation Type",
      name: "FastSimulationType",
      anchor: "50%",
      extraValues: [""],
      displayField: "text",
      valueField: "name",
      queryMode: "local",
      selectOnFocus: true,
      valueField: "None",
      submitEmptyText: false,
      value: "None",
      url: GLOBAL.BASE_URL + "ProductionRequestManager/getFastSimulationOpts",
      validate: function () {
        var me = this;
        if (!me.up("form").data) {
          //this is when we create a request.
          return true;
        }
        if (me.up("form").data.type != "Simulation") return true;
        if (me.getValue() == "") {
          Ext.dirac.system_info.msg("Error", "Please select a fast simulation", "error");
          me.markInvalid("Please select a fast simulation");
          return false;
        }

        me.clearInvalid();
        return true;
      },
    });

    me.Request = Ext.create("Ext.form.FieldSet", {
      title: "Request",
      autoHeight: true,
      width: 622,
      defaults: {
        submitEmptyText: false,
      },
      items: req_items,
    });

    me.Event = Ext.create("Ext.form.FieldSet", {
      title: "Event",
      autoHeight: true,
      width: 622,
      layout: "form",
      defaultType: "textfield",
      defaults: {
        submitEmptyText: false,
      },
      region: "north",
      items: [
        {
          xtype: "dirac.combobox",
          fieldLabel: "Type",
          name: "eventType",
          extraValues: [""],
          useOriginalValue: true,
          displayField: "text",
          valueField: "id",
          queryMode: "local",
          selectOnFocus: true,
          emptyText: "Select event type (if not subrequesting)",
          emptyValue: "",
          submitEmptyText: true,
          url: GLOBAL.BASE_URL + "ProductionRequestManager/bkk_event_types?addempty",
        },
        {
          xtype: "numberfield",
          fieldLabel: "Number",
          name: "eventNumber",
          submitEmptyText: false,
          emptyText: "Specify an event number (if not subrequest)",
        },
        /*
         * , { xtype : 'hiddenfield', name : '_master' }/* , { xtype :
         * 'hiddenfield', name : 'ID' }
         */
      ],
    });

    me.west = Ext.create("Ext.panel.Panel", {
      scrollable: true,
      autoHeigth: true,
      items: [me.Request, me.proPass],
      // me.simCond, me.inData
    });

    me.allbuttons = [
      {
        text: "Save",
        name: "saveButton",
        handler: me.onSave,
        scope: me,
      },
      {
        text: "Cancel",
        handler: me.onCancel,
        name: "cancelButton",
        scope: me,
      },
      {
        text: "Save without submission",
        handler: me.onSave,
        scope: me,
        name: "submitwithoutButton",
      },
      {
        text: "Submit to the production team",
        handler: me.onSubmit,
        name: "submitButton",
        scope: me,
      },
      {
        text: "Sign the request (BK OK)",
        handler: me.onBKSign,
        name: "signButton",
        scope: me,
      },
      {
        text: "Reject the request (better first comment why)",
        handler: me.onReject,
        name: "rejectButton",
        scope: me,
      },
      {
        text: "Registered Simulation Conditions are OK",
        handler: me.onSubmit,
        scope: me,
        name: "registerSimCondButton",
      },
      {
        text: "I no longer want this request",
        handler: me.onReject,
        scope: me,
        name: "noreqButton",
      },
      {
        text: "Sign the request",
        handler: me.onSign,
        scope: me,
        name: "origSignButton",
      },
      {
        text: "Save changes",
        handler: me.onSave,
        scope: me,
        name: "saveChangesButton",
      },
      {
        text: "Generate",
        handler: me.onWorkflow,
        scope: me,
        name: "generateButton",
      },
      {
        text: "Put on-hold",
        handler: me.onHold,
        scope: me,
        name: "onHoldButton",
      },
      {
        text: "Activate",
        handler: me.onActivate,
        scope: me,
        name: "activateButton",
      },
      {
        text: "Return to Tech. expert",
        handler: me.onReturn,
        scope: me,
        name: "returnTechButton",
      },
      {
        text: "Done",
        handler: me.onDone,
        scope: me,
        name: "doneButton",
      },
      {
        text: "Completed",
        handler: me.onCompleted,
        scope: me,
        name: "completedButton",
      },
      {
        text: "Reactivate",
        handler: me.onActivate,
        scope: me,
        name: "reactivateButton",
      },
      {
        text: "Cancel request (better first comment why)",
        handler: me.onCancelReq,
        scope: me,
        name: "cancelRequestButton",
      },
      {
        text: "Move to Accepted",
        handler: me.onAccepted,
        scope: me,
        name: "acceptedButton",
      },
    ];

    Ext.apply(this, {
      items: {
        xtype: "panel",
        border: false,
        anchor: "100% 100%",
        layout: "border",
        items: [
          {
            region: "west",
            width: 639,
            layout: "fit",
            items: me.west,
          },
          {
            region: "center",
            margins: "0 0 0 2",
            anchor: "100% 100%",
            layout: "border",
            items: [
              me.Event,
              {
                xtype: "fieldset",
                title: "Comments",
                layout: "fit",
                region: "center",
                margins: "5 0 0 0",
                items: {
                  xtype: "textarea",
                  hideLabel: true,
                  name: "reqComment",
                },
              },
            ],
          },
        ],
      },
      buttonAlign: "left",
      frame: true,
      buttons: me.allbuttons,
    });
    me.callParent(arguments);
  },

  initEvents: function () {
    var me = this;

    me.callParent(arguments);
    me.fireEvent("saved");
    me.fireEvent("cancelled");
  },

  setupEditor: function (data) {
    var me = this;

    me.__hideButtons();
    me.simCond.hide();
    me.inData.hide();

    var form = null;
    // by default do not add the simulation/data taking condtions to the
    // panel
    // the correct field set has to be added depending on the request
    if (data.type == "Simulation") {
      me.west.insert(1, me.simCond);
      form = me.getForm();
      form.findField("mcConfigVersion").hide();
      form.findField("eventType").setReadOnly(false);
      form.findField("mcConfigVersion").setReadOnly(false);
      me.simCond.show();
      me.simCondBtn.show();
    } else {
      me.west.insert(1, me.inData);
      form = me.getForm();
      form.findField("inProductionID").setReadOnly(false);
      form.findField("inDataQualityFlag").setReadOnly(false);
      form.findField("inTCKs").setReadOnly(false);

      me.inData.show();
      me.inDataBtn.show();
    }

    form.findField("reqWG").hide();
    form.findField("reqWG").setReadOnly(false);
    form.findField("reqName").setReadOnly(false);
    form.findField("reqPrio").setReadOnly(false);
    form.findField("ID").enable();

    form.findField("reqWG").show();
    form.findField("reqWG").enable();
    if (data.type == "Simulation") {
      form.findField("mcConfigVersion").show();
      form.findField("StartingDate").enable();
      form.findField("FinalizationDate").enable();
      form.findField("RetentionRate").enable();
      form.findField("FastSimulationType").enable();
    } else {
      form.findField("StartingDate").disable();
      form.findField("FinalizationDate").disable();
      form.findField("RetentionRate").disable();
      form.findField("FastSimulationType").disable();
    }

    if (data.type != "Simulation") {
      form.findField("eventType").setEmptyText("Defined by input data");
      form.findField("eventNumber").setEmptyText("-1 to process all events");
      form.findField("eventType").setFieldStyle({
        "background-color": "#FFFFCC",
        "background-image": "none",
      });
      form.findField("eventType").setReadOnly(true);
    } else {
      form.findField("eventType").setEmptyText("Select event type (if not subrequesting)");
      form.findField("eventType").setReadOnly(false);
      form.findField("eventType").setFieldStyle({
        "background-color": "#FFFFFF",
        "background-image": "none",
      });

      form.findField("eventNumber").setEmptyText("");
    }

    if (
      Ext.Array.contains(["diracAdmin", "lhcb_admin"], GLOBAL.USER_CREDENTIALS.group) ||
      (data.isModel && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech")
    ) {
      me.getDockedItems()[0].down("[name=saveButton]").show();
      me.getDockedItems()[0].down("[name=cancelButton]").show();
    } else if (data.state == "New") {
      me.getDockedItems()[0].down("[name=submitwithoutButton]").show();
      me.getDockedItems()[0].down("[name=submitButton]").show();
      me.getDockedItems()[0].down("[name=cancelButton]").show();
    } else if (data.state == "BK Check") {
      me.getDockedItems()[0].down("[name=signButton]").show();
      me.getDockedItems()[0].down("[name=rejectButton]").show();
      me.getDockedItems()[0].down("[name=cancelButton]").show();
    } else if (data.state == "BK OK") {
      me.getDockedItems()[0].down("[name=registerSimCondButton]").show();
      me.getDockedItems()[0].down("[name=noreqButton]").show();
      me.getDockedItems()[0].down("[name=cancelButton]").show();
    } else if (data.state == "Submitted" || data.state == "Tech OK") {
      if (GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") {
        me.getDockedItems()[0].down("[name=origSignButton]").show();
        me.getDockedItems()[0].down("[name=rejectButton]").show();
        me.getDockedItems()[0].down("[name=saveChangesButton]").show();
        me.getDockedItems()[0].down("[name=generateButton]").show();
        me.getDockedItems()[0].down("[name=cancelButton]").show();
      } else {
        me.getDockedItems()[0].down("[name=origSignButton]").show();
        me.getDockedItems()[0].down("[name=rejectButton]").show();
        me.getDockedItems()[0].down("[name=cancelButton]").show();
      }
    } else if (data.state == "PPG OK") {
      me.getDockedItems()[0].down("[name=origSignButton]").show();
      me.getDockedItems()[0].down("[name=onHoldButton]").show();
      me.getDockedItems()[0].down("[name=rejectButton]").show();
      me.getDockedItems()[0].down("[name=saveChangesButton]").show();
      me.getDockedItems()[0].down("[name=generateButton]").show();
      me.getDockedItems()[0].down("[name=cancelButton]").show();
    } else if (data.state == "On-hold") {
      me.getDockedItems()[0].down("[name=origSignButton]").show();
      me.getDockedItems()[0].down("[name=rejectButton]").show();
      me.getDockedItems()[0].down("[name=saveChangesButton]").show();
      me.getDockedItems()[0].down("[name=generateButton]").show();
      me.getDockedItems()[0].down("[name=cancelButton]").show();
    } else if (data.state == "Accepted") {
      me.getDockedItems()[0].down("[name=activateButton]").show();
      me.getDockedItems()[0].down("[name=rejectButton]").show();
      me.getDockedItems()[0].down("[name=returnTechButton]").show();
      me.getDockedItems()[0].down("[name=saveChangesButton]").show();
      me.getDockedItems()[0].down("[name=generateButton]").show();
      me.getDockedItems()[0].down("[name=cancelButton]").show();
    } else if (data.state == "Active") {
      me.getDockedItems()[0].down("[name=doneButton]").show();
      me.getDockedItems()[0].down("[name=completedButton]").show();
      me.getDockedItems()[0].down("[name=cancelRequestButton]").show();
      me.getDockedItems()[0].down("[name=saveChangesButton]").show();
      me.getDockedItems()[0].down("[name=generateButton]").show();
      me.getDockedItems()[0].down("[name=cancelButton]").show();
      me.getDockedItems()[0].down("[name=acceptedButton]").show();
    } else if (data.state == "Completed") {
      me.getDockedItems()[0].down("[name=doneButton]").show();
      me.getDockedItems()[0].down("[name=reactivateButton]").show();
      me.getDockedItems()[0].down("[name=cancelRequestButton]").show();
      me.getDockedItems()[0].down("[name=saveChangesButton]").show();
      me.getDockedItems()[0].down("[name=generateButton]").show();
      me.getDockedItems()[0].down("[name=cancelButton]").show();
    }

    if (data.ID == null) {
      var reqAuthor = GLOBAL.USER_CREDENTIALS.username;
      form.setValues({
        reqType: data.type,
        reqState: "New",
        reqPrio: "2b",
        reqAuthor: reqAuthor,
      });
      form.findField("currentState").setValue(me.data.state);
      form.findField("ID").disable();
    }
    me.setSimCond(me.data);
    me.setInData(me.data);
    me.setEventForm(me.data);
  },

  loadRecord: function (rm, r) {
    var me = this;
    var form = me.getForm();

    var id = form.findField("ID");

    if (!r || typeof r.data.ID == "undefined") {
      var reqAuthor = GLOBAL.USER_CREDENTIALS.username;
      form.setValues({
        reqType: me.data.type,
        reqState: "New",
        reqPrio: "2b",
        reqAuthor: reqAuthor,
      });
      form.findField("ID").disable();
    } else {
      form.findField("ID").enable();
    }

    if (r) {
      form.loadRecord(r);
      form.pData = r.data; // a bit more than required...
      me.pData = r.data;
    }
    form.findField("currentState").setValue(me.data.state);
    me.setRequest(rm);
    me.setProPass(rm);
    if (r) {
      me.setSimCond(rm);
      me.setInData(rm);
      me.setEventForm(rm);
      if (r.data.eventType) {
        form.findField("eventType").setAndReload(r.data.eventType);
      }
    } else {
      me.setInData(null);
      me.setEventForm({
        state: "New",
        user: reqAuthor,
        author: reqAuthor,
      });
    }
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

  onCancel: function () {
    var me = this;
    me.fireEvent("cancelled", me);
  },

  checkProcessingPass: function () {
    var me = this;
    var i;
    var pAll = "";
    var form = me.getForm();
    for (i = 1; i < 20; ++i) {
      var pApp = form.findField("p" + i + "App").getValue();
      var pVer = form.findField("p" + i + "Ver").getValue();
      if (!pApp) break;
      var pLbl = pApp + "-" + pVer;
      if (pAll) pAll = pAll + ",";
      pAll = pAll + pLbl;
    }
    form.findField("pAll").setValue(pAll);
    me.delStep(i); /* to be sure all fields are clean */
    return true;
  },

  _submit: function () {
    var me = this;
    me.getForm().submit({
      submitEmptyText: false,
      failure: function (response, action) {
        GLOBAL.APP.CF.showAjaxErrorMessage(action.response);
      },
      success: me.onSaveSuccess,
      scope: me,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/save",
      waitMsg: "Uploading the request",
    });
  },

  onSave: function () {
    var me = this;
    if (!me.getForm().isValid()) {
      Ext.dirac.system_info.msg("Error", "Please correct the wrong value(s)!");
      return;
    }
    if (!me.checkProcessingPass()) return;
    me.getForm().findField("reqState").setValue(me.data.state);
    me._submit();
  },

  fieldValue: function (name) {
    return this.getForm().findField(name).getValue();
  },

  onSubmit: function () {
    var me = this;
    var toBK_Check = false;
    var form = me.getForm();
    if (!form.isValid()) {
      Ext.dirac.system_info.msg("Error", "Please correct the wrong value(s)!");
      return;
    }
    if (form.findField("pDsc").getValue() == "Bad Step Combination") {
      Ext.MessageBox.show({
        title: "Wrong processing pass",
        msg: "Bad step combination: probably the Step visibility is not correct. Please check the step attributes",
        buttons: Ext.MessageBox.OK,
        icon: Ext.MessageBox.ERROR,
      });
      return;
    }
    if (!form.findField("simCondID").getValue()) {
      if (me.data.type != "Simulation") {
        Ext.MessageBox.show({
          title: "Incomplete request",
          msg: "Please specify input data for processing. ",
          buttons: Ext.MessageBox.OK,
          icon: Ext.MessageBox.ERROR,
        });
        return;
      }
      toBK_Check = true;
      if (
        !form.findField("simDesc").getValue() ||
        !form.findField("Generator").getValue() ||
        !form.findField("MagneticField").getValue() ||
        !form.findField("BeamEnergy").getValue() ||
        !form.findField("Luminosity").getValue() ||
        !form.findField("DetectorCond").getValue() ||
        !form.findField("BeamCond").getValue()
      ) {
        Ext.MessageBox.show({
          title: "Incomplete request",
          msg: "Specified Simulation Conditions are not yet registered. " + "Please fill ALL simulation condition fields.",
          buttons: Ext.MessageBox.OK,
          icon: Ext.MessageBox.ERROR,
        });
        return;
      }
    }
    if (!me.checkProcessingPass()) return;
    if (!form.findField("pDsc").getValue() || !form.findField("pAll").getValue()) {
      Ext.MessageBox.show({
        title: "Incomplete request",
        msg: "Specified Processing Pass is not yet registered. " + "You have to specify at least one Step ",
        buttons: Ext.MessageBox.OK,
        icon: Ext.MessageBox.ERROR,
      });
      return;
    }
    // Event type/subrequests consistency will be checked in DB part
    if (!form.findField("eventType").getValue()) {
      if (form.findField("eventNumber").getValue()) {
        Ext.MessageBox.show({
          title: "Incomplete request",
          msg: "You have specified the number of events, but no type.",
          buttons: Ext.MessageBox.OK,
          icon: Ext.MessageBox.ERROR,
        });
        return;
      }
    } else if (!form.findField("eventNumber").getValue()) {
      Ext.MessageBox.show({
        title: "Incomplete request",
        msg: "You have to specify the number of events.",
        buttons: Ext.MessageBox.OK,
        icon: Ext.MessageBox.ERROR,
      });
      return;
    }
    if (me.data.state == "BK OK") {
      me.__realSubmit();
      return;
    }
    var confirm_text = "You are about to submit the request. Note, that " + "you no longer can modify it after that. Proceed?";
    if (toBK_Check)
      confirm_text =
        "You are asking for unregistered Simulation Conditions. " +
        "You request will be send to BK Expert first for confirmation. " +
        "Note that you have to resign the request afterward. " +
        "Also note that you no longer can modify the request after submission. " +
        "Proceed?";
    Ext.MessageBox.confirm(
      "Submit",
      confirm_text,
      function (btn) {
        if (btn == "yes") this.__realSubmit();
      },
      this
    );
  },

  __realSubmit: function () {
    var me = this;
    var form = me.getForm();
    if (me.data.state == "New") {
      if (!form.findField("simCondID").getValue()) form.findField("reqState").setValue("BK Check");
      else form.findField("reqState").setValue("Submitted");
    } else if (me.data.state == "BK OK") form.findField("reqState").setValue("Submitted");
    me._submit();
  },

  onBKSign: function () {
    if (!this.fieldValue("simCondID")) {
      Ext.MessageBox.show({
        title: "Incomplete request",
        msg: "Currently Simulation Conditions must be registered with BK tools manually " + "and then selected here ('Select from BK' button).",
        buttons: Ext.MessageBox.OK,
        icon: Ext.MessageBox.ERROR,
      });
      return;
    }
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("BK OK");
    this._submit();
  },

  onSign: function () {
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("Accepted");
    this._submit();
  },

  onHold: function () {
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("On-hold");
    this._submit();
  },

  onReturn: function () {
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("PPG OK");
    this._submit();
  },

  onActivate: function () {
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("Active");
    this._submit();
  },
  onAccepted: function () {
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("Accepted");
    this._submit();
  },
  onCompleted: function () {
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("Completed");
    this._submit();
  },

  onDone: function () {
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("Done");
    this._submit();
  },

  onCancelReq: function () {
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("Cancelled");
    this._submit();
  },

  onReject: function () {
    if (!this.checkProcessingPass()) return;
    this.getForm().findField("reqState").setValue("Rejected");
    this._submit();
  },

  onSaveSuccess: function () {
    var me = this;
    me.fireEvent("saved", me);
  },

  setEventForm: function (rm) {
    var me = this;
    var form = me.getForm();
    var force = !Ext.Array.contains(["diracAdmin", "lhcb_admin"], GLOBAL.USER_CREDENTIALS.group);
    if (rm.state == "New" && rm.user == rm.author) force = false;
    if (rm.state == "New" && me.data.isModel && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") force = false;
    var evType = form.findField("eventType");
    if (me.data.type != "Simulation") {
      evType.setReadOnly(true);
    } else evType.setReadOnly(force);
    form.findField("eventNumber").setReadOnly(force);
    var emptyText = "";
    if (rm.state != "New") emptyText = "(see subrequests)";
    else if (force) emptyText = "(not yet set)";
    if (emptyText) {
      evType.setEmptyText(emptyText);
    }
  },

  onSelectFromBk: function () {
    var me = this;

    var idField = me.getForm().findField("simCondID");
    if (idField.getValue() == "") {
      me.scb = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.BkSimCondBrowser");
      me.scb.down("[name=sim-cond-select]").on("click", me.onSimCondSelected, me);
      me.scb.show();
    } else {
      idField.setValue("");
      me.setSimCond(null);
    }
  },

  onSelectInputFromBk: function () {
    var me = this;
    me.indb = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.BookkeepingInputDataBrowser");
    me.indb.down("[name=in-data-select]").on("click", me.onInDataSelected, me);
    me.indb.show();
  },

  setSimCond: function (rm) {
    var me = this;

    if (me.data.type != "Simulation") return;
    me.simCondBtn.show();
    var force = true;
    if (rm) {
      if (rm.state == "New" && rm.user == rm.author) force = false;
      if (rm.state == "New" && me.data.isModel && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") force = false;
      if (rm.state == "BK Check" && rm.group == "lhcb_bk") force = false;
    } else force = false;
    var id = me.getForm().findField("simCondID").getValue();
    if (id) me.simCond.setTitle("Simulation Conditions(ID: " + id + ")");
    else me.simCond.setTitle('Simulation Conditions  <font color="red">(not registered yet)</font>');
    if (id) me.simCondBtn.setText("Customize");
    else me.simCondBtn.setText("Select from BK");
    if (force) me.simCondBtn.hide();
    var fields = this.simCond.query("[xtype=textfield]");
    for (var i = 0; i < fields.length; ++i)
      if (force || id) {
        fields[i].setFieldStyle({
          "background-color": "#FFFFCC",
          "background-image": "none",
        });
        fields[i].setReadOnly(true);
      } else {
        fields[i].setFieldStyle({
          "background-color": "#FFFFFF",
          "background-image": "none",
        });
        fields[i].setReadOnly(false);
      }
    if (((me.data.state != "Submitted" && me.data.state != "Tech OK") || rm.group != "lhcb_ppg") && force) {
      me.getForm().findField("reqWG").setReadOnly(true);
      me.getForm().findField("StartingDate").setReadOnly(true);
      me.getForm().findField("FinalizationDate").setReadOnly(true);
      me.getForm().findField("RetentionRate").setReadOnly(true);
      me.getForm().findField("FastSimulationType").setReadOnly(true);
    } else {
      me.getForm().findField("reqWG").setReadOnly(false);
      me.getForm().findField("StartingDate").setReadOnly(false);
      me.getForm().findField("FinalizationDate").setReadOnly(false);
      me.getForm().findField("RetentionRate").setReadOnly(false);
      me.getForm().findField("FastSimulationType").setReadOnly(false);
    }
    if (rm && rm.group == "lhcb_ppg" && force) {
      me.getForm().findField("mcConfigVersion").setReadOnly(true);
    } else {
      me.getForm().findField("mcConfigVersion").setReadOnly(false);
    }
  },

  setInData: function (rm) {
    var me = this;
    if (me.data.type == "Simulation") return;
    var force = true;

    var id = "";
    if (rm) {
      if (rm.state == "New" && rm.user == rm.author) force = false;
      if (rm.state == "New" && me.data.isModel && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") force = false;
    } else force = false;
    var id = me.getForm().findField("simCondID").getValue();
    if (force) me.inDataBtn.hide();

    var prodCombo = me.getForm().findField("inProductionID");
    var prodtext = prodCombo.getValue();

    var simDescField = me.getForm().findField("simDesc");
    if (prodtext == "0" || prodtext == "") prodtext = "ALL";
    prodCombo.setAndReload(prodtext, {
      params: {
        configName: me.getForm().findField("configName").getValue(),
        configVersion: me.getForm().findField("configVersion").getValue(),
        simDesc: simDescField.getValue(),
        inProPass: me.getForm().findField("inProPass").getValue(),
        eventType: me.getForm().findField("eventType").getValue(),
      },
    });

    if (prodtext == "ALL" || (!force && id && !prodtext)) prodCombo.setValue(0);

    if (force || !id) {
      prodCombo.setFieldStyle({
        "background-color": "#FFFFCC",
        "background-image": "none",
      });
      prodCombo.setReadOnly(true);
    } else {
      prodCombo.setFieldStyle({
        "background-color": "#FFFFFF",
        "background-image": "none",
      });

      prodCombo.setReadOnly(false);
    }

    var dqCombo = me.getForm().findField("inDataQualityFlag");
    var dq = dqCombo.getValue();

    if ((dq == "" || dq == "0") && !force && id && !dq) dqCombo.setValue("ALL");

    if (force || !id) {
      dqCombo.setFieldStyle({
        "background-color": "#FFFFCC",
        "background-image": "none",
      });
      dqCombo.setReadOnly(true);
    } else {
      dqCombo.setFieldStyle({
        "background-color": "#FFFFFF",
        "background-image": "none",
      });
      dqCombo.setReadOnly(false);
    }

    var tckCombo = me.getForm().findField("inTCKs");
    var tck = tckCombo.getValue();
    if (tck == "0" || tck == "") tck = "ALL";
    tckCombo.setAndReload(tck, {
      params: {
        configName: me.getForm().findField("configName").getValue(),
        configVersion: me.getForm().findField("configVersion").getValue(),
        simDesc: simDescField.getValue(),
        inProPass: me.getForm().findField("inProPass").getValue(),
        eventType: me.getForm().findField("eventType").getValue(),
      },
    });

    if (tck == "ALL" || (!force && id && !tck)) tckCombo.setValue("ALL");

    if (force || !id) {
      tckCombo.setFieldStyle({
        "background-color": "#FFFFCC",
        "background-image": "none",
      });
      tckCombo.setReadOnly(true);
    } else {
      tckCombo.setFieldStyle({
        "background-color": "#FFFFFF",
        "background-image": "none",
      });
      tckCombo.setReadOnly(false);
    }

    simDescField.setFieldStyle({
      "background-color": "#FFFFCC",
      "background-image": "none",
    });
    simDescField.setReadOnly(true);
  },

  onSimCondSelected: function () {
    this.getForm().setValues(this.scb.detail.data);
    this.scb.close();
    this.setSimCond(null);
  },

  onInDataSelected: function () {
    var me = this;
    me.getForm().setValues(me.indb.detail.data);
    me.indb.close();
    var evType = me.indb.detail.data.evType;
    if (evType) me.getForm().findField("eventType").setValue(evType[0]);
    me.getForm().findField("inProductionID").setValue("0");
    me.setInData(null);
  },

  lastDefinedStep: function () {
    var me = this;
    var form = me.getForm();
    for (var i = 19; i > 0; --i) if (form.findField("p" + i + "App").getValue()) return i;
    return i;
  },

  dynProPass: function () {
    var me = this;
    var pp = "";
    var form = me.getForm();
    for (var i = 1; i < 20; ++i) {
      var name = form.findField("p" + i + "Pass").getValue();
      var visible = form.findField("p" + i + "Vis").getValue();
      var app = form.findField("p" + i + "App").getValue();
      if (!app) break;
      if (name && visible == "Y") {
        if (pp) pp = pp + "/" + name;
        else pp = name;
      }
    }
    if (!pp && form.findField("p1App").getValue()) pp = "Bad Step Combination";
    return pp;
  },

  delStep: function (i) {
    var me = this;
    var form = me.getForm();
    if (i < 1 || i > 19) return;

    for (; i < 20; ++i) {
      if (!form.findField("p" + i + "App").getValue()) break;
      for (var j = 0; j < me.LocalStepFields.length; ++j) form.findField("p" + i + me.LocalStepFields[j]).setValue("");
    }
    me.addStepBtn.show();
    if (!form.findField("p1App").getValue()) me.delStepBtn.hide();

    var pp = me.dynProPass();
    form.findField("pDsc").setValue(pp);
    me.proPass.setTitle("Processing Pass (" + pp + ")");

    me.stepPanel.updateDetail(form.getValues());
    me.proPass.updateLayout();
  },

  onStepReplace: function () {
    var i = this.asb.stepId;
    var sdata = this.asb.detail.data2edit(i);
    this.asb.close();

    this.getForm().setValues(sdata);

    var pp = this.dynProPass();
    this.getForm().findField("pDsc").setValue(pp);
    this.proPass.setTitle("Processing Pass (" + pp + ")");

    this.stepPanel.updateDetail(this.getForm().getValues());
    this.proPass.updateLayout();
  },

  onStepAdd: function () {
    var me = this;
    var i = me.lastDefinedStep() + 1;
    var sdata = me.asb.detail.data2edit(i);
    me.asb.close();

    me.getForm().setValues(sdata);
    me.delStepBtn.show();
    if (me.getForm().findField("p19App").getValue()) me.addStepBtn.hide();

    var pp = me.dynProPass();
    me.getForm().findField("pDsc").setValue(pp);
    me.proPass.setTitle("Processing Pass (" + pp + ")");

    me.stepPanel.updateDetail(me.getForm().getValues());
    me.proPass.updateLayout();
  },

  setProPass: function (data) {
    var force = true;
    var me = this;

    if (data) {
      if (data.state == "New" && data.user == data.author) force = false;
      if (data.state == "New" && data.isModel && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") force = false;
      if (data.state == "Submitted" && data.group == "lhcb_tech") force = false;
      if (data.state == "PPG OK" && data.group == "lhcb_tech") force = false;
      if (data.state == "On-hold" && data.group == "lhcb_tech") force = false;
      if (data.group == "lhcb_prmgr") force = false;
    } else force = false;

    var pApp1 = me.getForm().findField("p1App").getValue();
    var pApp19 = me.getForm().findField("p19App").getValue();
    var pDsc = me.getForm().findField("pDsc").getValue();
    me.proPass.setTitle("Processing Pass (" + pDsc + ")");

    if (pApp1 && !force) me.delStepBtn.show();
    else me.delStepBtn.hide();
    if (pApp19 || force) me.addStepBtn.hide();
    else me.addStepBtn.show();

    me.stepPanel.change_show = !force;
    me.stepPanel.updateDetail(me.getForm().getValues());
    me.proPass.updateLayout();
  },

  step1Filter: function () {
    var me = this;
    var form = me.getForm();
    var reqType = form.findField("reqType").getValue();
    if (reqType == "Simulation")
      return {
        ApplicationName: Ext.JSON.encode(["Gauss"]),
        Usable: Ext.JSON.encode(["Yes"]),
      };
    var inFileType = form.findField("inFileType").getValue();
    if (!inFileType) return "";
    inFileType = inFileType.split(","); // create a list of file types
    var f = {
      InputFileTypes: Ext.JSON.encode(inFileType),
      Usable: Ext.JSON.encode(["Yes"]),
    };
    return f;
  },

  stepFilter: function () {
    var i;
    var me = this;
    var form = me.getForm();
    for (i = 1; i < 20; ++i) if (!form.findField("p" + i + "App").getValue()) break;
    if (i == 1) {
      var f = me.step1Filter();
      if (!f)
        Ext.MessageBox.show({
          title: "No information yet",
          msg: "Please select input data first",
          buttons: Ext.MessageBox.OK,
          icon: Ext.MessageBox.INFO,
        });
      return f;
    }
    var oft = form
      .findField("p" + (i - 1) + "OFT")
      .getValue()
      .split(",");
    var ift = [];
    for (i = 0; i < oft.length; ++i) ift.push(oft[i].split("(")[0]);
    return {
      InputFileTypes: Ext.JSON.encode(ift),
      Usable: Ext.JSON.encode(["Yes"]),
    };
  },

  stepReplaceFilter: function (i) {
    var me = this;
    var form = me.getForm();
    if (i == 1) {
      var f = me.step1Filter();
      if (!f) {
        Ext.MessageBox.show({
          title: "No information yet",
          msg: "Please select input data first",
          buttons: Ext.MessageBox.OK,
          icon: Ext.MessageBox.INFO,
        });
        return f;
      }
    } else {
      var oft = form
        .findField("p" + (i - 1) + "OFT")
        .getValue()
        .split(",");
      var ift = [];
      for (j = 0; j < oft.length; ++j) ift.push(oft[j].split("(")[0]);
      f = {
        InputFileTypes: Ext.JSON.encode(ift),
        Usable: Ext.JSON.encode(["Yes"]),
      };
    }
    if (i == 19) return f;
    var nift = form
      .findField("p" + (i + 1) + "IFT")
      .getValue()
      .split(",");
    if (!nift.length) return f;
    var oft = [];
    for (j = 0; j < nift.length; ++j) oft.push(nift[j].split("(")[0]);
    if (oft.length > 0 && oft[0] != "") f["OutputFileTypes"] = Ext.JSON.encode(oft);
    return f;
  },

  onAddStepBtn: function () {
    var me = this;
    var f = me.stepFilter();
    if (!f) return;
    me.asb = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.StepAdder", {
      operation: "Add",
      stepfilter: f,
      pr: me,
    });

    me.asb.down("[name=step-add]").on("click", me.onStepAdd, me);
    me.asb.show();
  },

  onStepReplaceBtn: function (button) {
    var me = this;
    var f = me.stepReplaceFilter(button.stepId);
    if (!f) return;
    me.asb = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.StepAdder", {
      operation: "Replace",
      stepfilter: f,
      stepId: button.stepId,
      pr: me,
    });
    me.asb.down("[name=step-add]").on("click", me.onStepReplace, me);
    me.asb.show();
  },

  onDelStepBtn: function () {
    this.delStep(this.lastDefinedStep());
  },

  onReqTypeSelect: function (combo, record, index) {
    if (combo.getValue() == "Simulation") return;
    Ext.MessageBox.show({
      title: "Not implemented",
      msg: combo.getValue() + " request type is not implemented yet. Sorry.",
      buttons: Ext.MessageBox.OK,
      icon: Ext.MessageBox.INFO,
    });
    combo.setValue("Simulation");
  },

  setRequest: function (rm) {
    var me = this;
    var form = me.getForm();
    var id = form.findField("ID").getValue();
    var force = true;

    if (!rm) force = false;
    else if (rm.state == "New" && rm.user == rm.author) force = false;
    else if (rm.state == "New" && me.data.isModel && GLOBAL.USER_CREDENTIALS.group == "lhcb_tech") force = false;
    form.findField("reqName").setReadOnly(force);
    form.findField("reqPrio").setReadOnly((me.data.state != "Submitted" && me.data.state != "Tech OK") || rm.group != "lhcb_ppg");
  },

  onWorkflow: function () {
    var me = this;
    var prw = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.PrWorkflow", {
      pData: me.pData,
    });
    prw.show();
  },
  __hideButtons: function () {
    var me = this;
    me.getDockedItems()[0].down("[name=saveButton]").hide();
    me.getDockedItems()[0].down("[name=cancelButton]").hide();
    me.getDockedItems()[0].down("[name=submitwithoutButton]").hide();
    me.getDockedItems()[0].down("[name=submitButton]").hide();
    me.getDockedItems()[0].down("[name=signButton]").hide();
    me.getDockedItems()[0].down("[name=rejectButton]").hide();
    me.getDockedItems()[0].down("[name=registerSimCondButton]").hide();
    me.getDockedItems()[0].down("[name=noreqButton]").hide();
    me.getDockedItems()[0].down("[name=origSignButton]").hide();
    me.getDockedItems()[0].down("[name=rejectButton]").hide();
    me.getDockedItems()[0].down("[name=saveChangesButton]").hide();
    me.getDockedItems()[0].down("[name=generateButton]").hide();
    me.getDockedItems()[0].down("[name=onHoldButton]").hide();
    me.getDockedItems()[0].down("[name=activateButton]").hide();
    me.getDockedItems()[0].down("[name=returnTechButton]").hide();
    me.getDockedItems()[0].down("[name=doneButton]").hide();
    me.getDockedItems()[0].down("[name=completedButton]").hide();
    me.getDockedItems()[0].down("[name=cancelRequestButton]").hide();
    me.getDockedItems()[0].down("[name=reactivateButton]").hide();
    me.getDockedItems()[0].down("[name=acceptedButton]").hide();
  },
  __readOnlyAfterRender: function (field) {
    field.getEl().dom.readOnly = field.readOnly;
    if (field.trigger) field.trigger.setDisplayed(!field.readOnly);
  },
  removeProcessingPasses: function () {
    var me = this;
    var form = me.getForm();
    me.addStepBtn.show();
    me.delStepBtn.hide();
    me.proPass.setTitle("Processing Pass ()");

    me.stepPanel.updateDetail(form.getValues());
    me.proPass.updateLayout();
  },
});
