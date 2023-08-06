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
Ext.define("LHCbDIRAC.BookkeepingSimDescription.classes.SimulationEditor", {
  extend: "Ext.form.Panel",
  initComponent: function () {
    var me = this;
    var buttons = [
      {
        text: "Save",
        handler: me.onSave,
        scope: me,
      },
      {
        text: "Cancel",
        handler: me.onCancel,
        scope: me,
      },
    ];

    Ext.apply(me, {
      items: [
        {
          xtype: "textfield",
          fieldLabel: "Simulation Description",
          name: "SimDescription",
          anchor: "80%",
        },
        {
          xtype: "textfield",
          fieldLabel: "Beam Condition",
          name: "BeamCond",
          anchor: "80%",
        },
        {
          xtype: "textfield",
          fieldLabel: "Beam energy",
          name: "BeamEnergy",
          anchor: "80%",
        },
        {
          xtype: "textfield",
          fieldLabel: "Generator",
          name: "Generator",
          anchor: "80%",
        },
        {
          xtype: "textfield",
          fieldLabel: "Magnetic field",
          name: "MagneticField",
          anchor: "80%",
        },
        {
          xtype: "textfield",
          fieldLabel: "Detector condition",
          name: "DetectorCond",
          anchor: "80%",
        },
        {
          xtype: "textfield",
          fieldLabel: "Luminosity",
          name: "Luminosity",
          anchor: "80%",
        },
        {
          xtype: "textfield",
          fieldLabel: "G4settings",
          name: "G4settings",
          anchor: "80%",
        },
        {
          xtype: "combo",
          fieldLabel: "Visible",
          name: "Visible",
          store: ["Y", "N"],
          forceSelection: true,
          mode: "local",
          triggerAction: "all",
          selectOnFocus: true,
          autoCreate: {
            tag: "input",
            type: "text",
            size: "5",
            autocomplete: "off",
          },
        },
        {
          xtype: "hidden",
          name: "SimId",
        },
      ],
      buttonAlign: "left",
      frame: true,
      buttons: buttons,
    });
    me.callParent(arguments);
  },
  onCancel: function () {
    var me = this;
    me.scope.editor.hide();
  },

  _onSaveSuccess: function (form, response) {
    var me = this;
    if (response.result.success == "false") {
      Ext.Msg.alert("Failure", response.result.error);
    } else {
      Ext.Msg.alert("Info", response.result.result);
      me.scope.grid.getStore().load();
      me.scope.editor.hide();
    }
  },
  _onFailure: function (form, action) {
    switch (action.failureType) {
      case Ext.form.action.Action.CLIENT_INVALID:
        Ext.Msg.alert("Failure", "Form fields may not be submitted with invalid values");
        break;
      case Ext.form.action.Action.CONNECT_FAILURE:
        Ext.Msg.alert("Failure", "Ajax communication failed");
        break;
      case Ext.form.action.Action.SERVER_INVALID:
        Ext.Msg.alert("Failure", action.result.msg);
      default:
        Ext.Msg.alert("Failure", action.result.message);
    }
  },
  _submit: function () {
    this.getForm().submit({
      failure: this._onFailure,
      success: this._onSaveSuccess,
      scope: this,
      url: this.fieldValue("SimId") ? "BookkeepingSimDescription/simulationupdate" : "BookkeepingSimDescription/simulationinsert",
      waitMsg: "Saving simulation conditions",
    });
  },

  onSave: function () {
    this._submit();
  },

  fieldValue: function (name) {
    return this.getForm().findField(name).getValue();
  },
});
