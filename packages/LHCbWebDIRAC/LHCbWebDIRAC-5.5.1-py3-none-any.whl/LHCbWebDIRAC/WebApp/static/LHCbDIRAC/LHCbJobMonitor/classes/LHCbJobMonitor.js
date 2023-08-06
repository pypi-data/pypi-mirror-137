/*
 * ! Ext JS Library 4.0 Copyright(c) 2006-2011 Sencha Inc. licensing@sencha.com
 * http://www.sencha.com/license
 */
/**
 * LHCb specific JobMonitor page. It inherits from
 *
 * @link{DIRAC.JobMonitor.classes.JobMonitor} class.
 * @class LHCbDIRAC.LHCbJobMonitor.classes.LHCbJobMonitor
 * @extends DIRAC.JobMonitor.classes.JobMonitor
 */
Ext.define("LHCbDIRAC.LHCbJobMonitor.classes.LHCbJobMonitor", {
  extend: "DIRAC.JobMonitor.classes.JobMonitor",
  initComponent: function () {
    var me = this;
    me.callParent();
    me.launcher.title = "LHCb Job Monitor";
  },
  buildUI: function () {
    var me = this;
    me.callParent();
    me.leftPanel.addTextFieldSelector({
      RunNumbers: {
        name: "Run Number(s)",
        type: "number",
      },
    });

    me.lhcbFields = [
      "SystemPriority",
      "VerifiedFlag",
      "RetrievedFlag",
      "StartExecTime",
      "JobSplitType",
      "ApplicationNumStatus",
      "MasterJobID",
      "KilledFlag",
      "RescheduleTime",
      "RunNumber",
      "ISandboxReadyFlag",
      "HeartBeatTime",
      "EndExecTime",
      "UserPriority",
      "DeletedFlag",
      "TaskQueueID",
    ];
    var dataFieldsLength = me.dataFields.length;
    var columnsLength = me.grid.columns.length;
    for (var i = 0; i < me.lhcbFields.length; i++) {
      if (!me.__isDataFieldContains(me.dataFields, me.lhcbFields[i])) {
        me.dataFields[dataFieldsLength] = {
          name: me.lhcbFields[i],
        };
        dataFieldsLength++;
      }
      if (!me.__isCoulmnsContains(me.grid.columns, me.lhcbFields[i])) {
        Ext.apply(
          me.grid.columns[columnsLength],
          Ext.create("Ext.grid.column.Column", {
            scope: me,
            header: me.lhcbFields[i],
            sortable: true,
            dataIndex: me.lhcbFields[i],
            align: "left",
            hidden: true,
          })
        );
        columnsLength++;
      }
    }
    // refresh the data store fields list.
    Ext.apply(me.dataStore.fields, me.dataFields);
  },
  __isDataFieldContains: function (list, value) {
    var found = false;
    var i = 0;
    while (!(found = list[i].name == value) && i < list.length - 1) i++;
    return found;
  },
  __isCoulmnsContains: function (columns, value) {
    var found = false;
    var i = 0;
    while (!(found = columns[i].dataIndex == value) && i < columns.length - 1) i++;
    return found;
  },
});
