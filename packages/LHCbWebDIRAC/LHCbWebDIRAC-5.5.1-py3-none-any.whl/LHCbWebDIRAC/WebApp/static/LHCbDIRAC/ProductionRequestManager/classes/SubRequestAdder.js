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
Ext.define("LHCbDIRAC.ProductionRequestManager.classes.SubRequestAdder", {
  extend: "Ext.window.Window",
  requires: ["LHCbDIRAC.ProductionRequestManager.classes.RequestDetail"],

  alias: "widget.subrequestadder",

  plain: true,
  resizable: false,
  modal: true,
  closeAction: "hide",
  initComponent: function () {
    var me = this;
    me.master = Ext.create("LHCbDIRAC.ProductionRequestManager.classes.RequestDetail", {
      ID: me.gridData.ID,
      minWidth: 200,
      region: "center",
      frame: true,
      title: "Master request",
      scrollable: true,
    });
    me.master.on(
      "afterrender",
      function () {
        me.master.updateDetail(me.gridData);
      },
      me
    );

    var store = new Ext.data.JsonStore({
      fields: [
        {
          name: "eventType",
        },
        {
          name: "eventNumber",
          type: "int",
        },
      ],
      data: [],
    });
    store.on("datachanged", me.onStoreChanged, me);

    me.subrq = new Ext.grid.Panel({
      region: "center",
      frame: true,
      margins: "0 0 5 0",
      store: store,
      columns: [
        {
          header: "Event type",
          dataIndex: "eventType",
        },
        {
          header: "Events requested",
          dataIndex: "eventNumber",
        },
      ],
      stripeRows: true,
      title: "Subrequests to create",
      autoHeight: false,
      autoWidth: true,
      viewConfig: {
        forceFit: true,
      },
    });
    me.menu = new Ext.menu.Menu();
    me.menu.add({
      handler: function () {
        var r = md.subrq.getSelectionModel().getSelected();
        me.subrq.store.remove(r);
        me.onStoreChanged(me.subrq.store);
      },
      scope: me,
      text: "Remove",
    });

    me.subrq.on("cellclick", me.onRowClick, me);

    me.evset = Ext.create("Ext.form.FieldSet", {
      region: "south",
      title: "Select event type to add as subrequest",
      autoHeight: true,
      width: 622,
      items: [
        {
          xtype: "dirac.combobox",
          fieldLabel: "Type",
          id: "dirac-combobox-select-eventtype",
          name: "eventType",
          useOriginalValue: true,
          displayField: "text",
          valueNotFoundText: true,
          valueField: "id",
          forceSelection: true,
          queryMode: "local",
          selectOnFocus: true,
          emptyText: "Select event type",
          submitEmptyText: false,
          url: GLOBAL.BASE_URL + "ProductionRequestManager/bkk_event_types?addempty",
          listeners: {
            select: me.onEventTypeSelect,
            scope: me,
          },
        },
        {
          xtype: "panel",
          layout: "column",
          border: false,
          items: [
            {
              width: 300,
              layout: "column",
              autoHeight: true,
              items: {
                xtype: "numberfield",
                fieldLabel: "Number",
                name: "eventNumber",
                anchor: "100%",
              },
            },
            {
              autoWidth: true,
              items: {
                xtype: "button",
                text: "Add",
                handler: me.onAddButton,
                scope: me,
              },
            },
          ],
        },
      ],
    });

    me.bulkset = Ext.create("Ext.form.FieldSet", {
      region: "south",
      autoHeight: true,
      width: 622,
      items: [
        {
          xtype: "panel",
          layout: "column",
          border: false,
          items: [
            {
              width: 450,
              layout: "column",
              autoHeight: true,
              items: {
                xtype: "textareafield",
                width: 450,
                fieldLabel: "Add multiple",
                name: "bulkAddTest",
                emptyText: "List of event types and number of events. For example to generate 15 minbias events:\n30000000 15",
                anchor: "100%",
              },
            },
            {
              autoWidth: true,
              items: {
                xtype: "button",
                text: "Add in bulk",
                handler: me.onBulkAddButton,
                scope: me,
              },
            },
          ],
        },
      ],
    });

    me.east = Ext.create("Ext.panel.Panel", {
      region: "east",
      split: true,
      width: 600,
      minWidth: 600,
      border: false,

      layout: "border",
      items: [me.subrq, me.evset, me.bulkset],

      buttonAlign: "center",
      buttons: [
        {
          text: "Create",
          disabled: true,
          name: "srq-create-btn",
          handler: me.onCreate,
          scope: me,
        },
        {
          text: "Cancel",
          handler: me.close,
          scope: me,
        },
      ],
    });

    me.form = Ext.create("Ext.form.Panel", {
      border: false,
      items: {
        xtype: "panel",
        layout: "border",
        frame: true,
        border: false,
        anchor: "100% 100%",
        items: [me.master, me.east],
      },
    });

    Ext.apply(me, {
      width: 950,
      height: 450,
      minWidth: 500,
      minHeight: 300,
      maximizable: true,
      modal: true,
      layout: "fit",
      items: me.form,
    });

    me.callParent(arguments);
  },
  initEvents: function () {
    var me = this;

    me.callParent(arguments);
    me.fireEvent("saved");
  },

  onEventTypeSelect: function (combo, record, index) {
    if (combo.getValue() == 99999999) combo.setValue("");
  },
  onBulkAddButton: function () {
    var helpText =
      "Expected all lines to contain two numbers separated by a space. <br>" +
      "The first number is the event type and the second is the number of events. ";
    var me = this;
    var form = me.form.getForm();
    var data = form.findField("bulkAddTest").value;
    if (!data) {
      Ext.Msg.alert("No input specified", helpText);
      return;
    }

    data = data.trim();
    var errorMsg = "";
    var parsedData = data.split("\n").map(function (s) {
      var match = /^(\d+) (\d+)$/.exec(s);
      if (match) {
        evtype = match[1];
        evnumber = match[2];
        if (!me.evset.items.get("dirac-combobox-select-eventtype").getStore().getById(evtype)) {
          errorMsg += '\n"Unrecognised event type: ' + evtype + '"';
          return null;
        }
        return {
          eventType: evtype,
          eventNumber: evnumber,
        };
      } else {
        errorMsg += '<br>"' + s + '"';
        return null;
      }
    });

    if (errorMsg) {
      Ext.Msg.alert("Invalid line in input", helpText + "<br>Errors parsing the following lines: " + errorMsg);
      return;
    } else {
      parsedData.forEach(function (o) {
        me.subrq.store.add(o);
      });
    }
  },
  onAddButton: function () {
    var me = this;
    var form = me.form.getForm();
    var evtype = form.findField("eventType").getValue();
    var evnumber = form.findField("eventNumber").getValue();
    if (!evtype || !evnumber) {
      Ext.Msg.alert("Please specify information", "Both event type and number must be specified");
      return;
    }
    me.subrq.store.add({
      eventType: evtype,
      eventNumber: evnumber,
    });
    me.onStoreChanged(this.subrq.store);
  },
  onStoreChanged: function (store) {
    var me = this;
    var btn = me.down("[name=srq-create-btn]");
    if (store.getCount()) btn.enable();
    else btn.disable();
  },
  onRowClick: function (grid, td, cellIndex, record, tr, rowIndex, e, eOpts) {
    this.menu.showAt(e.getXY());
  },
  onCreate: function () {
    var me = this;
    var store = me.subrq.store;
    for (var i = 0; i < store.getCount(); ++i) {
      var r = store.getAt(i);
      me.saveOne(r.data.eventType, r.data.eventNumber);
    }
    me.fireEvent("saved", me);
    me.close();
  },
  saveOne: function (evtype, evnumber) {
    var me = this;
    if (!evtype || !evnumber) {
      Ext.MessageBox.show({
        title: "Incomplete subrequest",
        msg: "You have to specify event type and number. ",
        buttons: Ext.MessageBox.OK,
        icon: Ext.MessageBox.ERROR,
      });
      return;
    }
    var pdict = {
      _master: this.gridData.ID,
      _parent: this.gridData.ID,
      eventType: evtype,
      eventNumber: evnumber,
    };

    Ext.Ajax.request({
      timeout: 120000,
      url: GLOBAL.BASE_URL + "ProductionRequestManager/save",
      method: "POST",
      params: pdict,
      scope: me,
      success: function (response) {
        if (response) {
          // check that it is really OK... AZ: !! ??
          var str = "";
          try {
            var result = Ext.decode(response.responseText);
            if (!result.OK) str = result.Message;
          } catch (e2) {
            str = "unparsable reply from the portal: " + e2.message;
          }
          if (str) {
            Ext.MessageBox.show({
              title: "Subrequest create failed",
              msg: str,
              buttons: Ext.MessageBox.OK,
              icon: Ext.MessageBox.ERROR,
            });
            return;
          }
        }
      },
      failure: function (response) {
        GLOBAL.APP.CF.showAjaxErrorMessage(response);
      },
    });
  },
});
