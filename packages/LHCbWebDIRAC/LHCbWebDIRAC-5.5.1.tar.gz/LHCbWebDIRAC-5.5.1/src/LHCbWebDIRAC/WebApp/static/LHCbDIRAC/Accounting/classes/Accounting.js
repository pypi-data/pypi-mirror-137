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
 * It is the LHCb specific accounting. The RightPanle is replaced to a Presenter
 * view as well LHCb specific accounting types are added.
 */
Ext.define("LHCbDIRAC.Accounting.classes.Accounting", {
  extend: "DIRAC.Accounting.classes.Accounting",
  requires: ["DIRAC.Accounting.classes.Accounting"],
  timeout: 7200000, // 2 hours
  loadState: function (oData) {
    var me = this;
    me.rightPanel.loadState(oData);
  },
  getStateData: function () {
    var me = this;
    var oReturn = me.rightPanel.getStateData();

    return oReturn;
  },
  initComponent: function () {
    var me = this;

    me.callParent();

    me.reportsDesc["Accounting"]["DataStorage"] = {
      title: "Data Storage",
      selectionConditions: [
        ["DataType", "DataType"],
        ["EventType", "EventType"],
        ["FileType", "FileType"],
        ["ProcessingPass", "Processingpass"],
        ["StorageElement", "StorageElement"],
        ["Production", "Production"],
        ["Activity", "Activity"],
        ["Conditions", "Conditions"],
      ],
    };
    me.reports["Accounting"].push(["DataStorage", "Data Storage"]);

    me.reportsDesc["Accounting"]["UserStorage"] = {
      title: "User Storage",
      selectionConditions: [
        ["User", "User"],
        ["StorageElement", "StorageElement"],
      ],
    };
    me.reports["Accounting"].push(["UserStorage", "User Storage"]);

    me.reportsDesc["Accounting"]["Storage"] = {
      title: "Storage",
      selectionConditions: [
        ["Directory", "Directory"],
        ["StorageElement", "StorageElement"],
      ],
    };
    me.reports["Accounting"].push(["Storage", "Storage"]);

    me.reportsDesc["Accounting"]["JobStep"] = {
      title: "Job step",
      selectionConditions: [
        ["ProcessingStep", "ProcessingStep"],
        ["ProcessingType", "ProcessingType"],
        ["EventType", "EventType"],
        ["FinalStepState", "FinalStepState"],
        ["Site", "Site"],
        ["JobGroup", "JobGroup"],
        ["RunNumber", "RunNumber"],
      ],
    };
    me.reports["Accounting"].push(["JobStep", "JobStep"]);

    me.reportsDesc["Accounting"]["Popularity"] = {
      title: "Data popularity",
      selectionConditions: [
        ["DataType", "DataType"],
        ["EventType", "EventType"],
        ["FileType", "FileType"],
        ["ProcessingPass", "ProcessingPass"],
        ["StorageElement", "StorageElement"],
        ["Production", "Production"],
        ["Activity", "Activity"],
        ["Conditions", "Conditions"],
      ],
    };
    me.reports["Accounting"].push(["Popularity", "Data popularity"]);
  },
  buildUI: function () {
    var me = this;

    me.callParent();
    /***********************************************************************
     * Add LHCb specific accounting
     */

    me.cmbDomain.store.add(
      {
        text: "DataStorage",
        value: "DataStorage",
      },
      {
        text: "UserStorage",
        value: "UserStorage",
      },
      {
        text: "Storage",
        value: "Storage",
      },
      {
        text: "JobStep",
        value: "JobStep",
      },
      {
        text: "Data Popularity",
        value: "Popularity",
      }
    );
    /** *END LHCb specific accounting plots * */
  },
});
