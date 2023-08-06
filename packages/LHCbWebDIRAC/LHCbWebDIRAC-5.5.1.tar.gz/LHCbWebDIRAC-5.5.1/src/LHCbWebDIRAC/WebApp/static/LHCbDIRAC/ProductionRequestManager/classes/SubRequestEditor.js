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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.SubRequestEditor", {
  extend: Ext.form.Panel,

  initComponent: function () {
    var me = this;

    me.Event = new Ext.form.FieldSet({
      title: "Event",
      autoHeight: true,
      width: 622,
      layout: "column",
      defaultType: "textfield",
      region: "north",
      items: [
        {
          xtype: "dirac.combobox",
          fieldLabel: "Type",
          name: "eventType",
          useOriginalValue: true,
          displayField: "text",
          valueNotFoundText: true,
          extraValues: [""],
          valueField: "id",
          forceSelection: true,
          queryMode: "local",
          selectOnFocus: true,
          emptyText: "Select event type",
          submitEmptyText: false,
          url: GLOBAL.BASE_URL + "ProductionRequestManager/bkk_event_types?addempty",
        },
        {
          xtype: "numberfield",
          fieldLabel: "Number",
          name: "eventNumber",
        },
        {
          xtype: "hidden",
          name: "ID",
        },
        {
          xtype: "hidden",
          name: "_parent",
        },
        {
          xtype: "hidden",
          name: "_master",
        },
        {
          xtype: "hidden",
          name: "reqType",
        },
        {
          xtype: "hidden",
          name: "reqState",
        },
        {
          xtype: "hidden",
          name: "reqPrio",
        },
        {
          xtype: "hidden",
          name: "reqWG",
        },
        {
          xtype: "hidden",
          name: "simDesc",
        },
        {
          xtype: "hidden",
          name: "pDsc",
        },
        {
          xtype: "hidden",
          name: "pAll",
        },
        {
          xtype: "hidden",
          name: "reqInform",
        },
        {
          xtype: "hidden",
          name: "IsModel",
        },
        {
          xtype: "hidden",
          name: "mcConfigVersion",
        },
      ],
    });

    me.Original = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.RequestDetail", {
      title: "Original request ",
      scrollable: true,
      frame: true,
    });

    Ext.apply(me, {
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
            items: me.Original,
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
      buttons: [
        {
          text: "Save",
          handler: me.onSave,
          scope: this,
        },
        {
          text: "Cancel",
          handler: me.onCancel,
          scope: me,
        },
      ],
    });
    me.callParent(arguments);
  },

  initEvents: function () {
    var me = this;
    me.fireEvent("saved");
  },

  onCancel: function () {
    var me = this;
    me.fireEvent("cancelled", me);
  },

  onSave: function () {
    var me = this;
    var form = me.getForm();
    if (!form.findField("eventType").getValue() || !form.findField("eventNumber").getValue()) {
      Ext.MessageBox.show({
        title: "Incomplete subrequest",
        msg: "You have to specify event type and number. " + "Please fill ALL simulation condition fields.",
        buttons: Ext.MessageBox.OK,
        icon: Ext.MessageBox.ERROR,
      });
      return;
    }

    form.findField("_parent").setValue(me.parentPath[0]);
    form.findField("_master").setValue(me.parentPath[me.parentPath.length - 1]);
    form.submit({
      failure: function (response, action) {
        GLOBAL.APP.CF.showAjaxErrorMessage(action.response);
      },
      success: me.onSaveSuccess,
      scope: me,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/save",
      waitMsg: "Uploading the request",
    });
  },

  onSaveSuccess: function () {
    var me = this;
    me.fireEvent("saved", this);
  },

  loadRecord: function (r, setro) {
    var me = this;
    var form = me.getForm();

    if (r) {
      form.loadRecord(r);
      me.pData = r.data; // a bit more than required...
      form.findField("eventType").setRawValue(r.get("eventType"));
      if (setro) {
        form.findField("eventType").setReadOnly(true);
        form.findField("eventNumber").setReadOnly(true);
      }
    }

    if (!r || typeof r.data.ID == "undefined") {
      form.findField("ID").disable();
    }
  },
});
