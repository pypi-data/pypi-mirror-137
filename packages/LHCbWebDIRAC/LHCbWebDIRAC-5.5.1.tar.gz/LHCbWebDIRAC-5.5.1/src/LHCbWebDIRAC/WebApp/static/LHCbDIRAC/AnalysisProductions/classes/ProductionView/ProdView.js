/*****************************************************************************\
* (c) Copyright 2020 CERN for the benefit of the LHCb Collaboration           *
*                                                                             *
* This software is distributed under the terms of the GNU General Public      *
* Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   *
*                                                                             *
* In applying this licence, CERN does not waive the privileges and immunities *
* granted to it by virtue of its status as an Intergovernmental Organization  *
* or submit itself to any jurisdiction.                                       *
\*****************************************************************************/
var anaProdSummaryTemplate = new Ext.XTemplate(`
<div class="ap-summary">
  <div class="ap-header" onclick="apToggleDisplay(this)"> <code class="ap-id">{requestID:htmlEncode}</code>
    <code class="ap-name">{name:htmlEncode}</code>
    <div class="ap-header-padding"></div>

    <tpl if='["active", "error"].includes(state)'>
      <code>{[
        Ext.util.Format.percent(
          values.transformations.reduce(
            function (total, currentValue) {
              if (currentValue.fileCounts) {
                total *= currentValue.fileCounts.Processed / currentValue.fileCounts.Total;
              }
              return total;
            }, 1),
          "0.00")
      ]} processed</code>
    <tpl elseif='["replicating"].includes(state)'>
      <code>{[
        Ext.util.Format.percent(values.numOutputFilesAtCERN/values.numOutputFiles, "0.00")
      ]} replicated</code>
    </tpl>

    <img src="static/LHCbDIRAC/AnalysisProductions/images/ap-status-{state:htmlEncode}.svg">
    <!-- <button onClick="alert();">Copy output pattern</button> -->
    <!-- <button onClick="alert();">Download metadata</button> -->
  </div>

  <div class="ap-details" style="display: none;">
    <div style="display: flex; flex-wrap: wrap;">
      <label>Output pattern:</label>
      <div class="ap-value-container">
        <input class="ap-value ap-output-pattern" readonly="readonly" value='{outputPattern:escape}' type="text">
        <div class="ap-toolbar">
          <span class="ap-toolbar-button" onclick="apSelectValue(this);">Select All</span>
          <span class="ap-toolbar-button" onclick="apCopyValue(this);">Copy</span>
        </div>
      </div>
      <input class="ap-lfns" type="hidden" value='{[values.LFNs.join("&#10;")]}'>
      <input class="ap-pfns" type="hidden" value='{[values.PFNs.join("&#10;")]}'>
      <button onClick="apCopyLFNs(this);">Copy output LFNs</button>
      <button onClick="apCopyPFNs(this);">Copy output PFNs</button>

      <div class="ap-break"></div>

      <div>
        <label>Output size:</label>
        <code>{outputSize:fileSize} from {numOutputFiles:number(',')} files
          <tpl if='(values.fractionAtCERN = values.numOutputFilesAtCERN/values.numOutputFiles) < 1'>
            <span style='color: red;'>
          </tpl>
            ({fractionAtCERN:percent('0.00')} of files replicated to CERN)
          <tpl if='values.fractionAtCERN < 1'>
            </span>
          </tpl>
        </code>
      </div>

      <div class="ap-break"></div>

      <label>Input BK path:</label>
      <div class="ap-value-container">
        <input class="ap-value" readonly="readonly" value='{productionInputQuery:escape}' type="text">
        <div class="ap-toolbar">
          <span class="ap-toolbar-button" onclick="apSelectValue(this);">Select All</span>
          <span class="ap-toolbar-button" onclick="apCopyValue(this);">Copy</span>
        </div>
      </div>
      <!-- <button onClick='alert();'>Open in Bookkeeping</button> -->

      <tpl for="transformations">
        <div class="ap-sep"></div>

        <label>Transformation {transformationID:number('0')}</label>
        <tpl if='fileCounts && fileCounts.Total && !["Archived", "Deleted", "Cleaned", "Completed"].includes(transformationStatus)'>
          <span style='color: red;'>
            <code> {[Ext.util.Format.percent(values.fileCounts.Processed/values.fileCounts.Total, '0.00')]} of files processed </code>
          </span>
        </tpl>
        <!-- <button onClick='alert();'>View Transformation</button> -->
        <button onClick="window.open('{logsURL:escape}');">View Job Logs</button>

        <tpl for="steps">
          <div class="ap-break"></div>

          <div>
            <label>StepID:</label>
            <code>{stepID:number('0')}</code>
            <!-- <button onClick='alert();'>View Step</button> -->
          </div>
          <div>
            <label>Application:</label>
            <code>{application:htmlEncode}</code>
          </div>
          <div>
            <label>Extras:</label>
            <tpl for="extras">
              <code>{.:htmlEncode}</code>
            </tpl>
          </div>
          <tpl if='values.GitLabURL'>
            <button onClick="window.open('{GitLabURL:escape}');">
              <i class="fa fa-gitlab" aria-hidden="true"></i>
              View on GitLab
            </button>
          </tpl>

          <div class="ap-break"></div>

          <label>Options:</label>
          <div class="ap-value-container">
            <input class="ap-value" type="text" readonly="readonly"
                    value="{options:htmlEncode}">
            <div class="ap-toolbar">
              <span class="ap-toolbar-button" onclick="apSelectValue(this);">Select All</span>
              <span class="ap-toolbar-button" onclick="apCopyValue(this);">Copy</span>
            </div>
          </div>
        </tpl>
      </tpl>
    </div>
  </div>
</div>
`);

Ext.define("LHCbDIRAC.AnalysisProductions.classes.ProductionView.ProdView", {
  extend: "Ext.view.View",
  alias: "widget.AnalysisProductions.classes.ProductionView.ProdView",
  itemTpl: anaProdSummaryTemplate,
});

/*
  Utility functions used by the anaProdSummaryTemplate above
*/
function apToggleDisplay(me) {
  const elm = me.closest(".ap-summary").querySelector(".ap-details");
  if (elm.style.display === "none") {
    elm.style.display = "block";
  } else {
    elm.style.display = "none";
  }
  Ext.getCmp(me.closest(".ap-info-display-panel").id).updateLayout();
}

function apCopyPatternsAsJSON(me) {
  // Find each section corresponding to a production
  const elm = me.closest(".ap-info-display-panel");
  const sections = elm.querySelectorAll(".ap-summary");
  if (sections.length === 0) {
    Ext.dirac.system_info.msg("Error", "Nothing found to copy!", "error");
    return;
  }

  // Extract the production names and output patterns from each section
  var result = {};
  for (const productionDetails of sections) {
    const name = productionDetails.querySelector(".ap-name");
    if (!name) {
      Ext.dirac.system_info.msg("Error", "Failed to find name for element!", "error");
      return;
    }
    const value = productionDetails.querySelector(".ap-output-pattern");
    if (!value) {
      Ext.dirac.system_info.msg("Error", "Failed to find output pattern for element!", "error");
      return;
    }
    result[name.textContent] = value.value;
    console.log(name.textContent + ":" + value.value);
  }

  // Copy pretty printed JSON to the clipboard
  apDoCopy(JSON.stringify(result, null, 4));
}

function apSelectValue(btn) {
  const input = btn.closest(".ap-value-container").querySelector(".ap-value");
  input.focus();
  input.select();
}

function apCopyValue(btn) {
  apDoCopy(btn.closest(".ap-value-container").querySelector(".ap-value").value);
}

function apCopyLFNs(me) {
  apDoCopy(me.closest(".ap-details").querySelector(".ap-lfns").value);
}

function apCopyPFNs(me) {
  apDoCopy(me.closest(".ap-details").querySelector(".ap-pfns").value);
}

function apDoCopy(value) {
  navigator.clipboard.writeText(value).then(
    function () {
      /* clipboard successfully set */
    },
    function () {
      /* clipboard write failed */
      Ext.dirac.system_info.msg("Error", "Writing to clipboard failed!", "error");
    }
  );
}
